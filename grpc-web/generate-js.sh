#!/bin/bash

OUTPUT=./generated-js
TMP=./build

rm -rf $TMP
mkdir $TMP

rm -rf $OUTPUT
mkdir $OUTPUT

# Generate js + typescript stubs
docker run  \
  -v $(pwd)/../protos:/protofile \
  -v $(pwd)/$TMP:/output \
  -e "grpc_web_import_style=commonjs" \
  -e "protofile=*.proto" remotivelabs/grpc-web-generator

# Disable eslint on each js file
(cd $TMP && \
for filename in *.js; do
  echo "Adding /* eslint-disable */ to $filename"
  printf "/* eslint-disable */\n" | cat - $filename > "../$OUTPUT/$filename"
done )