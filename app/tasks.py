from app.celery import celery
import requests
from bs4 import BeautifulSoup

@celery.task
def scrape_url(url):
    """Function that scrapes the content of a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        print(f"Title of the page at {url}: {title}")
        return title
    else:
        print(f"Failed to retrieve the page at {url}. Status code: {response.status_code}")
        return None
