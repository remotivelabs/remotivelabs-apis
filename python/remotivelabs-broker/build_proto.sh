#!/bin/sh -e

OUT=remotivelabs/broker/generated/sync/

# protoc -I ../../proto ../../proto/*.proto --python_out=$OUT --grpc_python_out=$OUT
# python3 -m grpc_tools.protoc --python_out=helloworld --grpc_python_out=helloworld --pyi_out=helloworld -I ../protos ../protos/helloworld.proto

# TODO - Get from dockerhub once we know that this works properly on all platforms
docker build -t remotivelabs/grpcio-tools-protobuf-3.19.2 .

docker run  \
  --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd)/../../protos:/protofile \
  -v $(pwd)/$OUT:/output \
  -e "protofile=*.proto" \
  remotivelabs/grpcio-tools-protobuf-3.19.2

#python3  -m grpc_tools.protoc -I ../../protos ../../protos/*.proto --python_out=$OUT --grpc_python_out=$OUT
python3 misc/fix_import_statements.py

echo "Successfully generated python stubs"
