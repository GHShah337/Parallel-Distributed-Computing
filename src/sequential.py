from src.square import square

def sequential_square(numbers):
    """Computes squares sequentially using a for loop."""
    result = []
    for num in numbers:
        squared = square(num)
        if num % 100000 == 0:  # Print every 100,000 numbers to verify
            print(f"Processing {num} -> {squared}")
        result.append(squared)
    return result
