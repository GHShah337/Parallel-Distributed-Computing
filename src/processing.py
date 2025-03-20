import time
import random
from src.sequential import sequential_square
from src.multiprocessing import multiprocessing_square, pool_map_square, pool_apply_square, process_pool_executor_square,pool_map_async_square

def run_all_processes():
    """Runs all processing methods and prints their execution times."""
    numbers = [random.randint(1, 100) for _ in range(10**7)]
    print(f"Processing {len(numbers)} numbers")

    
    # Sequential execution
    start = time.time()
    sequential_square(numbers)
    print("Sequential time:", time.time() - start)
    
    # Multiprocessing with separate processes
    start = time.time()
    multiprocessing_square(numbers[:100])  # Limiting due to process creation overhead
    print("Multiprocessing individual processes time:", time.time() - start)
    
    # Multiprocessing with pool.map
    start = time.time()
    pool_map_square(numbers)
    print("Multiprocessing pool map time:", time.time() - start)
    
    # Multiprocessing with pool.apply
    start = time.time()
    pool_apply_square(numbers[:100])  # Limiting due to apply() being slower
    print("Multiprocessing pool apply time:", time.time() - start)
    
    # ProcessPoolExecutor
    start = time.time()
    process_pool_executor_square(numbers)
    print("ProcessPoolExecutor time:", time.time() - start)
    # pool_map_async_square
    start = time.time()
    pool_map_async_square(numbers)
    print("Async pool map time:", time.time() - start)
