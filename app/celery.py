from celery import Celery

def make_celery():
    celery = Celery(
        'flask_app',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    return celery

# Create the Celery instance
celery = make_celery()
