import multiprocessing
import time
import random
import string

# Function to join a thousand random letters
def join_random_letters():
    letters = [random.choice(string.ascii_letters) for _ in range(1000)]
    joined_letters = ''.join(letters)
    print("Joined Letters Task Done")

# Function to add a thousand random numbers
def add_random_numbers():
    numbers = [random.randint(1, 100) for _ in range(1000)]
    total_sum = sum(numbers)
    print("Add Numbers Task Done")

# Measure the total time for both operations
if __name__ == "__main__":
    total_start_time = time.time()
    # Create processes for both functions
    process_letters = multiprocessing.Process(target=join_random_letters)
    process_numbers = multiprocessing.Process(target=add_random_numbers)
    # Start the processes
    process_letters.start()
    process_numbers.start()
    # Wait for all processes to complete
    process_letters.join()
    process_numbers.join()
    total_end_time = time.time()
    print(f"Total time taken: {total_end_time - total_start_time} seconds")
