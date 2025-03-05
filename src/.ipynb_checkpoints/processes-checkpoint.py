# src/processes.py
import time
from threading import Condition
from src.simulate_sensor import temperature_averages, temperature_queue, data_lock

condition = Condition()

def process_temperatures():
    while True:
        with data_lock:
            while temperature_queue.empty():
                condition.wait()

            readings = list(temperature_queue.queue)  # Get readings
            sensor_data = {}

            for temperature in readings:
                sensor_id = f"sensor_{readings.index(temperature) + 1}"
                if sensor_id not in sensor_data:
                    sensor_data[sensor_id] = []
                sensor_data[sensor_id].append(temperature)

            # Calculate and update the average
            for sensor_id, sensor_readings in sensor_data.items():
                avg_temperature = sum(sensor_readings) / len(sensor_readings)
                temperature_averages[sensor_id] = avg_temperature

        time.sleep(1)

