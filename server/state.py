from flask import Blueprint, current_app, jsonify, request
import json


class InMemoryState:
    def __init__(self):
        self.features_data = None
        self.tests_data = None
        self.run_meta = None
        self.run_id = None
        self.seen_metrics = {}
        self.seen_registrations = {}
        self.seen_reports = {}

    def add_batch_to(self, container, data, key):
        if data is None:
            return
        if key not in container:
            container[key] = []
        container[key].append(data)

state_api = Blueprint("state_api", __name__)


@state_api.route("/state/", methods=["POST"])
def update_state():
    store = current_app.config["PUPPY_STORE"]
    try:
        store.features_data = request.get_json()
        return jsonify({"message": "State updated successfully"}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
