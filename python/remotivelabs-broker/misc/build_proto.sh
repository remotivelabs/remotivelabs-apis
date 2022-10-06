#!/bin/sh -e

OUT=remotivelabs/broker/generated/sync/

# protoc -I ../../proto ../../proto/*.proto --python_out=$OUT --grpc_python_out=$OUT
# python3 -m grpc_tools.protoc --python_out=helloworld --grpc_python_out=helloworld --pyi_out=helloworld -I ../protos ../protos/helloworld.proto

python3 -m grpc_tools.protoc -I ../../protos ../../protos/*.proto --python_out=$OUT --grpc_python_out=$OUT
sed -i -E "s/^import \w+_pb2/from . \0/gm" $OUT/*.py

