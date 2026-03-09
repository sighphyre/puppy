from flask import Blueprint

frontend_api = Blueprint("frontend_api", __name__)


@frontend_api.route("/api/frontend", methods=["GET"])
def frontend():
    return "Hello world", 200
