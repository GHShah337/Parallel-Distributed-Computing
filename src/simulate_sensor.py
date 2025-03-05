# src/simulate_sensor.py
import random
import time
from threading import RLock
import queue

latest_temperatures = {}
temperature_averages = {}
temperature_queue = queue.Queue(maxsize=10)

data_lock = RLock()

def simulate_sensor(sensor_id):
    while True:
        temperature = random.randint(15, 40)
        with data_lock:
            latest_temperatures[sensor_id] = temperature

        if not temperature_queue.full():
            temperature_queue.put(temperature)
        else:
            temperature_queue.get()
            temperature_queue.put(temperature)

        time.sleep(1)

