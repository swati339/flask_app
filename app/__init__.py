from flask import Flask
from redis import Redis
from .celery_utils import create_celery

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.celery = create_celery(app)

    from .routes import init_routes
    init_routes(app)

    return app
