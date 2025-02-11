import logging
from backend.app import create_app
from backend.config import HOST, PORT

if __name__ == "__main__":
    """
    Главная точка входа для запуска Flask-приложения.

    Создает экземпляр Flask-приложения с помощью функции create_app(), 
    а затем запускает сервер с включенным режимом отладки.

    """
    create_app().run(debug=True, host=HOST, port=PORT)
    logging.basicConfig(level=logging.DEBUG)