from flask import request, jsonify, current_app

def init_routes(app):

    @app.route('/scrape', methods=['GET'])
    def scrape():
        url = request.args.get('url')
        user_id = request.args.get('user_id')
        if not url or not user_id:
            return jsonify({'error': 'Missing URL or user_id parameter'}), 400

        result = current_app.celery.send_task('app.tasks.scrape_url', args=[user_id, url])
        return jsonify({'task_id': result.id}), 202

    @app.route('/urls', methods=['GET'])
    def list_urls():
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Missing user_id parameter'}), 400

        if request.method == 'POST':
            url = request.form.get('url')
            if not url:
                return jsonify({'error': 'Missing URL parameter'}), 400
            current_app.redis.rpush(f'user:{user_id}:urls', url)
            return jsonify({'status': 'URL added'}), 201

        urls = current_app.redis.lrange(f'user:{user_id}:urls', 0, -1)
        urls = [url.decode('utf-8') for url in urls]
        return jsonify({"urls": urls})
