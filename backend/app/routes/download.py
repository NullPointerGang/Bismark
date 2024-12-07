import logging
from typing import Literal
from flask import Blueprint, jsonify, request, Response
from app.utils.download import YouTubeDownloader

download_bp = Blueprint('download', __name__)

download_youtube = YouTubeDownloader()

@download_bp.route('/download', methods=['POST'])
def download() -> tuple[Response, Literal[400]] | tuple[Response, Literal[200]] | tuple[Response, Literal[500]] | None:
    request_data = request.get_json()
    url = request_data.get('url')
    format_type = request_data.get('format')
    if not url or not format_type:
        return jsonify({'error': 'Invalid request data'}), 400
    try:
        file_path = download_youtube.download(url, format_type)
        if file_path:
            return jsonify({'filePath': file_path}), 200
        else:
            return jsonify({'error': 'Download failed'}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'error': 'Internal server error'}), 500