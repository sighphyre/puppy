from flask import Flask, jsonify
import json
import sys

app = Flask(__name__)


@app.route("/api/client/features")
def features():
    try:
        with open("feature_toggles.json", "r") as file:
            data = json.load(file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242)
