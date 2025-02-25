import time
import threading

def thread_worker(start, end, result, index):
    result[index] = sum(range(start, end))

def threaded_sum(n, num_threads=4):
    threads = []
    result = [0] * num_threads
    step = n // num_threads

    start_time = time.time()
    for i in range(num_threads):
        start = i * step + 1
        end = n + 1 if i == num_threads - 1 else (i + 1) * step + 1
        thread = threading.Thread(target=thread_worker, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(result)
    end_time = time.time()
    return total, end_time - start_time
