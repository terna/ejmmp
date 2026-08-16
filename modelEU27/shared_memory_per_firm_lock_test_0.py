from mpi4py import MPI
import numpy as np

from repast4py import core
from repast4py.context import SharedContext


# ============================================================
# Parameters
# ============================================================

N_FIRMS = 10_000
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
        address: int,
        acquisti: float = 0.0,
    ):
        super().__init__(
            id=firm_id,
            type=Firm.TYPE,
            rank=rank,
        )

        # Logical address in the shared warehouse array.
        self.address = int(address)

        # Cumulative purchases made by this Firm.
        self.acquisti = float(acquisti)

    def save(self):
        """
        State used by Repast4Py to create a ghost.
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
    Make direct load/store accesses to the shared window
    visible and synchronize all ranks on this node.

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
    Acquire one Firm's lock with MPI Compare_and_swap.

    lock value:
        0 = free
        1 = occupied

    Atomically:
        if lock == 0:
            lock = 1
            acquisition succeeds

    Returns the number of failed attempts before acquisition.
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

        # Complete the atomic operation and make result valid.
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
    Release one Firm's lock atomically.

    Atomically:
        if lock == 1:
            lock = 0
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
    # Create local Firms
    #
    # Firm i belongs to:
    #
    #     owner_rank = i % size
    #
    # Firm.address is the global Firm number and therefore
    # also the index of its warehouse slot.
    # --------------------------------------------------------

    local_firms = []

    for firm_id in range(N_FIRMS):

        owner_rank = firm_id % size

        if owner_rank == rank:

            aFirm = Firm(
                firm_id=firm_id,
                rank=rank,
                address=firm_id,
            )

            context.add(aFirm)
            local_firms.append(aFirm)

    # --------------------------------------------------------
    # Create ghosts
    #
    # Every rank requests all Firms owned by all other ranks.
    # Thus every rank sees all N_FIRMS Firms.
    # --------------------------------------------------------

    requested = []

    if size > 1:

        for firm_id in range(N_FIRMS):

            owner_rank = firm_id % size

            if owner_rank != rank:

                requested.append(
                    (
                        (
                            firm_id,
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

    visible_firms.sort(
        key=lambda agent: agent.address
    )

    print(
        f"rank {rank}: "
        f"node={processor_name}, "
        f"{len(local_firms)} local, "
        f"{len(ghost_firms)} ghosts, "
        f"{len(visible_firms)} visible"
    )

    if len(visible_firms) != N_FIRMS:

        raise RuntimeError(
            f"rank {rank}: expected {N_FIRMS} visible Firms, "
            f"found {len(visible_firms)}"
        )

    comm.Barrier()

    if rank == 0:

        print()
        print(
            f"MPI ranks: {size}; "
            f"shared-memory ranks: {shared_size}"
        )

    # ========================================================
    # ONE SHARED WINDOW
    #
    # The shared memory contains:
    #
    #   [ N_FIRMS float64 warehouses ]
    #   [ N_FIRMS int32   lock flags ]
    #
    # Only shared rank 0 physically allocates the memory.
    # All other ranks map the same segment.
    #
    # disp_unit = 1 byte.
    #
    # This lets us address each atomic lock precisely by
    # byte displacement with MPI.Compare_and_swap.
    # ========================================================

    float_size = np.dtype(np.float64).itemsize
    int_size = np.dtype(np.int32).itemsize

    warehouse_offset = 0

    locks_offset = (
        N_FIRMS
        * float_size
    )

    total_nbytes = (
        N_FIRMS * float_size
        + N_FIRMS * int_size
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

    buffer, disp_unit = win.Shared_query(0)

    warehouse = np.ndarray(
        buffer=buffer,
        dtype=np.float64,
        shape=(N_FIRMS,),
        offset=warehouse_offset,
    )

    lock_flags = np.ndarray(
        buffer=buffer,
        dtype=np.int32,
        shape=(N_FIRMS,),
        offset=locks_offset,
    )

    # Long-lived passive-target RMA access epoch.
    #
    # This is required for Win.Sync and for the atomic
    # Compare_and_swap operations used below.
    win.Lock_all()

    # --------------------------------------------------------
    # Initialize shared memory
    # --------------------------------------------------------

    if shared_rank == 0:

        warehouse[:] = 0.0

        # Every Firm starts unlocked.
        lock_flags[:] = 0

    sync_shared(
        win,
        shared_comm,
    )

    # --------------------------------------------------------
    # Buffers used by Compare_and_swap
    #
    # They remain private to each MPI process.
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
    # RNG
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
            # Every local Firm writes only its own warehouse.
            # Therefore no Firm lock is needed here.
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
            # Each local Firm chooses a supplier among all
            # visible Firms (local + ghosts).
            #
            # Only the selected supplier's lock is acquired.
            # Other suppliers remain accessible concurrently.
            # =================================================

            local_transactions = 0
            local_ghost_suppliers = 0
            local_bought_this_cycle = 0.0

            local_total_spins = 0
            local_contended_transactions = 0
            local_max_spins = 0

            for aFirm in local_firms:

                # ---------------------------------------------
                # Choose another Firm
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
                # Address of this supplier's atomic lock.
                #
                # Because disp_unit == 1, target_disp is a
                # BYTE displacement.
                # ---------------------------------------------

                supplier_lock_disp = (
                    locks_offset
                    + supplier.address * int_size
                )

                # =============================================
                # Acquire ONLY this supplier's lock
                # =============================================

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

                    # Synchronize the direct shared-memory
                    # load/store operations around the critical
                    # section.
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

                    # Publish the warehouse update before the
                    # supplier lock is released.
                    win.Sync()

                finally:

                    # =========================================
                    # Release ONLY this supplier's lock
                    # =========================================

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
                    N_FIRMS
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
        # Final sample
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

            for i in range(10):

                print(
                    f"Firm {i:5d}: "
                    f"warehouse = "
                    f"{warehouse[i]:10.6f}, "
                    f"lock = {lock_flags[i]}"
                )

            print()
            print(
                "Expected final cumulative production:"
            )

            print(
                f"{N_FIRMS} * {PRODUCTION} * "
                f"{N_CYCLES} = "
                f"{N_FIRMS * PRODUCTION * N_CYCLES:,.6f}"
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
