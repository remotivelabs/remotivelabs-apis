#!/bin/bash
#
# Build the remotivelabs-broker python library together with its documentation.
#
# We use grpc-tools to generate the python stubs for the protobuf definition in protos/ dir,
# and then package the python library using hatch. Documentation is generated for python, protobuf
# and json-schema.
#
set -e

# We need to set HOME (or XDG_*) to a directory where we have write permissions, so that hatch can store config files there
HOME=/tmp

PROJECT_DIR=/app/python/remotivelabs-broker

PROTO_IN=/app/protos
PROTO_STUBS_OUT=$PROJECT_DIR/remotivelabs/broker/generated/sync

SCHEMA_IN=/app/schemas

BUILD_DIR=$PROJECT_DIR/dist

DOCS_DIR=$PROJECT_DIR/dist/doc/
PY_DOCS=$DOCS_DIR/python
PROTO_DOCS=$DOCS_DIR/protos
JSON_DOCS=$DOCS_DIR/json

function generate_protobuf_files() {
  mkdir -p "${PROTO_STUBS_OUT}"

  python3 -m grpc_tools.protoc \
    -I $PROTO_IN \
    --python_out=$PROTO_STUBS_OUT \
    --grpc_python_out=$PROTO_STUBS_OUT \
    --mypy_out=$PROTO_STUBS_OUT \
    --mypy_grpc_out=$PROTO_STUBS_OUT \
    $PROTO_IN/*.proto

  # TODO: fix this
  python3 $PROJECT_DIR/misc/fix_import_statements.py
}

function build_python_library() {
  hatch build
}

function generate_python_docs() {
    mkdir -p $PY_DOCS

    # Install wheel in order for pdoc to run properly so docs can be built
    dist_wheel=$(ls -AU dist/*.whl | head -1)
    echo "dist = $dist_wheel"
    pip3 install $dist_wheel

    pdoc \
        --favicon https://releases.remotivelabs.com/favicon.ico \
        --logo https://releases.remotivelabs.com/remotive-labs-logo-neg.png \
        --no-show-source \
        -t misc/theme \
        -o $PY_DOCS \
        $PROJECT_DIR/remotivelabs
}

function generate_proto_docs() {
  mkdir -p $PROTO_DOCS

  PROTO_FILES="$PROTO_IN/common.proto $PROTO_IN/network_api.proto $PROTO_IN/system_api.proto $PROTO_IN/traffic_api.proto"
  protoc -I $PROTO_IN --doc_out=$PROTO_DOCS --doc_opt=html,index.html $PROTO_FILES
}

function generate_json() {
    mkdir -p $JSON_DOCS

    generate-schema-doc $SCHEMA_IN/metadb.json $JSON_DOCS
    generate-schema-doc $SCHEMA_IN/interfaces_schema.json $JSON_DOCS
    generate-schema-doc $SCHEMA_IN/scripted_db.json $JSON_DOCS
}

# run build
cd $PROJECT_DIR
rm -rf $BUILD_DIR

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
