from rq import Queue
from redis import Redis
import requests

# Connect to Redis
redis_conn = Redis()
task_queue = Queue(connection=redis_conn)

def process_url(url):
    try:
        response = requests.get(url)
        result = response.status_code
        return result
    except Exception as e:
        return str(e)
