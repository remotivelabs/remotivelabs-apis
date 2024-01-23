#!/bin/bash

set -e

# Generates code from proto files, builds package and generates documentation

docker build -t remotivelabs/python-api-build-image -f docker/Dockerfile .

ARGS="-it"

if [ "${NO_TTY}" == "true" ]; then
    ARGS="-i"
fi


docker run \
    -u $(id -u):$(id -g) \
    -v $(pwd)/../../:/app  \
    -e "protofile=*.proto"  \
    -w /app  \
    ${ARGS} remotivelabs/python-api-build-image
