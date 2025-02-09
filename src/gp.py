import time
import threading
import multiprocessing

def sequential_sum(n):
    start_time = time.time()
    total = sum(range(1, n+1))
    end_time = time.time()
    return total, end_time - start_time

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

def compute_speedup(sequential_time, parallel_time):
    return sequential_time / parallel_time

def compute_efficiency(speedup, num_units):
    return speedup / num_units

def main():
    n = 10**7
    
    seq_total, seq_time = sequential_sum(n)
    print(f"Sequential Sum: {seq_total}, Time: {seq_time:.4f}s")
    
    thr_total, thr_time = threaded_sum(n)
    print(f"Threaded Sum: {thr_total}, Time: {thr_time:.4f}s")
    
    proc_total, proc_time = process_sum(n)
    print(f"Processed Sum: {proc_total}, Time: {proc_time:.4f}s")
    
    thread_speedup = compute_speedup(seq_time, thr_time)
    process_speedup = compute_speedup(seq_time, proc_time)
    
    print(f"Thread Speedup: {thread_speedup:.4f}, Efficiency: {compute_efficiency(thread_speedup, 4):.4f}")
    print(f"Process Speedup: {process_speedup:.4f}, Efficiency: {compute_efficiency(process_speedup, 4):.4f}")
    
if __name__ == "__main__":
    main()
