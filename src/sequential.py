import time
import random
import string
from src.tasks import join_random_letters,add_random_letters

def run_sequential(start_letters = 0,
                   end_letters =100000
# Measure the total time for both operations
total_start_time = time.time()
join_random_letters()
add_random_numbers()
total_end_time = time.time()

print(f"Total time taken: {total_end_time - total_start_time} seconds")
