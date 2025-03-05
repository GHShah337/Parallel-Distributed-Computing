# main.py
import time
from threading import Thread
from src.simulate_sensor import simulate_sensor, latest_temperatures, temperature_averages
from src.processes import process_temperatures

def display_temperatures():
    while True:
        print("\033[H\033[J")  # Clear the console screen
        print("=" * 43)
        print("Sensor ID \t Latest Temp \t Avg Temp")
        print("=" * 43)

        for sensor_id in latest_temperatures:
            latest_temp = latest_temperatures[sensor_id]
            avg_temp = temperature_averages.get(sensor_id, "N/A")

            if isinstance(avg_temp, (int, float)):
                print(f"{sensor_id:9} \t {latest_temp:11} \t {avg_temp:8.2f}")
            else:
                print(f"{sensor_id:9} \t {latest_temp:11} \t {'--':8}")

        time.sleep(5)

# Main

def main():
    sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]

    for sensor_id in sensor_ids:
        thread = Thread(target=simulate_sensor, args=(sensor_id,), daemon=True)
        thread.start()

    # Start the temperature processing thread
    processing_thread = Thread(target=process_temperatures, daemon=True)
    processing_thread.start()

    # Start the display update thread
    display_thread = Thread(target=display_temperatures, daemon=True)
    display_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    main()
