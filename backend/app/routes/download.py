import logging
from flask import Blueprint, jsonify, request, Response, send_file
from app.utils.download import YouTubeDownloader

download_bp = Blueprint('download', __name__)

download_youtube = YouTubeDownloader()

@download_bp.route('/download', methods=['POST'])
def download():
    request_data = request.get_json()
    url = request_data.get('url')
    format_type = request_data.get('format')
    if not url or not format_type:
        return jsonify({'error': 'Invalid request data'}), 400
    try:
        file, title, thumbnail = download_youtube.download(url, format_type)
        if file:
            return send_file(file, as_attachment=True, download_name="file_name.mp4", mimetype='video/mp4'), jsonify({'title': title, 'thumbnail': thumbnail})
        else:
            return jsonify({'error': 'Download failed'}), 400
    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        return jsonify({'error': 'Internal server error'}), 500