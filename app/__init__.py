from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    from app import models  # Import models here

    # Swagger UI
    SWAGGER_URL = '/api/v1/docs'
    API_URL = '/static/swagger.json'
    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be served at {SWAGGER_URL}/dist/
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Travel Company API"
        },
    )

    app.register_blueprint(swaggerui_blueprint)

    return app