from flask import Blueprint, render_template


index_bp = Blueprint('main', __name__)

@index_bp.route('/', methods=['GET'])
def home():
    """
    Обработчик маршрута для главной страницы.

    Возвращает HTML-шаблон для главной страницы сайта.

    Returns:
        str: Сгенерированный HTML-контент страницы 'index.html'.
    """
    return render_template('index.html')