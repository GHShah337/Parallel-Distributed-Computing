# src/processor.py
import time
from threading import RLock
from queue import Queue

temperature_averages = {}
lock = RLock()

def process_temperatures(sensor_id, queue, update_interval=5):
    while True:
        with lock:
            if not queue.empty():
                data = list(queue.queue)
                average_temp = sum(data) / len(data)
                temperature_averages[sensor_id] = average_temp
                queue.queue.clear()
        time.sleep(update_interval)

