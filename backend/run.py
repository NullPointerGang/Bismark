import logging
from app import create_app


if __name__ == "__main__":
    """
    Главная точка входа для запуска Flask-приложения.

    Создает экземпляр Flask-приложения с помощью функции create_app(), 
    а затем запускает сервер на хосте '0.0.0.0' и порту 80 с включенным режимом отладки.

    Args:
        None

    Returns:
        None
    """
    create_app().run(debug=True, host='0.0.0.0', port=80)
    logging.basicConfig(level=logging.DEBUG)