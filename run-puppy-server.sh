#!/bin/bash

network_name="puppy-network"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_test_run_json>"
    exit 1
fi

test_run_path="$1"
if [ ! -f "$test_run_path" ]; then
    echo "Error: Test run file not found at $test_run_path"
    exit 1
fi

absolute_test_run_path="$(realpath "$test_run_path")"


create_network() {
    local network_name=$1
    if ! docker network ls | grep -q $network_name; then
        echo "Creating Docker network: $network_name"
        docker network create $network_name
    else
        echo "Docker network $network_name already exists"
    fi
}

create_network $network_name

docker build --no-cache -f Dockerfile-Puppy -t puppy-core .

docker rm -f puppy-core && docker run \
    -p 4242:4242 \
    --name puppy-core \
    --network puppy-network \
    -v "$absolute_test_run_path:/app/test-run.json:ro" \
    puppy-core \
    python main.py --test-run /app/test-run.json
