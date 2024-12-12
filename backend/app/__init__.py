import os
from dotenv import load_dotenv
from flask import Flask
from flask_session import Session
from .routes.index import index_bp
from .routes.download import download_bp
from .routes.error import error_bp
from .routes.other import other_bp


# from .routes.user import ...

load_dotenv()

def create_app():
    """
    Создает и конфигурирует экземпляр Flask приложения.

    Эта функция настраивает приложение Flask, загружает переменные окружения,
    настраивает сессии и регистрирует маршруты (blueprints).

    Returns:
        Flask: Экземпляр приложения Flask, готовый к запуску.
    """
    app = Flask(__name__, 
                template_folder='../../frontend/main/',
                static_folder='../../frontend/static/'
            )
    
    app.register_blueprint(index_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(other_bp)
    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = os.getenv('SECRET_KEY')
    
    Session(app)

    return app
