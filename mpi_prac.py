from mpi4py import MPI
import socket

# Initialize the MPI communicator
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
ip_address = socket.gethostbyname(socket.gethostname())

# Rank 0 prepares data, others start with None
if rank == 0:
    data_to_broadcast = f"Hello from rank 0 at {ip_address}"
else:
    data_to_broadcast = None

# Broadcast data from rank 0 to all ranks (including rank 0 itself)
data_received = comm.bcast(data_to_broadcast, root=0)

# Print the received data on each rank
print(f"Rank {rank}/{size - 1} on {ip_address} received: {data_received}")


