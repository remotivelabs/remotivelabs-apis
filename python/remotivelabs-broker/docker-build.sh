#!/bin/bash
#
# Generates code from proto files, builds package and generates documentation
#
set -e

SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
TAG=remotivelabs/python-api-build-image

docker build -t "${TAG}" -f "${SCRIPT_DIR}/docker/Dockerfile" "${SCRIPT_DIR}"

# set args to allow build to run in non-tty shells
ARGS="-it"
[ "${NO_TTY}" == "true" ] && ARGS="-i"

docker run \
    -u "$(id -u):$(id -g)" \
    -v "${SCRIPT_DIR}/../../:/app"  \
    -e "protofile=*.proto"  \
    -w /app  \
    "${ARGS}" "${TAG}"
