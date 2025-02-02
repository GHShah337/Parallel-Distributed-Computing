# Function to join a thousand random letters
def join_random_letters(start = 0,
                       end=1000):
    letters = [random.choice(string.ascii_letters) for _ in range(start, end)]
    joined_letters = ''.join(letters)
    print("Joined Letters Task Done")

# Function to add a thousand random numbers
def add_random_numbers():
    numbers = [random.randint(1, 100) for _ in range(1000)]
    total_sum = sum(numbers)
    print("Add Numbers Task Done")
