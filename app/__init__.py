from flask import Flask, session
import os
from redis import Redis, RedisError


app = Flask(__name__)
app.secret_key = os.urandom(20)

# redis_client = Redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
try:
    redis = Redis(host='localhost', port=6379)
    redis.ping()
    print("Connected to Redis!")
except RedisError as error:
    print(f"Failed to connect to Redis: {error}")

@app.route('/')
def home():
    return "Hello World!"

@app.route('/visit')
def visit():
    if 'visit_count' in session:
        session['visit_count'] = session.get('visit_count') + 1
    else:
        session['visit_count'] = 1
    
    return f'You have visited this page {session["visit_count"]} times.'





if __name__ == '__main__':
    app.run(debug=True)

