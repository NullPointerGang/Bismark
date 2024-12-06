import logging
from flask import Blueprint

download_bp = Blueprint('download', __name__)

@download_bp.route('/download', methods=['GET'])
def download(url: str):
    logging.info(f'Download: {url}')
    # TODO: Download logic
    return ''