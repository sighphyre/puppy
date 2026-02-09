from flask import Blueprint, jsonify, request, current_app

report_api = Blueprint("report_api", __name__)


@report_api.route("/api/report/ingest", methods=["POST"])
def ingest_report():
    store = current_app.config["PUPPY_STORE"]
    run_id = request.headers.get("X-Run-Id", store.run_id)
    body = request.get_json()
    if run_id is None:
        return jsonify({"error": "Missing run id"}), 400
    store.add_batch_to(store.seen_reports, body, run_id)
    return jsonify({"message": "Report received successfully"}), 200


@report_api.route("/api/report/ingest/<run_id>")
def get_report(run_id):
    store = current_app.config["PUPPY_STORE"]
    return jsonify(store.seen_reports.get(run_id, [])), 200
