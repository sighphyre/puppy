from flask import Flask
import logging

from .state import InMemoryState, state_api
from .unleash_client import unleash_client_api
from .edge import edge_api
from .report import report_api
from .tests import tests_api


def create_app(test_run) -> Flask:
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    store = InMemoryState()
    store.features_data = test_run["clientFeatures"]
    store.tests_data = test_run["tests"]
    store.run_meta = test_run["meta"]
    store.run_id = test_run["meta"]["runId"]

    app.config["PUPPY_STORE"] = store

    app.register_blueprint(state_api)
    app.register_blueprint(unleash_client_api)
    app.register_blueprint(edge_api)
    app.register_blueprint(report_api)
    app.register_blueprint(tests_api)

    return app
