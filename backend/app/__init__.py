from flask import Flask
from .routes.index import index_bp

def create_app():
    app = Flask(__name__, 
                template_folder='../../frontend/main/',
                static_folder='../../frontend/static/'
            )
    app.register_blueprint(index_bp)
    return app
