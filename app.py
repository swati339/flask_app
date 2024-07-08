from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/about')
def about():
    return 'Nice to meet ya all..'

if __name__ == '__main__':

   app.run()