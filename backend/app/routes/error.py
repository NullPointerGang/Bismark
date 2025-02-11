import logging
from flask import Blueprint, render_template


error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(Exception)
def handle_error(error):
    """
    Универсальная обработка ошибок.

    Этот обработчик перехватывает все исключения, происходящие в приложении.
    Он логирует ошибку и возвращает страницу с ошибкой, отображая код ошибки и сообщение.

    Args:
        error (Exception): Исключение, которое было вызвано в приложении.

    Returns:
        tuple: Кортеж, содержащий:
            - str: Сгенерированный HTML-контент страницы ошибки.
            - int: Код ошибки (например, 500 для серверных ошибок).
    """
    error_code = getattr(error, 'code', 500)
    logging.error(f"Error: {error}, Code: {error_code}")
    
    return render_template('error.html', error_code=error_code, error_message=str(error)), error_code
