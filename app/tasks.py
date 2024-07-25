import requests
from bs4 import BeautifulSoup
from flask import current_app
from .celery_utils import create_celery

celery = create_celery(current_app)

@celery.task(name='app.tasks.scrape_url')
def scrape_url(user_id, url):
    print(f"Scraping URL: {url} for user: {user_id}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    print(f"Scraped title: {title}")

    # Ensure Redis storage
    redis_key = f'user:{user_id}:urls'
    print(f"Adding URL to Redis: {url}")
    current_app.redis.rpush(redis_key, url)
    
    # Verify Redis storage
    urls = current_app.redis.lrange(redis_key, 0, -1)
    print(f"Stored URLs in Redis: {[url.decode('utf-8') for url in urls]}")
    
    return title
