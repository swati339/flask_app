from flask import Flask
from config import Config
import redis
from rq import Queue

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.redis = redis.StrictRedis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue(connection=app.redis)

    app.secret_key = app.config['SECRET_KEY']


    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
