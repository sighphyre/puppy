#!/bin/bash

run_container() {
    local language=$1
    local dockerfile="Dockerfile-${language^}"
    local tag="${language}-scaffold"
    local container_name="${language}-scaffold"

    if [ -f "$dockerfile" ]; then
        echo "Building $language container..."
        docker build -f $dockerfile -t $tag .

        if [ "${SEIDR_DEBUG:-true}" = "true" ]; then
            docker rm -f $container_name && cat context.json | docker run -i --name $container_name --network seidr-network $tag
            echo "Debug mode is on, to persist the run, rerun the env var SEIDR_DEBUG=false and run the script again."
        else
            echo "Debug mode is off, output will be written to output.txt"
            docker rm -f $container_name && cat context.json | docker run -i --name $container_name --network seidr-network $tag > output.txt
        fi
    else
        echo "Dockerfile for $language not found."
        exit 1
    fi
}

if [ $# -eq 0 ]; then
    echo "No language specified. Please provide a language as an argument."
    exit 1
fi

run_container $1
