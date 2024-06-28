#!/bin/bash


get_features_hash() {
    local features_url=$1
    curl -s "$features_url" | sha256sum | awk '{ print substr($1, 1, 6) }'
}

get_file_hash() {
    local file_path="$1"

    if [ ! -f "$file_path" ]; then
        echo "Error: File not found at $file_path"
        return 1
    fi

    sha256sum "$file_path" | awk '{ print substr($1, 1, length_var) }' length_var=6
}

run_container() {
    local language_tag=$1
    local test_file=$2
    local puppy_url="http://localhost:4242/api/client/features"

    local features_hash
    if ! features_hash=$(get_features_hash "$puppy_url"); then
        echo "Failed to get features from $puppy_url. Is Puppy running?."
        return 1
    fi

    local file_hash
    if ! file_hash=$(get_file_hash "$test_file"); then
        echo "Failed to get file hash for $test_file. Exiting."
        return 1
    fi
    local destination_path="testruns/$features_hash/$file_hash"

    mkdir -p "$destination_path"

    curl -s "$puppy_url" -o "testruns/$features_hash/client_features.json"
    cp "$test_file" "$destination_path/test_file.json"

    IFS=':' read -r language tag <<< "$language_tag"
    tag=${tag:-main} # Default to 'main' if no tag is provided, is this a good idea?

    local dockerfile="${language_tag}/Dockerfile"
    local image_tag="${language}-${tag}-scaffold"
    local container_name="${language}-${tag}-scaffold"

    if [ -f "$dockerfile" ]; then
        echo "Building $language container with tag $tag..."
        docker build --build-arg TAG=$tag -f $dockerfile -t $image_tag $language_tag

        local debug_mode=${PUPPY_DEBUG:-true}
        echo "Debug mode is set to $debug_mode."

        # Ugh I hate this, these two branches are so similar but I keep breaking it when I collapse them
        docker rm -f $container_name
        if [ "$debug_mode" = "true" ]; then
            cat "$test_file" | docker run -i -e PUPPY_DEBUG="$debug_mode" -e UNLEASH_API_URL="http://puppy-core:4242/api/" --name $container_name --network puppy-network $image_tag
        else
            cat "$test_file" | docker run -i -e PUPPY_DEBUG="$debug_mode" -e UNLEASH_API_URL="http://puppy-core:4242/api/" --name $container_name --network puppy-network $image_tag > ${destination_path}/${language}-${tag}-output.json
        fi
    else
        echo "Dockerfile for $language not found."
        exit 1
    fi
}

if [ $# -lt 2 ]; then
    echo "Insufficient arguments provided."
    echo "Usage: $0 <language[:tag]> <test_file>"
    exit 1
fi

run_container $1 $2
