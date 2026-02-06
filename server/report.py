from flask import Blueprint, jsonify, request, current_app

report_api = Blueprint("report_api", __name__)


@report_api.route("/api/report/ingest", methods=["POST"])
def ingest_report():
    run_id = request.headers.get("X-Run-Id", "default")
    body = request.get_json()
    store = current_app.config["PUPPY_STORE"]
    store.add_batch_to(store.seen_reports, body, run_id)
    return jsonify({"message": "Report received successfully"}), 200


@report_api.route("/api/report/ingest/<run_id>")
def get_report(run_id):
    store = current_app.config["PUPPY_STORE"]
    return jsonify(store.seen_reports.get(run_id, [])), 200
