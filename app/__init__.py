from flask import Flask
from config import params
import logging

_logger = logging.getLogger(__name__)


def _initialize_blueprints(application):
    """
    register blueprints
    """
    from app.views.api import api
    application.register_blueprint(api, url_prefix='/detectobot/v{0}'.format(params["version"]))


def create_app():
    """
    init app
    """
    application = Flask(__name__)

    _initialize_blueprints(application)

    return application
