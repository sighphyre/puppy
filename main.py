from flask import Flask, jsonify, request, make_response
import json
import hashlib
import logging


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

features_data = None
seen_metrics = {}
seen_registrations = {}

def add_batch_to(container, data, key):
    if data is None:
        return
    if key not in container:
        container[key] = []
    container[key].append(data)

def add_metrics(data, key):
    add_batch_to(seen_metrics, data, key)

def add_registration(data, key):
    add_batch_to(seen_registrations, data, key)

def generate_etag(data):
    content_hash = hashlib.sha1(json.dumps(data).encode()).hexdigest()
    content_length = len(json.dumps(data))
    return f'W/"{content_length}-{content_hash}"'

@app.route("/state/", methods=["POST"])
def update_state():
    global features_data
    try:
        features_data = request.get_json()
        return jsonify({"message": "State updated successfully"}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400


@app.route("/api/client/features")
def features():
    if features_data is not None:
        etag = generate_etag(features_data)
        response = make_response(jsonify(features_data))
        response.headers['ETag'] = etag
        return response
    else:
        return jsonify({"error": "No data available"}), 404


@app.route("/api/client/register", methods=["POST"])
def register():
    # get auth header headers
    api_key = request.headers.get("Authorization")
    print(api_key)
    return jsonify({"message": "Registered successfully"}), 200

@app.route("/api/client/metrics", methods=["POST"])
def metrics():
    # raise Exception()
    api_key = request.headers.get("Authorization")
    body = request.get_json()
    app.logger.info(f"stuff {str(api_key)}")
    # add_metrics(request.get_json(), api_key)
    app.logger.info(f"Metrics received: {body}")
    return jsonify({"message": "Metrics received successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242)
