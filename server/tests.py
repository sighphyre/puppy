from flask import Blueprint, current_app, jsonify

tests_api = Blueprint("tests_api", __name__)


@tests_api.route("/api/tests", methods=["GET"])
def get_tests():
    store = current_app.config["PUPPY_STORE"]
    if store.tests_data is None:
        return jsonify({"error": "No tests available"}), 404

    return (
        jsonify(
            {
                "meta": store.run_meta,
                "tests": store.tests_data,
            }
        ),
        200,
    )
