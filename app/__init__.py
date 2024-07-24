from flask import Flask, request
from .celery import celery
from .tasks import scrape_url

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    @app.route('/')
    def home():
        return "Hello World!"

    @app.route('/scrape', methods=['GET'])
    def scrape():
        url = request.args.get('url')
        if not url:
            return "No URL provided.", 400

        # Enqueue the scraping task
        job = scrape_url.apply_async(args=[url])
        return f"Scraping URL: {url}, job id: {job.id}"

    return app
