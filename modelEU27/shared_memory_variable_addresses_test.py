from mpi4py import MPI
import numpy as np

from repast4py import core
from repast4py.context import SharedContext


# ============================================================
# Parameters
# ============================================================

BASE_FIRMS_PER_RANK = 2_500
MIN_LOCAL_FIRMS = 1_500
MAX_LOCAL_FIRMS = 3_500

N_CYCLES = 3

PRODUCTION = 10.0

MIN_PURCHASE = 0.1
MAX_PURCHASE = 1.0

SEED = 12345


# ============================================================
# Firm
# ============================================================

class Firm(core.Agent):

    TYPE = 0

    def __init__(
        self,
        firm_id: int,
        rank: int,
        address: int = -1,
        acquisti: float = 0.0,
    ):
        super().__init__(
            id=firm_id,
            type=Firm.TYPE,
            rank=rank,
        )

        # Compact global position in the shared warehouse array.
        # This is a logical index, not a raw memory pointer.
        self.address = int(address)

        # Cumulative purchases made by this Firm.
        self.acquisti = float(acquisti)

    def save(self):
        """
        Return the state needed by Repast4Py to create a ghost.
        """
        return (
            self.uid,
            self.address,
            self.acquisti,
        )


# ============================================================
# Repast4Py restore function
# ============================================================

def restore_firm(data):
    """
    Recreate a Firm from the tuple returned by Firm.save().
    """

    uid = data[0]
    address = data[1]
    acquisti = data[2]

    return Firm(
        firm_id=uid[0],
        rank=uid[2],
        address=address,
        acquisti=acquisti,
    )


# ============================================================
# Shared-memory synchronization
# ============================================================

def sync_shared(win, shared_comm):
    """
    Make direct shared-memory load/store operations visible
    and synchronize all ranks in the shared-memory communicator.

    win.Lock_all() must already be active.
    """

    win.Sync()
    shared_comm.Barrier()
    win.Sync()


# ============================================================
# Per-Firm atomic spinlock
# ============================================================

def acquire_firm_lock(
    win,
    target_rank,
    target_disp,
    zero,
    one,
    result,
):
    """
    Acquire one Firm-specific lock with MPI Compare_and_swap.

    Lock values:
        0 = free
        1 = occupied

    The operation is atomic:
        if lock == 0:
            lock = 1
            acquisition succeeds

    Return the number of failed attempts before acquisition.
    """

    spins = 0

    while True:

        result[0] = -1

        win.Compare_and_swap(
            one,
            zero,
            result,
            target_rank,
            target_disp,
        )

        win.Flush(target_rank)

        if result[0] == 0:
            return spins

        spins += 1


