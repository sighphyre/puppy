docker build -f Dockerfile-Reporter -t puppy-reporter .

docker run --user $(id -u):$(id -g) -v ./:/app puppy-reporter