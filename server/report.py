from flask import Blueprint, current_app, jsonify, request
from datetime import datetime, timezone
import json
import os

report_api = Blueprint("report_api", __name__)


def summarize_toggle_totals(seen_metrics):
    totals = {}

    for metric_batches in seen_metrics.values():
        if not isinstance(metric_batches, list):
            raise ValueError("Metrics batches must be a list.")

        for metric_entry in metric_batches:
            if not isinstance(metric_entry, dict):
                raise ValueError("Each metric entry must be an object.")

            bucket = metric_entry.get("bucket")
            if bucket is None:
                continue
            if not isinstance(bucket, dict):
                raise ValueError("Metric entry bucket must be an object.")

            toggles = bucket.get("toggles")
            if toggles is None:
                continue
            if not isinstance(toggles, dict):
                raise ValueError("Metric bucket toggles must be an object.")

            for toggle_name, toggle_counts in toggles.items():
                if not isinstance(toggle_counts, dict):
                    raise ValueError("Toggle counts must be an object.")
                yes_count = int(toggle_counts.get("yes", 0))
                no_count = int(toggle_counts.get("no", 0))
                variants = toggle_counts.get("variants", {})
                if variants is not None and not isinstance(variants, dict):
                    raise ValueError("Toggle variants must be an object.")

                if toggle_name not in totals:
                    totals[toggle_name] = {"yes": 0, "no": 0, "variants": {}}
                totals[toggle_name]["yes"] += yes_count
                totals[toggle_name]["no"] += no_count
                for variant_name, variant_count in variants.items():
                    if variant_name not in totals[toggle_name]["variants"]:
                        totals[toggle_name]["variants"][variant_name] = 0
                    totals[toggle_name]["variants"][variant_name] += int(variant_count)

    return totals


def build_expected_results_map(tests_data):
    expected = {}
    for test in tests_data:
        test_id = test.get("id") or test.get("name") or "unknown"
        for index, step in enumerate(test.get("steps", [])):
            if "expectedResult" in step:
                expected[(test_id, index)] = {
                    "op": step.get("op"),
                    "toggleName": step.get("toggleName"),
                    "expectedResult": step["expectedResult"],
                }
    return expected


def build_actual_results_map(report_body):
    results = report_body.get("results", []) if isinstance(report_body, dict) else []
    actual = {}
    for entry in results:
        test_id = entry.get("testId")
        step_index = entry.get("stepIndex")
        if test_id is None or step_index is None:
            raise ValueError("Each reported result must include testId and stepIndex.")
        actual[(test_id, int(step_index))] = {
            "op": entry.get("op"),
            "toggleName": entry.get("toggleName"),
            "result": entry.get("result"),
        }
    return actual


def build_operation_results_assertion(tests_data, report_body):
    expected_map = build_expected_results_map(tests_data)
    if not expected_map:
        return {
            "configured": False,
            "pass": True,
            "details": "No step expectedResult values configured.",
        }

    actual_map = build_actual_results_map(report_body)
    mismatches = []

    for key, expected in expected_map.items():
        actual = actual_map.get(key)
        if actual is None:
            raise ValueError(
                f"Harness bug: missing actual result for testId={key[0]} stepIndex={key[1]}."
            )
        if actual.get("op") != expected["op"]:
            raise ValueError(
                "Harness bug: op mismatch "
                f"for testId={key[0]} stepIndex={key[1]} "
                f"expected={expected['op']} actual={actual.get('op')}."
            )
        if actual.get("toggleName") != expected["toggleName"]:
            raise ValueError(
                "Harness bug: toggleName mismatch "
                f"for testId={key[0]} stepIndex={key[1]} "
                f"expected={expected['toggleName']} actual={actual.get('toggleName')}."
            )
        if actual.get("result") != expected["expectedResult"]:
            mismatches.append(
                {
                    "testId": key[0],
                    "stepIndex": key[1],
                    "reason": "result mismatch",
                    "expected": expected["expectedResult"],
                    "actual": actual.get("result"),
                }
            )

    return {
        "configured": True,
        "pass": len(mismatches) == 0,
        "mismatches": mismatches,
        "expectedCount": len(expected_map),
    }


def build_assertions(expected_data, actual_toggle_totals):
    expected_toggle_totals = expected_data.get("metricsToggleTotals", {})
    if not expected_toggle_totals:
        return {
            "configured": False,
            "pass": True,
            "details": "No expected.metricsToggleTotals configured.",
        }

    assertion_pass = actual_toggle_totals == expected_toggle_totals
    return {
        "configured": True,
        "pass": assertion_pass,
        "expected": expected_toggle_totals,
        "actual": actual_toggle_totals,
    }


def persist_reports(store, run_id, sdk, output_dir, report_body):
    os.makedirs(output_dir, exist_ok=True)
    date_tag = datetime.now(timezone.utc).strftime("%Y%m%d")
    destination_path = os.path.join(output_dir, f"{run_id}-{sdk}-{date_tag}.json")
    actual_toggle_totals = summarize_toggle_totals(store.seen_metrics)
    assertions = {
        "metricsToggleTotals": build_assertions(store.expected_data or {}, actual_toggle_totals),
        "operationResults": build_operation_results_assertion(store.tests_data or [], report_body),
    }
    payload = {
        "runId": run_id,
        "sdk": sdk,
        "date": date_tag,
        "reports": store.seen_reports.get(run_id, []),
        "metrics": store.seen_metrics,
        "metricsToggleTotals": actual_toggle_totals,
        "registrations": store.seen_registrations,
        "assertions": assertions,
    }
    with open(destination_path, "w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2)
    return assertions


@report_api.route("/api/report/ingest", methods=["POST"])
def ingest_report():
    store = current_app.config["PUPPY_STORE"]
    run_id = request.headers.get("X-Run-Id", store.run_id)
    body = request.get_json()
    if run_id is None:
        return jsonify({"error": "Missing run id"}), 400
    sdk = body.get("meta", {}).get("sdk") if isinstance(body, dict) else None
    if not isinstance(sdk, str) or not sdk.strip():
        return jsonify({"error": "Missing meta.sdk in report payload"}), 400
    store.add_batch_to(store.seen_reports, body, run_id)
    try:
        assertions = persist_reports(
            store,
            run_id,
            sdk.strip(),
            current_app.config["REPORT_OUTPUT_DIR"],
            body,
        )
    except Exception as error:
        return jsonify({"error": f"Failed to persist report: {error}"}), 500
    return (
        jsonify(
            {
                "message": "Report received successfully",
                "assertions": assertions,
            }
        ),
        200,
    )


@report_api.route("/api/report/ingest/<run_id>")
def get_report(run_id):
    store = current_app.config["PUPPY_STORE"]
    return jsonify(store.seen_reports.get(run_id, [])), 200
