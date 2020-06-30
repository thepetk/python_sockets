import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


def create_app(**kwargs):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

logger = logging.getLogger('sockets_logger')
app.logger.handlers.extend(logger.handlers)

from app.routes import routes
