#!/bin/bash

OUTPUT=./generated-ts
TMP=./build

rm -rf $TMP
mkdir -p $TMP

rm -rf $OUTPUT
mkdir -p $OUTPUT

# Generate js + typescript stubs
docker run  \
  -v $(pwd)/../protos:/protofile \
  -v $(pwd)/$TMP:/output \
  -e "grpc_web_import_style=commonjs+dts" \
  -e "protofile=*.proto" remotivelabs/grpc-web-generator

# Disable eslint on each js file
(cd $TMP && \
for filename in *.js; do
  echo "Adding /* eslint-disable */ to $filename"
  printf "/* eslint-disable */\n" | cat - $filename > "../$OUTPUT/$filename"
done )

cp $TMP/*.ts $OUTPUT
