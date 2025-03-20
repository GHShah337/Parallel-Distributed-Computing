import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from src.square import square

def multiprocessing_square(numbers):
    """Computes squares using multiprocessing, spawning a process for each number."""
    processes = []
    results = multiprocessing.Manager().list()

    def worker(n, results):
        results.append(square(n))

    for num in numbers:
        p = multiprocessing.Process(target=worker, args=(num, results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return list(results)

def pool_map_square(numbers):
    """Computes squares using multiprocessing.Pool with map() function."""
    with multiprocessing.Pool() as pool:
        result = pool.map(square, numbers)
    return result

def pool_apply_square(numbers):
    """Computes squares using multiprocessing.Pool with apply() function."""
    with multiprocessing.Pool() as pool:
        results = []
        for num in numbers:
            results.append(pool.apply(square, (num,)))
    return results

def process_pool_executor_square(numbers):
    """Computes squares using concurrent.futures.ProcessPoolExecutor."""
    with ProcessPoolExecutor() as executor:
        result = list(executor.map(square, numbers))
    return result

def pool_map_async_square(numbers):
    """Computes squares asynchronously using multiprocessing.Pool with map_async() function."""
    with multiprocessing.Pool() as pool:
        result = pool.map_async(square, numbers)
        return result.get()
