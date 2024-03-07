#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-directory-containing-index.json>"
    exit 1
fi

DIRECTORY_PATH=$1
INDEX_FILE="${DIRECTORY_PATH}/index.json"

if [ ! -f "$INDEX_FILE" ]; then
    echo "Index file not found at $INDEX_FILE"
    exit 1
fi

cat "$INDEX_FILE" | jq -r '.[]' | while read -r filename; do
    FILE_PATH="${DIRECTORY_PATH}${filename}"

    if [ ! -f "$FILE_PATH" ]; then
        echo "File not found: $FILE_PATH"
        continue
    fi

    echo "Processing $FILE_PATH"
    cat $FILE_PATH | jq "{tests: .tests}" > "split-spec/tests-${filename}"
    cat $FILE_PATH | jq ".state" > "split-spec/features-${filename}"


    ./hydrate.sh "split-spec/features-${filename}"

    languages=("node" "python" "ruby" "php" "java" "dotnet" "go")

    for lang in "${languages[@]}"; do
        ./run.sh "$lang" "split-spec/tests-${filename}" &
    done

    wait
done
