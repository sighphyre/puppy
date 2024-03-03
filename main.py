from flask import Flask, jsonify, request, make_response
import json
import hashlib


app = Flask(__name__)

features_data = None

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242)
