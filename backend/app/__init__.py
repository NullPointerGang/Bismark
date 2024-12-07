from flask import Flask
from .routes.index import index_bp
from .routes.download import download_bp
from .routes.error import error_bp
# from .routes.auth import ...
# from .routes.user import ...

def create_app():
    app = Flask(__name__, 
                template_folder='../../frontend/main/',
                static_folder='../../frontend/static/'
            )
    app.register_blueprint(index_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(error_bp)
    return app
