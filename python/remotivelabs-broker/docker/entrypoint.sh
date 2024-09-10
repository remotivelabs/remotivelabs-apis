#!/bin/bash

set -e

HOME=/app/python/remotivelabs-broker
STUBS_OUTPUT=$HOME/remotivelabs/broker/generated/sync
mkdir -p "${STUBS_OUTPUT}"

#1.1 Generate stubs
python3  -m grpc_tools.protoc \
 -I /app/protos \
 --python_out=$STUBS_OUTPUT \
 --grpc_python_out=$STUBS_OUTPUT \
 --mypy_out=$STUBS_OUTPUT \
 --mypy_grpc_out=$STUBS_OUTPUT \
 /app/protos/*.proto

cd $HOME
#1.2 Fix those imports
python3 misc/fix_import_statements.py

rm -rf dist

# Build distribution wheel
hatch build

# Install wheel in order for pdoc to run properly so docs can be built
dist_wheel=$(ls -AU dist/*.whl | head -1)
echo "dist = $dist_wheel"
pip3 install $dist_wheel


# Build python documentation

mkdir -p dist/doc/
DOCS=$(realpath dist/doc)


function generate_python_docs() {
    PY_DOCS=$DOCS/python
    mkdir $PY_DOCS

    pdoc \
        --favicon https://releases.remotivelabs.com/favicon.ico \
        --logo https://releases.remotivelabs.com/remotive-labs-logo-neg.png \
        --no-show-source \
        -t misc/theme \
        -o $PY_DOCS \
        ./remotivelabs
}

function generate_proto_docs() {
  PROTO_DOCS=$DOCS/protos
  mkdir $PROTO_DOCS
  PROTO_FILES="common.proto network_api.proto system_api.proto traffic_api.proto"
  protoc --doc_out=$PROTO_DOCS --doc_opt=html,index.html $PROTO_FILES
}

function generate_json() {
    JSON_DOCS=$DOCS/json
    mkdir $JSON_DOCS
    # Generate
    generate-schema-doc metadb.json $JSON_DOCS
    generate-schema-doc interfaces_schema.json $JSON_DOCS
    generate-schema-doc scripted_db.json $JSON_DOCS
}

generate_python_docs
(cd /app/protos && generate_proto_docs)
(cd /app/schemas/ && generate_json)
