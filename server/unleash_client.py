from flask import Blueprint, current_app, jsonify, make_response, request
from datetime import datetime, timezone
import hashlib
import json

unleash_client_api = Blueprint("unleash_client_api", __name__)


def generate_etag(data):
    content_hash = hashlib.sha1(json.dumps(data).encode()).hexdigest()
    content_length = len(json.dumps(data))
    return f'W/"{content_length}-{content_hash}"'


@unleash_client_api.route("/api/client/features")
def features():
    store = current_app.config["PUPPY_STORE"]
    if store.features_data is None:
        return jsonify({"error": "No data available"}), 404

    etag = generate_etag(store.features_data)
    if_none_match = request.headers.get("If-None-Match")
    authorization = request.headers.get("Authorization")
    if if_none_match == etag:
        response = make_response("", 304)
    else:
        response = make_response(jsonify(store.features_data), 200)
    response.headers["ETag"] = etag

    store.add_features_poll_trace(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "authorization": authorization,
            "ifNoneMatch": if_none_match,
            "responseStatus": response.status_code,
            "responseEtag": etag,
        }
    )
    return response


@unleash_client_api.route("/api/client/register", methods=["POST"])
def register():
    api_key = request.headers.get("Authorization")
    current_app.logger.info(f"Registration received: {api_key}")
    store = current_app.config["PUPPY_STORE"]
    store.add_batch_to(store.seen_registrations, request.get_json(), api_key)
    return jsonify({"message": "Registered successfully"}), 200


@unleash_client_api.route("/api/client/metrics", methods=["POST"])
def metrics():
    api_key = request.headers.get("Authorization")
    body = request.get_json()
    current_app.logger.info(f"Metrics received: {body}")
    store = current_app.config["PUPPY_STORE"]
    store.add_batch_to(store.seen_metrics, body, api_key)
    return jsonify({"message": "Metrics received successfully"}), 200
