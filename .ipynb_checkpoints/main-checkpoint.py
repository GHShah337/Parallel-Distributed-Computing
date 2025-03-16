from src.first_celery import dispatch_tasks
if __name__ == "__main__":
    results = dispatch_tasks()
    print(results[:10])  # Print first 10 results
