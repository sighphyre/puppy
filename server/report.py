from flask import Blueprint, current_app, jsonify, request
import json
import os

report_api = Blueprint("report_api", __name__)


def persist_reports(store, run_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    destination_path = os.path.join(output_dir, f"{run_id}.json")
    payload = {
        "runId": run_id,
        "reports": store.seen_reports.get(run_id, []),
    }
    with open(destination_path, "w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2)


@report_api.route("/api/report/ingest", methods=["POST"])
def ingest_report():
    store = current_app.config["PUPPY_STORE"]
    run_id = request.headers.get("X-Run-Id", store.run_id)
    body = request.get_json()
    if run_id is None:
        return jsonify({"error": "Missing run id"}), 400
    store.add_batch_to(store.seen_reports, body, run_id)
    try:
        persist_reports(store, run_id, current_app.config["REPORT_OUTPUT_DIR"])
    except Exception as error:
        return jsonify({"error": f"Failed to persist report: {error}"}), 500
    return jsonify({"message": "Report received successfully"}), 200


@report_api.route("/api/report/ingest/<run_id>")
def get_report(run_id):
    store = current_app.config["PUPPY_STORE"]
    return jsonify(store.seen_reports.get(run_id, [])), 200
