from rq import get_current_job
import requests

def process_url(url):
    job = get_current_job()
    try:
        response = requests.get(url)
        result = response.text[:200]  # Return the first 200 characters of the content
        job.meta['result'] = result
        job.save_meta()
        return result
    except Exception as e:
        job.meta['error'] = str(e)
        job.save_meta()
        return None

