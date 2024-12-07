import logging
from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)


@error_bp.app_errorhandler(Exception)
def handle_error(error):
    """Универсальная обработка ошибок."""
    error_code = getattr(error, 'code', 500)
    logging.error(f"Error: {error}, Code: {error_code}")
    
    return render_template('error.html', error_code=error_code, error_message=str(error)), error_code
