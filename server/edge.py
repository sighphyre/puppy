from flask import Blueprint, jsonify, request

edge_api = Blueprint("edge_api", __name__)


def make_edge_token(token: str):
    environment = token.split(".")[0].split(":")[1]
    return {
        "token": token,
        "type": "CLIENT",
        "environment": environment,
        "projects": ["*"],
    }


@edge_api.route("/api/client/edge-licensing/heartbeat", methods=["POST"])
def license_heartbeat():
    return jsonify({"edgeLicenseState": "Valid"}), 200


@edge_api.route("/edge/validate", methods=["POST"])
def validate():
    body = request.get_json()
    all_tokens = [make_edge_token(token) for token in body.get("tokens", [])]
    response = {
        "tokens": all_tokens,
    }

    # If Edge is asking us if a token is valid, then for our purposes it is.
    return jsonify(response), 200
