#!/bin/bash

set -e

# Generates code from proto files, builds package and generates documentation

docker build -t remotivelabs/python-api-build-image -f docker/Dockerfile .

docker run \
    -u $(id -u):$(id -g) \
    -v $(pwd)/../../:/app  \
    -e "protofile=*.proto"  \
    -w /app  \
    -it remotivelabs/python-api-build-image