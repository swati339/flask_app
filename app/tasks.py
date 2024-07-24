import requests
from bs4 import BeautifulSoup
from .celery import celery

@celery.task
def scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.title.string if soup.title else 'No title found'
