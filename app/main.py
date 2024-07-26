from flask import Blueprint, request, jsonify, current_app
from app.tasks import process_url

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask App'})

@bp.route('/submit', methods=['GET'])
def submit_url():
    user_id = request.args.get('user_id')
    url = request.args.get('url')
    if user_id and url:
        user_key = f"user:{user_id}:urls"
        job = current_app.task_queue.enqueue(process_url, url)
        current_app.redis.lpush(user_key, url)
        return jsonify({'message': 'URL submitted successfully!', 'url': url, 'job_id': job.get_id()})
    return jsonify({'message': 'User ID or URL not provided'}), 400

@bp.route('/urls', methods=['GET'])
def user_urls():
    user_id = request.args.get('user_id')
    if user_id:
        user_key = f"user:{user_id}:urls"
        urls = current_app.redis.lrange(user_key, 0, -1)
        urls = [url.decode('utf-8') for url in urls]
        return jsonify({'urls': urls})
    return jsonify({'message': 'User ID not provided'}), 400
