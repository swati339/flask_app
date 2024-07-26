from flask import Blueprint, request, jsonify, current_app,session
from app.tasks import process_url
import uuid
from rq import Queue
from rq.job import Job
import redis
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
     session['user_id'] = str(uuid.uuid4())
     return jsonify({'message': 'Welcome to the Flask App'})

@bp.route('/submit', methods=['GET'])
def submit_url():
    user_id = session.get('user_id')
    url = request.args.get('url')
    if user_id and url:
        user_key = f"user:{user_id}:urls"
        job = current_app.task_queue.enqueue(process_url, url)
        current_app.redis.hset(f"user:{user_id}:jobs", job.get_id(), 'pending')
        current_app.redis.lpush(user_key, url)
        return jsonify({'message': 'URL submitted successfully!', 'job_id': job.get_id()})
    return jsonify({'message': 'User ID or URL not provided'}), 400

@bp.route('/urls', methods=['GET'])
def user_urls():
    user_id = session.get('user_id')
    if user_id:
        user_key = f"user:{user_id}:urls"
        urls = current_app.redis.lrange(user_key, 0, -1)
        urls = [url.decode('utf-8') for url in urls]
        return jsonify({'urls': urls})
    return jsonify({'message': 'User ID not provided'}), 400

@bp.route('/task_status', methods=['GET'])
def task_status():
    user_id = session.get('user_id')
    job_id = request.args.get('job_id')
    if user_id and job_id:
        try:
            job = Job.fetch(job_id, connection=current_app.redis)
            status = job.get_status()
            result = job.result if job.is_finished else None
            current_app.redis.hset(f"user:{user_id}:jobs", job_id, status)
            return jsonify({'job_id': job_id, 'status': status, 'result': result})
        except redis.RedisError as e:
            logging.error(f"Redis error: {e}")
            return jsonify({'message': 'Failed to retrieve task status'}), 500
        except Exception as e:
            logging.error(f"Error fetching job: {e}")
            return jsonify({'message': 'Failed to retrieve task status'}), 500
    return jsonify({'message': 'User ID or Job ID not provided'}), 400

@bp.route('/tasks', methods=['GET'])
def all_tasks():
    user_id = session.get('user_id')
    if user_id:
        jobs = current_app.redis.hgetall(f"user:{user_id}:jobs")
        tasks = {job_id.decode('utf-8'): status.decode('utf-8') for job_id, status in jobs.items()}
        return jsonify({'tasks': tasks})
    return jsonify({'message': 'User ID not provided'}), 400
