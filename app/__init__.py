#This file initializes your Flask app and sets up Swagger and Marshmallow.

from flask import Flask
from flasgger import Swagger
from app.middleware import SimpleMiddleware

def create_app():
    app = Flask(__name__)

    # Initialize Swagger
    swagger = Swagger(app, template={
        "info": {
            "title": "Flask Learning API",
            "description": "A demo API with modular structure, Swagger docs, and validation",
            "version": "1.0.0"
        }
    })

    # Register middleware
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)

    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
