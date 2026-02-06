from flask import Flask
import logging

from .state import InMemoryState, state_api
from .unleash_client import unleash_client_api
from .edge import edge_api
from .report import report_api


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    app.config["PUPPY_STORE"] = InMemoryState()

    app.register_blueprint(state_api)
    app.register_blueprint(unleash_client_api)
    app.register_blueprint(edge_api)
    app.register_blueprint(report_api)

    return app
