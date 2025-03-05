# src/display.py
import os
import time

def initialize_display():
    os.system("clear")
    print("Current Temperatures:")
    print("Latest Temperatures: Sensor 0: --°C Sensor 1: --°C Sensor 2: --°C")
    print("Sensor 1 Average: --°C")
    print("Sensor 2 Average: --°C")
    print("Sensor 3 Average: --°C")

def update_display(latest_temperatures, temperature_averages):
    os.system("clear")
    print("Current Temperatures:")
    for sensor_id, temp in latest_temperatures.items():
        print(f"Sensor {sensor_id}: {temp}°C", end="  ")
    print("\n")
    for sensor_id, avg in temperature_averages.items():
        print(f"Sensor {sensor_id} Average: {avg:.2f}°C")

