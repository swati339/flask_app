from flask import Flask, request, jsonify
from .celery import celery
from .tasks import scrape_url
from .urls_store import get_all_urls, add_url

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    @app.route('/')
    def home():
        return "Hello World!"

    @app.route('/scrape')
    def scrape():
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Add URL to the list
        add_url(url)

        # Enqueue the scraping task
        job = scrape_url.apply_async(args=[url])
        return jsonify({"message": f"Scraping URL: {url}", "job_id": job.id})

    @app.route('/urls')
    def list_urls():
        urls = get_all_urls()
        return jsonify({"urls": urls})

    return app
