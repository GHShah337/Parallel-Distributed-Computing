# src/sensor.py
import time
import random
from threading import RLock

latest_temperatures = {}
lock = RLock()

def simulate_sensor(sensor_id, update_interval=1):
    while True:
        temperature = random.randint(15, 40)
        with lock:
            latest_temperatures[sensor_id] = temperature
        time.sleep(update_interval)

