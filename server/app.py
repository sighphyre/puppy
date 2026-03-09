from flask import Flask
import logging

from .state import InMemoryState, state_api
from .unleash_client import unleash_client_api
from .edge import edge_api
from .frontend import frontend_api
from .report import report_api
from .tests import tests_api


def create_app(test_run, report_output_dir) -> Flask:
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    store = InMemoryState()
    client_features = test_run["clientFeatures"]
    store.features_sequence = client_features if isinstance(client_features, list) else [client_features]
    store.features_data = store.features_sequence[0]
    store.features_request_count = 0
    store.tests_data = test_run["tests"]
    store.expected_data = test_run["expected"]
    store.run_meta = test_run["meta"]
    store.run_id = test_run["meta"]["runId"]

    app.config["PUPPY_STORE"] = store
    app.config["REPORT_OUTPUT_DIR"] = report_output_dir

    app.register_blueprint(state_api)
    app.register_blueprint(unleash_client_api)
    app.register_blueprint(edge_api)
    app.register_blueprint(frontend_api)
    app.register_blueprint(report_api)
    app.register_blueprint(tests_api)

    return app
