#!/bin/bash

network_name="seidr-network"


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

docker build --no-cache -f Dockerfile-Seidr -t seidr-core .

docker rm -f seidr-core && docker run -p 4242:4242 --name seidr-core --network seidr-network seidr-core