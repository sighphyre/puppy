import json


SUPPORTED_OPS = {"isEnabled", "getVariant", "sleep"}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_test_run(data):
    _require(isinstance(data, dict), "Test run must be a JSON object.")

    meta = data.get("meta")
    _require(isinstance(meta, dict), "Test run requires a 'meta' object.")
    run_id = meta.get("runId")
    _require(isinstance(run_id, str) and run_id.strip(), "Test run requires meta.runId.")

    client_features = data.get("clientFeatures")
    _require(
        isinstance(client_features, dict),
        "Test run requires a 'clientFeatures' object.",
    )

    tests = data.get("tests")
    _require(isinstance(tests, list) and len(tests) > 0, "Test run requires non-empty 'tests'.")

    for test in tests:
        _require(isinstance(test, dict), "Each test must be an object.")
        steps = test.get("steps")
        _require(
            isinstance(steps, list) and len(steps) > 0,
            "Each test requires non-empty 'steps'.",
        )
        for step in steps:
            _require(isinstance(step, dict), "Each step must be an object.")
            op = step.get("op")
            _require(op in SUPPORTED_OPS, f"Unsupported op '{op}'.")
            if op in {"isEnabled", "getVariant"}:
                _require(
                    isinstance(step.get("toggleName"), str) and step["toggleName"].strip(),
                    f"Step op '{op}' requires a non-empty toggleName.",
                )
                _require(
                    isinstance(step.get("context"), dict),
                    f"Step op '{op}' requires a context object.",
                )
            if "expectedResult" in step:
                expected_result = step["expectedResult"]
                if op == "isEnabled":
                    _require(
                        isinstance(expected_result, bool),
                        "isEnabled expectedResult must be a boolean.",
                    )
                elif op == "getVariant":
                    _require(
                        isinstance(expected_result, dict),
                        "getVariant expectedResult must be an object.",
                    )
                    _require(
                        isinstance(expected_result.get("name"), str) and expected_result["name"].strip(),
                        "getVariant expectedResult.name must be a non-empty string.",
                    )
                    _require(
                        isinstance(expected_result.get("enabled"), bool),
                        "getVariant expectedResult.enabled must be a boolean.",
                    )
                    payload = expected_result.get("payload")
                    _require(
                        payload is None or isinstance(payload, dict),
                        "getVariant expectedResult.payload must be an object or null.",
                    )

    expected = data.get("expected", {})
    _require(isinstance(expected, dict), "Test run 'expected' must be an object when provided.")
    expected_toggle_totals = expected.get("metricsToggleTotals", {})
    _require(
        isinstance(expected_toggle_totals, dict),
        "expected.metricsToggleTotals must be an object when provided.",
    )
    for toggle_name, toggle_counts in expected_toggle_totals.items():
        _require(
            isinstance(toggle_name, str) and toggle_name.strip(),
            "expected.metricsToggleTotals keys must be non-empty strings.",
        )
        _require(
            isinstance(toggle_counts, dict),
            "Each expected.metricsToggleTotals entry must be an object.",
        )
        _require(
            isinstance(toggle_counts.get("yes"), int),
            "Each expected.metricsToggleTotals entry requires integer 'yes'.",
        )
        _require(
            isinstance(toggle_counts.get("no"), int),
            "Each expected.metricsToggleTotals entry requires integer 'no'.",
        )
        variants = toggle_counts.get("variants", {})
        _require(
            isinstance(variants, dict),
            "Each expected.metricsToggleTotals variants value must be an object.",
        )
        for variant_name, variant_count in variants.items():
            _require(
                isinstance(variant_name, str) and variant_name.strip(),
                "Variant names in expected.metricsToggleTotals must be non-empty strings.",
            )
            _require(
                isinstance(variant_count, int),
                "Variant counts in expected.metricsToggleTotals must be integers.",
            )

    return {
        "meta": meta,
        "clientFeatures": client_features,
        "tests": tests,
        "expected": expected,
    }


def load_test_run(path):
    with open(path, "r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    return validate_test_run(payload)
