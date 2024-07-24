from celery import Celery

def create_celery_app():
    celery = Celery(
        'flask_app',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    celery.conf.update(
        result_backend='redis://localhost:6379/0'
    )
    return celery

celery = create_celery_app()
