# main.py
import threading
from queue import Queue
from src.sensor import simulate_sensor
from src.processor import process_temperatures
from src.display import initialize_display, update_display
from threading import RLock
lock = RLock

def main():
    num_sensors = 3
    queues = [Queue() for _ in range(num_sensors)]

    # Initialize sensors
    for i in range(num_sensors):
        threading.Thread(target=simulate_sensor, args=(i,), daemon=True).start()

    # Initialize processors
    for i, q in enumerate(queues):
        threading.Thread(target=process_temperatures, args=(i, q), daemon=True).start()

    initialize_display()

    # Update display every 5 seconds
    while True:
        for i in range(num_sensors):
            with lock:
                if i in latest_temperatures:
                    queues[i].put(latest_temperatures[i])
        update_display(latest_temperatures, temperature_averages)
        time.sleep(5)

if __name__ == "__main__":
    main()