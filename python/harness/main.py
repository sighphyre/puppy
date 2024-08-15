from dataclasses import dataclass
from UnleashClient import UnleashClient
from UnleashClient.cache import FileCache
import json
import logging
import os
from os import path
import sys
import uuid
import time


def load_tests():
    return json.loads(sys.stdin.read())


if os.environ.get("PUPPY_DEBUG") == "false":
    logging.disable(logging.CRITICAL + 1)

unleash_api_url = os.getenv('UNLEASH_API_URL', 'http://localhost:4242/api/')

unleash_client = UnleashClient(
    url=unleash_api_url,
    app_name="python-test-harness",
    instance_id="pytest_%s" % uuid.uuid4(),
    environment="default",
    metrics_interval=1,
    custom_headers={'Authorization': 'python:test.token'},
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
        "result": result,
        "toggleName": toggle_name,
    }


time.sleep(2)
print(json.dumps(output, indent=4))
