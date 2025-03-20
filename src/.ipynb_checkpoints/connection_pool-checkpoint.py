import multiprocessing
import time
import random

class ConnectionPool:
    def __init__(self, size):
        self.pool = [f"Connection {i}" for i in range(size)]
        self.semaphore = multiprocessing.Semaphore(size)
        self.lock = multiprocessing.Lock()

    def get_connection(self):
        self.semaphore.acquire()
        with self.lock:
            return self.pool.pop()
    
    def release_connection(self, conn):
        with self.lock:
            self.pool.append(conn)
        self.semaphore.release()

def access_database(pool):
    conn = pool.get_connection()
    print(f"{multiprocessing.current_process().name} acquired {conn}")
    time.sleep(random.uniform(1, 3))
    pool.release_connection(conn)
    print(f"{multiprocessing.current_process().name} released {conn}")
