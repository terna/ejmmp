# shared_memory_test_0.py

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

# Each purchase is a random quantity between these limits.
MIN_PURCHASE = 0.1
MAX_PURCHASE = 1.0


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
        self.address = address

        # Total purchases made by this firm.
        self.acquisti = acquisti


    def save(self):
        """
        State used by Repast4Py when creating a ghost.
        """
        return (
            self.uid,
            self.address,
            self.acquisti,
        )


# ============================================================
# Restore Firm
# ============================================================

def restore_firm(data):
    """
    Creates a Firm from the tuple returned by Firm.save().
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
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # MPI world
    # --------------------------------------------------------

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()


    # --------------------------------------------------------
    # Check that all ranks are on the same physical node.
    #
    # MPI shared memory works only among ranks belonging
    # to the same shared-memory domain.
    # --------------------------------------------------------

    shared_comm = comm.Split_type(
        MPI.COMM_TYPE_SHARED,
        key=rank,
    )

    shared_rank = shared_comm.Get_rank()
    shared_size = shared_comm.Get_size()

    if shared_size != size:

        if rank == 0:
            print(
                "ERROR: not all MPI ranks are on the same "
                "shared-memory node."
            )

        shared_comm.Free()
        return


    # --------------------------------------------------------
    # Repast4Py context
    # --------------------------------------------------------

    context = SharedContext(comm)


    # --------------------------------------------------------
    # Create the local Firms.
    #
    # Global firm i belongs to:
    #
    #     owner_rank = i % size
    #
    # address is simply its global firm number.
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


    print(
        f"rank {rank}: "
        f"{len(local_firms)} local firms"
    )


    # --------------------------------------------------------
    # Create ghosts.
    #
    # Every rank requests ALL firms belonging to all the
    # other ranks.
    #
    # Consequently every rank sees the complete population:
    #
    #     local firms + ghosts = 10,000
    # --------------------------------------------------------

    ghost_firms = []

    if size > 1:

        requested = []

        for firm_id in range(N_FIRMS):

            owner_rank = firm_id % size

            if owner_rank != rank:

                uid = (
                    firm_id,
                    Firm.TYPE,
                    owner_rank,
                )

                requested.append(
                    (
                        uid,
                        owner_rank,
                    )
                )

        ghost_firms = context.request_agents(
            requested,
            restore_firm,
        )


    # Complete population visible from this rank.
    visible_firms = local_firms + list(ghost_firms)


    print(
        f"rank {rank}: "
        f"{len(local_firms)} local, "
        f"{len(ghost_firms)} ghosts, "
        f"{len(visible_firms)} visible"
    )


    # --------------------------------------------------------
    # Create the shared memory.
    #
    # We allocate the complete warehouse array ONLY on
    # shared rank 0.
    #
    # All the other ranks allocate zero bytes and then obtain
    # a view of rank 0's shared memory.
    # --------------------------------------------------------

    itemsize = np.dtype(np.float64).itemsize

    if shared_rank == 0:
        nbytes = N_FIRMS * itemsize
    else:
        nbytes = 0


    win = MPI.Win.Allocate_shared(
        nbytes,
        itemsize,
        comm=shared_comm,
    )


    # Obtain the memory allocated by shared rank 0.
    buf, disp_unit = win.Shared_query(0)


    # Create a NumPy array using exactly that memory.
    warehouse = np.ndarray(
        buffer=buf,
        dtype=np.float64,
        shape=(N_FIRMS,),
    )


    # --------------------------------------------------------
    # Initialize the warehouse.
    #
    # Only rank 0 writes the initial values.
    # --------------------------------------------------------

    if shared_rank == 0:
        warehouse[:] = 0.0

    win.Sync()
    shared_comm.Barrier()
    win.Sync()


    # --------------------------------------------------------
    # Random generator.
    #
    # Different deterministic sequence on each rank.
    # --------------------------------------------------------

    rng = np.random.default_rng(
        seed=12345 + rank
    )


    # ========================================================
    # Simulation cycles
    # ========================================================

    for cycle in range(1, N_CYCLES + 1):

        # ====================================================
        # PHASE 1
        #
        # Every LOCAL firm adds production to its own
        # warehouse location.
        #
        # No lock is necessary here because each location has
        # exactly one writer: its owner firm.
        # ====================================================

        for aFirm in local_firms:

            warehouse[aFirm.address] += PRODUCTION


        # Make production visible before purchasing starts.
        win.Sync()
        shared_comm.Barrier()
        win.Sync()


        # ====================================================
        # PHASE 2
        #
        # Every LOCAL firm chooses another visible firm.
        #
        # In mono-rank it chooses another local firm.
        #
        # In multi-rank visible_firms contains both local
        # firms and ghosts.
        # ====================================================

        local_transactions = 0
        local_from_ghost = 0

        for aFirm in local_firms:

            # -----------------------------------------------
            # Choose another Firm.
            # -----------------------------------------------

            while True:

                j = rng.integers(
                    0,
                    len(visible_firms),
                )

                supplier = visible_firms[j]

                if supplier.address != aFirm.address:
                    break


            # -----------------------------------------------
            # Determine whether the selected supplier is a
            # ghost on this rank.
            # -----------------------------------------------

            supplier_is_ghost = (
                supplier.uid_rank != rank
            )

            if supplier_is_ghost:
                local_from_ghost += 1


            # -----------------------------------------------
            # Desired purchase.
            # -----------------------------------------------

            wanted = rng.uniform(
                MIN_PURCHASE,
                MAX_PURCHASE,
            )


            # =================================================
            # GLOBAL EXCLUSIVE LOCK
            #
            # All warehouse memory belongs to shared rank 0.
            #
            # Every transaction acquires an exclusive lock
            # on that target.
            #
            # Thus only one rank at a time can execute this
            # protected section.
            # =================================================

            win.Lock(
                0,
                MPI.LOCK_EXCLUSIVE,
            )

            try:

                win.Sync()

                available = warehouse[
                    supplier.address
                ]

                bought = min(
                    wanted,
                    available,
                )

                warehouse[
                    supplier.address
                ] -= bought

                aFirm.acquisti += bought

                win.Sync()

            finally:

                win.Unlock(0)


            local_transactions += 1


        # ====================================================
        # End of cycle synchronization
        # ====================================================

        win.Sync()
        shared_comm.Barrier()
        win.Sync()


        # ====================================================
        # Statistics
        # ====================================================

        local_acquisti = sum(
            aFirm.acquisti
            for aFirm in local_firms
        )

        total_acquisti = comm.allreduce(
            local_acquisti,
            op=MPI.SUM,
        )

        total_transactions = comm.allreduce(
            local_transactions,
            op=MPI.SUM,
        )

        total_from_ghost = comm.allreduce(
            local_from_ghost,
            op=MPI.SUM,
        )


        if rank == 0:

            total_warehouse = warehouse.sum()

            total_produced = (
                N_FIRMS
                * PRODUCTION
                * cycle
            )

            conservation = (
                total_warehouse
                + total_acquisti
            )

            print()
            print(
                "======================================"
            )
            print(f"CYCLE {cycle}")
            print(
                "======================================"
            )
            print(
                f"produced       = "
                f"{total_produced:,.6f}"
            )
            print(
                f"warehouse      = "
                f"{total_warehouse:,.6f}"
            )
            print(
                f"purchases      = "
                f"{total_acquisti:,.6f}"
            )
            print(
                f"warehouse+acq. = "
                f"{conservation:,.6f}"
            )
            print(
                f"transactions   = "
                f"{total_transactions:,}"
            )

            if size > 1:
                print(
                    f"ghost suppliers= "
                    f"{total_from_ghost:,}"
                )

            print(
                f"error           = "
                f"{conservation - total_produced:.12g}"
            )


        comm.Barrier()


    # ========================================================
    # Some individual examples
    # ========================================================

    if rank == 0:

        print()
        print("First 10 warehouse positions:")

        for i in range(10):

            print(
                f"Firm {i:5d}: "
                f"warehouse = {warehouse[i]:10.6f}"
            )


    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    comm.Barrier()

    win.Free()
    shared_comm.Free()


# ============================================================
# Start
# ============================================================

if __name__ == "__main__":
    main()