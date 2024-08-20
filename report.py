import argparse
from dataclasses import dataclass
import os
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader


@dataclass
class TestEntry:
    test_name: str
    result: bool
    toggle_name: str


@dataclass
class TestDataSet:
    name: str
    dataset: list[TestEntry]


@dataclass
class ReportMatrix:
    columns_headers: list[str]
    row_headers: list[str]
    matrix: list[list[bool]]


def build_html_report(report_matrix):

    def mark_color(value):
        if value:
            return "background-color: green"
        else:
            return "background-color: blue"

    def highlight_unequal(row):
        if row.nunique() > 1:
            return [mark_color(value) for value in row]
        else:
            return [""] * len(row)

    df = pd.DataFrame(
        report_matrix.matrix,
        columns=report_matrix.columns_headers,
        index=report_matrix.row_headers,
    )
    styled_df = df.style.apply(highlight_unequal, axis=1)

    html_table = styled_df.to_html()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    html_content = template.render(data_table=html_table)

    with open("report.html", "w") as f:
        f.write(html_content)


def make_report_matrix(
    known_tests: set[str], test_data: list[TestDataSet]
) -> ReportMatrix:
    matrix = []
    ordered_tests = sorted(list(known_tests))

    for test_name in ordered_tests:
        row = []
        for sdk_test_output in test_data:
            test_dict = {entry.test_name: entry for entry in sdk_test_output.dataset}
            row.append(test_dict[test_name].result)
        matrix.append(row)

    column_headers = [test_set.name for test_set in test_data]
    return ReportMatrix(
        columns_headers=column_headers, row_headers=ordered_tests, matrix=matrix
    )


def read_dataset(file_name, directory) -> TestDataSet:
    with open(directory + "/" + file_name, "r") as f:
        data = json.load(f)

    test_entries = []
    for test_name, test_data in data.items():
        test_entries.append(
            TestEntry(test_name, test_data["result"], test_data["toggleName"])
        )

    return TestDataSet(file_name, test_entries)


def get_last_touched_report(path):
    directories = [f.path for f in os.scandir(path) if f.is_dir()]
    if not directories:
        raise FileNotFoundError("No directories found in the specified path.")
    last_modified_dir = max(directories, key=os.path.getmtime)
    return last_modified_dir


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate an HTML report from a dataset."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="Path to the dataset file, e.g. ./testruns/e47671",
    )

    args = parser.parse_args()

    if args.dataset:
        dataset_path = args.dataset
    else:
        default_path = "./testruns"
        dataset_path = get_last_touched_report(default_path)
        print(
            f"No dataset provided. Defaulting to the last modified directory: {dataset_path}"
        )

    test_run_directories = [f.path for f in os.scandir(dataset_path) if f.is_dir()]

    for directory in test_run_directories:
        known_tests = set()
        test_data_sets = [
            read_dataset(f.name, directory)
            for f in os.scandir(directory)
            if f.is_file() and f.name != "test_file.json"
        ]

        for test_data_set in test_data_sets:
            known_tests.update([test.test_name for test in test_data_set.dataset])

        report_matrix = make_report_matrix(known_tests, test_data_sets)

        build_html_report(report_matrix)
