import os
import json

# Define the path to the urls.json file
URLS_FILE = os.path.join(os.path.dirname(__file__), '..', 'urls.json')

def _load_urls():
    if not os.path.exists(URLS_FILE):
        return []
    with open(URLS_FILE, 'r') as file:
        return json.load(file)

def _save_urls(urls):
    with open(URLS_FILE, 'w') as file:
        json.dump(urls, file)

def get_all_urls():
    return _load_urls()

def add_url(url):
    urls = _load_urls()
    if url not in urls:
        urls.append(url)
        _save_urls(urls)
