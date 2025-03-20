from src.processing import run_all_processes
from src.connection_pool import ConnectionPool, access_database
import multiprocessing

if __name__ == "__main__":
    run_all_processes()
    pool = ConnectionPool(3)  # Limit to 3 concurrent connections
    processes = [multiprocessing.Process(target=access_database, args=(pool,)) for _ in range(10)]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    
    print("All processes completed.")
    
