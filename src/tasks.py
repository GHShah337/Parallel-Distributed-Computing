from celery import Celery

# Configure Celery to use RabbitMQ as the message broker
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def power(n, exponent):
    return n ** exponent