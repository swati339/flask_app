from flask import Blueprint, request, jsonify, current_app, session
from app.tasks import process_url
import uuid
from rq import Queue
from rq.job import Job
import redis
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return  ('Welcome to the Flask App')

@bp.route('/submit', methods=['GET'])
def submit_url():
    user_id = session.get('user_id')
    url = request.args.get('url')
    if not user_id or not url:
        return jsonify({'message': 'User ID or URL not provided'}), 400

    job_id = f"{user_id}:{uuid.uuid5(uuid.NAMESPACE_URL, url)}"
    try:
        job = current_app.task_queue.enqueue(process_url, url, job_id=job_id)
        return jsonify({'message': 'URL submitted successfully!', 'job_id': job_id})
    except redis.RedisError as e:
        logging.error(f"Redis error: {e}")
        return jsonify({'message': 'Failed to submit URL'}), 500

@bp.route('/urls', methods=['GET'])
def user_urls():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not provided'}), 400

    user_key = f"user:{user_id}:urls"
    try:
        urls = current_app.redis.hkeys(user_key)
        urls = [url.decode('utf-8') for url in urls]
        return jsonify({'urls': urls})
    except redis.RedisError as e:
        logging.error(f"Redis error: {e}")
        return jsonify({'message': 'Failed to retrieve URLs'}), 500

@bp.route('/task_status', methods=['GET'])
def task_status():
    user_id = session.get('user_id')
    url = request.args.get('url')
    if not user_id or not url:
        return jsonify({'message': 'User ID or URL not provided'}), 400

    job_id = f"{user_id}:{uuid.uuid5(uuid.NAMESPACE_URL, url)}"
    try:
        job = Job.fetch(job_id, connection=current_app.redis)
        status = job.get_status()
        result = job.result if job.is_finished else None
        return jsonify({'job_id': job_id, 'status': status, 'result': result})
    except redis.RedisError as e:
        logging.error(f"Redis error: {e}")
        return jsonify({'message': 'Failed to retrieve task status'}), 500
    except Exception as e:
        logging.error(f"Error fetching job: {e}")
        return jsonify({'message': 'Failed to retrieve task status'}), 500
