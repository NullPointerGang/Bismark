from flask import Blueprint, jsonify, request, url_for, send_file
import logging
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
            download_url = url_for('download.download_file', file_path=file, _external=True)
            return jsonify({'file_url': download_url, 'title': title, 'thumbnail': thumbnail}), 200
        else:
            return jsonify({'error': 'Download failed'}), 400
    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@download_bp.route('/download/file', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path')
    if file_path:
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404
