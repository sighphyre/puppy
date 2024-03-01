#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_json_file>"
    exit 1
fi

FILE="$1"

URL="http://localhost:4242/state/"

if [ ! -f "$FILE" ]; then
    echo "Error: File not found."
    exit 1
fi

curl -X POST -H "Content-Type: application/json" -d @"$FILE" $URL
