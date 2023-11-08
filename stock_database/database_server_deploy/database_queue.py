from celery import Celery
from database_query import execute_database_operation

app = Celery('database_queue', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@app.task
def process_message(data):
    # process the query request in the message queue
    result = execute_database_operation(data)
    return result