from dataclasses import dataclass
from UnleashClient import UnleashClient
from UnleashClient.cache import FileCache
import json
import logging
import os
from os import path
import sys
import uuid


def load_tests():
    return json.loads(sys.stdin.read())


if os.environ.get("SEIDR_DEBUG") == "false":
    logging.disable(logging.CRITICAL + 1)

unleash_client = UnleashClient(
    url="http://seidr-core:4242/api/",
    app_name="python-test-harness",
    instance_id="pytest_%s" % uuid.uuid4(),
    disable_metrics=True,
    disable_registration=True,
    environment="default",
)

unleash_client.initialize_client()

tests = load_tests()["tests"]

output = {}
for test in tests:
    context = test["context"]
    description = test["description"]
    toggle_name = test["toggleName"]
    expected_result = test["expectedResult"]

    result = unleash_client.is_enabled(toggle_name, context)

    output[description] = {
        "toggleName": toggle_name,
        "result": result,
        "context": context,
    }

print(json.dumps(output, indent=4))
