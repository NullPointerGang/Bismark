import os
import logging
from flask import Blueprint, jsonify, request, url_for, send_file
from app.utils.download import YouTubeDownloader

download_bp = Blueprint('download', __name__)

SAFE_DOWNLOAD_DIR = 'downloads'

download_youtube = YouTubeDownloader(SAFE_DOWNLOAD_DIR)

@download_bp.route('/download', methods=['POST'])
def download():
    request_data = request.get_json()
    url = request_data.get('url')
    format_id = request_data.get('format_id')
    print(url, format_id)
    if not url or not format_id:
        return jsonify({'error': 'Invalid request data'}), 400

    try:
        file = download_youtube.download(url, format_id)
        if file:
            download_url = url_for('download.download_file', file_path=file, _external=True)
            return jsonify({'file_url': download_url}), 200
        else:
            return jsonify({'error': 'Download failed'}), 400
    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@download_bp.route('/download/info', methods=['POST'])
def download_info():
    request_data = request.get_json()
    url = request_data.get('url')

    if not url:
        return jsonify({'error': 'Invalid request data'}), 400

    try:
        title, thumbnail, quality_list = download_youtube.get_info(url)
        if title:
            return jsonify({'title': title, 'thumbnail': thumbnail, 'quality_list': quality_list}), 200
        else:
            return jsonify({'error': 'Failed to get video information'}), 400
    except Exception as e:
        logging.error(f"Error occurred during getting video information: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@download_bp.route('/download/file', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path')
    
    if not file_path:
        return jsonify({'error': 'File path not provided'}), 400
    
    if not file_path.startswith(SAFE_DOWNLOAD_DIR):
        return jsonify({'error': 'Access to this file is not allowed'}), 403
    
    file_path = os.path.abspath(file_path.replace('+', ' '))
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        allowed_extensions = ['.mp3', '.mp4', '.m4a']
        if not any(file_path.endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'File type not allowed'}), 403
        

        return send_file(file_path, as_attachment=True)

    else:
        return jsonify({'error': 'File not found'}), 404