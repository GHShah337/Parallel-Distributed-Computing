## sequential.py
import time

def sequential_sum(n):
    start_time = time.time()
    total = sum(range(1, n + 1))
    end_time = time.time()
    return total, end_time - start_time