def release_firm_lock(
    win,
    target_rank,
    target_disp,
    zero,
    one,
    result,
):
    """
    Release one Firm-specific lock atomically.
    """

    result[0] = -1

    win.Compare_and_swap(
        zero,
        one,
        result,
        target_rank,
        target_disp,
    )

    win.Flush(target_rank)

    if result[0] != 1:
        raise RuntimeError(
            "Attempt to release a Firm lock "
            f"whose previous value was {result[0]}"
        )


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # MPI world
    # --------------------------------------------------------

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()

    processor_name = MPI.Get_processor_name()

    # --------------------------------------------------------
    # Shared-memory communicator
    #
    # This test requires all MPI ranks to run on the same
    # physical machine / shared-memory node.
    # --------------------------------------------------------

    shared_comm = comm.Split_type(
        MPI.COMM_TYPE_SHARED,
        key=rank,
    )

    shared_rank = shared_comm.Get_rank()
    shared_size = shared_comm.Get_size()

    if shared_size != size:

        if rank == 0:
            print()
            print("ERROR")
            print(
                "This test requires all MPI ranks to run "
                "on the same shared-memory node."
            )

        shared_comm.Free()
        return

    # --------------------------------------------------------
    # Repast4Py context
    # --------------------------------------------------------

    context = SharedContext(comm)

    # --------------------------------------------------------
    # Create a variable number of local Firms on each rank.
    #
    # In the real model this number may depend on probabilities
    # by class, sector, country, size, and other characteristics.
    #
    # Here we emulate that situation with a deterministic random
    # number of local Firms for each rank.
    # --------------------------------------------------------

    local_rng = np.random.default_rng(
        SEED + 1000 + rank
    )

    if size == 1:
        n_local = BASE_FIRMS_PER_RANK * 4
    else:
        n_local = int(
            local_rng.integers(
                MIN_LOCAL_FIRMS,
                MAX_LOCAL_FIRMS + 1,
            )
        )

    local_firms = []

    # uid[0] is local to the owning rank.
    #
    # Therefore the same uid[0] may exist on different ranks.
    # The complete Repast4Py identity is:
    #
    #     (uid[0], uid[1], uid[2])
    #
    # where uid[2] is the owning rank.
    for local_id in range(n_local):

        aFirm = Firm(
            firm_id=local_id,
            rank=rank,
        )

        context.add(aFirm)
        local_firms.append(aFirm)

    # --------------------------------------------------------
    # Collect only the number of Firms created on each rank.
    #
    # Every rank receives the same counts array.
    # --------------------------------------------------------

    counts = comm.allgather(
        n_local
    )

    counts = np.asarray(
        counts,
        dtype=np.int64,
    )

    # --------------------------------------------------------
    # Compute the starting address of each rank.
    #
    # Example:
    #
    # counts  = [2300, 2718, 1941, 3041]
    # offsets = [   0, 2300, 5018, 6959]
    #
    # Each rank owns one contiguous block of global addresses.
    # --------------------------------------------------------

    offsets = np.zeros(
        size,
        dtype=np.int64,
    )

    if size > 1:
        offsets[1:] = np.cumsum(
            counts[:-1]
        )

    total_firms = int(
        counts.sum()
    )

    # --------------------------------------------------------
    # Assign one compact and globally unique shared-memory
    # address to every local Firm.
    #
    # The address does not depend directly on uid[0].
    # It depends on the Firm's local position plus the offset
    # of its owning rank.
    #
    # Therefore:
    #
    #     address = offsets[uid[2]] + local_position
    #
    # This remains compact even if the real model later uses
    # sparse or non-consecutive uid[0] values.
    # --------------------------------------------------------

    for local_position, aFirm in enumerate(
        local_firms
    ):

        aFirm.address = int(
            offsets[rank]
            + local_position
        )

    # --------------------------------------------------------
    # Create ghosts after the addresses have been assigned.
    #
    # Every ghost receives exactly the same address as its
    # owning Firm through Firm.save() / restore_firm().
    # --------------------------------------------------------

    requested = []

    if size > 1:

        for owner_rank in range(size):

            if owner_rank == rank:
                continue

            owner_count = int(
                counts[owner_rank]
            )

            for local_id in range(
                owner_count
            ):

                requested.append(
                    (
                        (
                            local_id,
                            Firm.TYPE,
                            owner_rank,
                        ),
                        owner_rank,
                    )
                )

    ghost_firms = context.request_agents(
        requested,
        restore_firm,
    )

    visible_firms = (
        local_firms
        + list(ghost_firms)
    )

    # Sorting is not required for correctness.
    # It is used only to make diagnostics easier to inspect.
    visible_firms.sort(
        key=lambda agent: agent.address
    )

    print(
        f"rank {rank}: "
        f"node={processor_name}, "
        f"{len(local_firms)} local, "
        f"{len(ghost_firms)} ghosts, "
        f"{len(visible_firms)} visible, "
        f"offset={offsets[rank]}"
    )

    if len(visible_firms) != total_firms:

        raise RuntimeError(
            f"rank {rank}: expected {total_firms} visible Firms, "
            f"found {len(visible_firms)}"
        )

    comm.Barrier()

    if rank == 0:

        print()
        print(
            f"MPI ranks: {size}; "
            f"shared-memory ranks: {shared_size}"
        )

        print(
            f"local Firm counts: {counts.tolist()}"
        )

        print(
            f"rank offsets: {offsets.tolist()}"
        )

        print(
            f"total Firms: {total_firms}"
        )

    # ========================================================
    # Shared-memory layout
    #
    # The single shared window contains:
    #
    #   [ total_firms float64 warehouses ]
    #   [ total_firms int32   lock flags ]
    #
    # Only shared rank 0 physically allocates the memory.
    # All other ranks map the same shared segment.
    # ========================================================

    float_size = np.dtype(
        np.float64
    ).itemsize

    int_size = np.dtype(
        np.int32
    ).itemsize

    warehouse_offset = 0

    locks_offset = (
        total_firms
        * float_size
    )

    total_nbytes = (
        total_firms * float_size
        + total_firms * int_size
    )

    if shared_rank == 0:
        local_nbytes = total_nbytes
    else:
        local_nbytes = 0

    win = MPI.Win.Allocate_shared(
        local_nbytes,
        1,
        comm=shared_comm,
    )

    buffer, disp_unit = win.Shared_query(
        0
    )

    warehouse = np.ndarray(
        buffer=buffer,
        dtype=np.float64,
        shape=(total_firms,),
        offset=warehouse_offset,
    )

    lock_flags = np.ndarray(
        buffer=buffer,
        dtype=np.int32,
        shape=(total_firms,),
        offset=locks_offset,
    )

    # Keep one passive-target RMA access epoch open for the
    # complete simulation.
    win.Lock_all()

    # --------------------------------------------------------
    # Initialize shared memory
    # --------------------------------------------------------

    if shared_rank == 0:

        warehouse[:] = 0.0
        lock_flags[:] = 0

    sync_shared(
        win,
        shared_comm,
    )

    # --------------------------------------------------------
    # Private Compare-and-swap buffers
    # --------------------------------------------------------

    zero = np.array(
        [0],
        dtype=np.int32,
    )

    one = np.array(
        [1],
        dtype=np.int32,
    )

    cas_result = np.empty(
        1,
        dtype=np.int32,
    )

    # --------------------------------------------------------
    # Random generator used for purchase decisions
    # --------------------------------------------------------

    rng = np.random.default_rng(
        SEED + rank
    )

    # ========================================================
    # Simulation
    # ========================================================

    try:

        for cycle in range(
            1,
            N_CYCLES + 1,
        ):

            # =================================================
            # PHASE 1: production
            #
            # Each local Firm writes only to its own warehouse
            # slot, so no lock is required in this phase.
            # =================================================

            for aFirm in local_firms:

                warehouse[
                    aFirm.address
                ] += PRODUCTION

            sync_shared(
                win,
                shared_comm,
            )

            # =================================================
            # PHASE 2: purchases
            #
            # Each local Firm chooses another Firm among all
            # visible Firms, including ghosts when size > 1.
            # Only the selected supplier's lock is acquired.
            # =================================================

            local_transactions = 0
            local_ghost_suppliers = 0
            local_bought_this_cycle = 0.0

            local_total_spins = 0
            local_contended_transactions = 0
            local_max_spins = 0

            for aFirm in local_firms:

                # ---------------------------------------------
                # Select another Firm.
                # ---------------------------------------------

                while True:

                    supplier = visible_firms[
                        int(
                            rng.integers(
                                0,
                                len(visible_firms),
                            )
                        )
                    ]

                    if (
                        supplier.address
                        != aFirm.address
                    ):
                        break

                if supplier.uid_rank != rank:
                    local_ghost_suppliers += 1

                wanted = float(
                    rng.uniform(
                        MIN_PURCHASE,
                        MAX_PURCHASE,
                    )
                )

                # ---------------------------------------------
                # Compute the byte displacement of this
                # supplier-specific atomic lock.
                # ---------------------------------------------

                supplier_lock_disp = (
                    locks_offset
                    + supplier.address * int_size
                )

                # ---------------------------------------------
                # Acquire only this supplier's lock.
                # ---------------------------------------------

                spins = acquire_firm_lock(
                    win=win,
                    target_rank=0,
                    target_disp=supplier_lock_disp,
                    zero=zero,
                    one=one,
                    result=cas_result,
                )

                local_total_spins += spins

                if spins > 0:
                    local_contended_transactions += 1

                if spins > local_max_spins:
                    local_max_spins = spins

                try:

                    # Synchronize this process's direct
                    # shared-memory view before the read /
                    # modify / write transaction.
                    win.Sync()

                    available = float(
                        warehouse[
                            supplier.address
                        ]
                    )

                    bought = min(
                        wanted,
                        available,
                    )

                    warehouse[
                        supplier.address
                    ] = (
                        available
                        - bought
                    )

                    aFirm.acquisti += bought

                    local_bought_this_cycle += (
                        bought
                    )

                    # Publish the updated warehouse value
                    # before releasing the supplier lock.
                    win.Sync()

                finally:

                    # -----------------------------------------
                    # Release only this supplier's lock.
                    # -----------------------------------------

                    release_firm_lock(
                        win=win,
                        target_rank=0,
                        target_disp=supplier_lock_disp,
                        zero=zero,
                        one=one,
                        result=cas_result,
                    )

                local_transactions += 1

            # -------------------------------------------------
            # End-of-cycle synchronization
            # -------------------------------------------------

            sync_shared(
                win,
                shared_comm,
            )

            # =================================================
            # Diagnostics
            # =================================================

            local_acquisti_total = sum(
                aFirm.acquisti
                for aFirm in local_firms
            )

            total_acquisti = comm.allreduce(
                local_acquisti_total,
                op=MPI.SUM,
            )

            bought_this_cycle = comm.allreduce(
                local_bought_this_cycle,
                op=MPI.SUM,
            )

            total_transactions = comm.allreduce(
                local_transactions,
                op=MPI.SUM,
            )

            total_ghost_suppliers = comm.allreduce(
                local_ghost_suppliers,
                op=MPI.SUM,
            )

            total_spins = comm.allreduce(
                local_total_spins,
                op=MPI.SUM,
            )

            contended_transactions = comm.allreduce(
                local_contended_transactions,
                op=MPI.SUM,
            )

            max_spins = comm.allreduce(
                local_max_spins,
                op=MPI.MAX,
            )

            if rank == 0:

                total_warehouse = float(
                    warehouse.sum()
                )

                total_produced = (
                    total_firms
                    * PRODUCTION
                    * cycle
                )

                conservation = (
                    total_warehouse
                    + total_acquisti
                )

                error = (
                    conservation
                    - total_produced
                )

                locked_at_end = int(
                    np.count_nonzero(
                        lock_flags
                    )
                )

                print()
                print(
                    "========================================"
                )
                print(
                    f"CYCLE {cycle}"
                )
                print(
                    "========================================"
                )

                print(
                    f"produced cumulative = "
                    f"{total_produced:,.6f}"
                )

                print(
                    f"warehouse total     = "
                    f"{total_warehouse:,.6f}"
                )

                print(
                    f"purchases this cycle= "
                    f"{bought_this_cycle:,.6f}"
                )

                print(
                    f"purchases cumulative= "
                    f"{total_acquisti:,.6f}"
                )

                print(
                    f"warehouse + purchases = "
                    f"{conservation:,.6f}"
                )

                print(
                    f"transactions        = "
                    f"{total_transactions:,}"
                )

                if size > 1:

                    print(
                        f"ghost suppliers     = "
                        f"{total_ghost_suppliers:,}"
                    )

                print(
                    f"contended purchases = "
                    f"{contended_transactions:,}"
                )

                print(
                    f"total failed CAS     = "
                    f"{total_spins:,}"
                )

                print(
                    f"max CAS retries      = "
                    f"{max_spins:,}"
                )

                print(
                    f"locks still set     = "
                    f"{locked_at_end:,}"
                )

                print(
                    f"conservation error  = "
                    f"{error:.12g}"
                )

            comm.Barrier()

        # ====================================================
        # Final address / warehouse sample
        # ====================================================

        sync_shared(
            win,
            shared_comm,
        )

        if rank == 0:

            print()
            print(
                "First 10 shared warehouse positions:"
            )

            for i in range(
                min(
                    10,
                    total_firms,
                )
            ):

                print(
                    f"address {i:5d}: "
                    f"warehouse = "
                    f"{warehouse[i]:10.6f}, "
                    f"lock = {lock_flags[i]}"
                )

            print()
            print(
                "First Firm of each rank:"
            )

            for owner_rank in range(size):

                if counts[owner_rank] == 0:
                    continue

                address = int(
                    offsets[owner_rank]
                )

                print(
                    f"rank {owner_rank}: "
                    f"uid=(0, {Firm.TYPE}, {owner_rank}), "
                    f"address={address}, "
                    f"warehouse={warehouse[address]:.6f}"
                )

            print()
            print(
                "Expected final cumulative production:"
            )

            print(
                f"{total_firms} * {PRODUCTION} * "
                f"{N_CYCLES} = "
                f"{total_firms * PRODUCTION * N_CYCLES:,.6f}"
            )

    finally:

        # ----------------------------------------------------
        # Clean shutdown
        # ----------------------------------------------------

        comm.Barrier()

        win.Sync()
        win.Unlock_all()

        win.Free()
        shared_comm.Free()


# ============================================================
# Start
# ============================================================

if __name__ == "__main__":
    main()
