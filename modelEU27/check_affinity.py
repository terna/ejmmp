from mpi4py import MPI
import os
import socket

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

hostname = socket.gethostname()

# CPUs on which this MPI process is allowed to run
try:
    affinity = sorted(os.sched_getaffinity(0))
except AttributeError:
    affinity = ["os.sched_getaffinity not available"]

# Current CPU, if supported by the Python / OS combination
try:
    current_cpu = os.sched_getcpu()
except AttributeError:
    current_cpu = "not available"

info = (
    rank,
    hostname,
    affinity,
    current_cpu,
)

# Gather everything on rank 0 so that the output is ordered
all_info = comm.gather(info, root=0)

if rank == 0:
    print()
    print("MPI CPU AFFINITY CHECK")
    print("======================")
    print("Number of MPI ranks:", size)
    print()

    for r, host, cpus, cpu in all_info:
        print(
            f"rank {r:3d} | "
            f"host {host} | "
            f"affinity {cpus} | "
            f"current CPU {cpu}"
        )

comm.Barrier()