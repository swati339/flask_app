# __init__.py
from flask import Flask, session
import os
import redis
from rq import Queue
from worker import conn
from tasks import background_task  # Import the task from the separate module

app = Flask(__name__)
app.secret_key = os.urandom(24)
cache = redis.Redis(host='localhost', port=6379)

# rq queue
q = Queue(connection=conn)

@app.route('/')
def home():
    return "Hello World!"

@app.route('/visit')
def visit():
    if 'visit_count' in session:
        session['visit_count'] = session.get('visit_count') + 1
    else:
        session['visit_count'] = 1
    
    job = q.enqueue(background_task, str(session['visit_count']))
    return f"Visit count: {session['visit_count']}, job id: {job.id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

