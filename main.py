from flask import Flask, jsonify, request
import json


app = Flask(__name__)

features_data = None


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
        return jsonify(features_data)
    else:
        return jsonify({"error": "No data available"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242)
