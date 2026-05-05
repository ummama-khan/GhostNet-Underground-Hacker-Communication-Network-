import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .extensions import limiter 

# Load the secrets from the .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Plug the limiter into the app
    limiter.init_app(app)

    # ADD THIS LINE: Pull the secret key from the environment
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    from .presentation.auth_routes import auth_bp
    from .presentation.chat_routes import chat_bp
    from .presentation.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    return app