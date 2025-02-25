### multiprocessing.py
import time
import multiprocessing

def process_worker(start, end, queue):
    queue.put(sum(range(start, end)))

def process_sum(n, num_processes=4):
    processes = []
    queue = multiprocessing.Queue()
    step = n // num_processes

    start_time = time.time()
    for i in range(num_processes):
        start = i * step + 1
        end = n + 1 if i == num_processes - 1 else (i + 1) * step + 1
        process = multiprocessing.Process(target=process_worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total = sum(queue.get() for _ in range(num_processes))
    end_time = time.time()
    return total, end_time - start_time
