import logging
from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    logging.error(error)
    return render_template('404.html'), 404

@error_bp.app_errorhandler(500)
def internal_error(error):
    logging.error(error)
    return render_template('500.html'), 500