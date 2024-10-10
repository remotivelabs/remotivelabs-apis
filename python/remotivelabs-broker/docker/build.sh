#!/bin/bash
#
# Build the remotivelabs-broker python library together with its documentation.
#
# We use grpc-tools to generate the python stubs for the protobuf definition in protos/ dir,
# and then package the python library using hatch. Documentation is generated for python, protobuf
# and json-schema.
#
set -e

PROJECT_DIR=/app/python/remotivelabs-broker

PROTO_IN=/app/protos
PROTO_STUBS_OUT=$PROJECT_DIR/remotivelabs/broker/generated/sync

SCHEMA_IN=/app/schemas

BUILD_DIR=$PROJECT_DIR/dist

DOCS_DIR=$PROJECT_DIR/dist/doc
PY_DOCS=$DOCS_DIR/python
PROTO_DOCS=$DOCS_DIR/protos
JSON_DOCS=$DOCS_DIR/json

function setup_build_env() {
  cd $PROJECT_DIR
  rm -rf $BUILD_DIR

  # Make sure we dont mess up any .venv already present in the mounted volume
  export POETRY_VIRTUALENVS_IN_PROJECT=false
  poetry install
}

function generate_protobuf_files() {
  mkdir -p "${PROTO_STUBS_OUT}"

  poetry run python -m grpc_tools.protoc \
    --proto_path=$PROTO_IN \
    --python_out=$PROTO_STUBS_OUT \
    --grpc_python_out=$PROTO_STUBS_OUT \
    --pyi_out=$PROTO_STUBS_OUT \
    $PROTO_IN/*.proto

  # Note: protobuf compiler does not support generating relative or custom absolute imports for python. Use a script to do this manually...
  poetry run python $PROJECT_DIR/misc/fix_import_statements.py
}

function build_python_library() {
  poetry build
}

function generate_python_docs() {
    mkdir -p $PY_DOCS

    poetry run pdoc \
        --favicon https://releases.remotivelabs.com/favicon.ico \
        --logo https://releases.remotivelabs.com/remotive-labs-logo-neg.png \
        --no-show-source \
        -t misc/theme \
        -o $PY_DOCS \
        $PROJECT_DIR/remotivelabs
}

# TODO: Move away from python lib
# TODO: Investigate the possibility to use grpcio-tools proto compiler instead of this custom one.
# See e.g. protoc-docs-plugin on pypi
function generate_proto_docs() {
  mkdir -p $PROTO_DOCS

  PROTO_FILES="$PROTO_IN/common.proto $PROTO_IN/network_api.proto $PROTO_IN/system_api.proto $PROTO_IN/traffic_api.proto"
  protoc -I $PROTO_IN --doc_out=$PROTO_DOCS --doc_opt=html,index.html $PROTO_FILES
}

# TODO: Move away from python lib
function generate_json() {
    mkdir -p $JSON_DOCS

    poetry run generate-schema-doc $SCHEMA_IN/metadb.json $JSON_DOCS
    poetry run generate-schema-doc $SCHEMA_IN/interfaces_schema.json $JSON_DOCS
    poetry run generate-schema-doc $SCHEMA_IN/scripted_db.json $JSON_DOCS
}

echo -e "\n######################"
echo "Installing python dependencies in ${PROJECT_DIR}"
echo "######################"
setup_build_env

echo -e "\n######################"
echo "Generating protobuf files to ${PROTO_STUBS_OUT}"
echo "######################"
generate_protobuf_files

echo -e "\n######################"
echo "Building python library in ${BUILD_DIR}"
echo "######################"
build_python_library

echo -e "\n######################"
echo "Generating pydocs in ${PY_DOCS}"
echo "######################"
generate_python_docs

echo -e "\n######################"
echo "Generating protobuf docs to ${PROTO_DOCS}"
echo "######################"
generate_proto_docs

echo -e "\n######################"
echo "Generating json schema docs to ${JSON_DOCS}"
echo "######################"
generate_json
