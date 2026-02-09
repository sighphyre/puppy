import argparse

from server import create_app
from server.test_run import load_test_run


def parse_args():
    parser = argparse.ArgumentParser(description="Run Puppy server with a test run definition.")
    parser.add_argument(
        "--test-run",
        required=True,
        help="Path to test run JSON file.",
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=4242, type=int)
    parser.add_argument(
        "--report-output-dir",
        default="./testruns/reports",
        help="Directory where ingested harness reports are persisted.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    test_run = load_test_run(args.test_run)
    app = create_app(test_run=test_run, report_output_dir=args.report_output_dir)
    app.run(host=args.host, port=args.port)
