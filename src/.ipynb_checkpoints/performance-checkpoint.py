
### performance.py
from src.sequential import sequential_sum
from src.thread import threaded_sum
from src.multiprocessing import process_sum

def compute_speedup(sequential_time, parallel_time):
    return sequential_time / parallel_time

def compute_efficiency(speedup, num_units):
    return speedup / num_units

def compute_amdahl_speedup(fraction_serial, num_units):
    return 1 / (fraction_serial + (1 - fraction_serial) / num_units)

def compute_gustafson_speedup(fraction_serial, num_units):
    return num_units - fraction_serial * (num_units - 1)

def performance_analysis(n):
    seq_total, seq_time = sequential_sum(n)
    print(f"Sequential Sum: {seq_total}, Time: {seq_time:.4f}s")

    thr_total, thr_time = threaded_sum(n)
    print(f"Threaded Sum: {thr_total}, Time: {thr_time:.4f}s")

    proc_total, proc_time = process_sum(n)
    print(f"Processed Sum: {proc_total}, Time: {proc_time:.4f}s")

    thread_speedup = compute_speedup(seq_time, thr_time)
    process_speedup = compute_speedup(seq_time, proc_time)

    thread_efficiency = compute_efficiency(thread_speedup, 4)
    process_efficiency = compute_efficiency(process_speedup, 4)

    fraction_serial_thread = (thr_time - seq_time) / seq_time
    fraction_serial_process = (proc_time - seq_time) / seq_time

    amdahl_thread = compute_amdahl_speedup(fraction_serial_thread, 4)
    amdahl_process = compute_amdahl_speedup(fraction_serial_process, 4)

    gustafson_thread = compute_gustafson_speedup(fraction_serial_thread, 4)
    gustafson_process = compute_gustafson_speedup(fraction_serial_process, 4)

    print(f"Thread Speedup: {thread_speedup:.4f}, Efficiency: {thread_efficiency:.4f}")
    print(f"Process Speedup: {process_speedup:.4f}, Efficiency: {process_efficiency:.4f}")

    print(f"Thread Amdahl Speedup: {amdahl_thread:.4f}, Gustafson Speedup: {gustafson_thread:.4f}")
    print(f"Process Amdahl Speedup: {amdahl_process:.4f}, Gustafson Speedup: {gustafson_process:.4f}")
