from flask import Flask, session
import os
import redis

app = Flask(__name__)
app.secret_key = os.urandom(24)
cache = redis.Redis(host='localhost', port=6379)

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
   app.run(host='0.0.0.0', port=8080, debug=True)

