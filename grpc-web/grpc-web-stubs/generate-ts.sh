#!/bin/bash

OUTPUT=./generated-ts
TMP=./build

rm -rf $TMP
mkdir -p $TMP

rm -rf $OUTPUT
mkdir -p $OUTPUT

# Generate js + typescript stubs
docker run  \
  -v $(pwd)/../../protos:/protofile \
  -v $(pwd)/$TMP:/output \
  -e "grpc_web_import_style=commonjs+dts" \
  -e "protofile=*.proto" remotivelabs/grpc-web-generator


# Copy files and disable eslint on each js file
(
find $TMP -type f | while read -r filepath; do
  relative_path="${filepath#$TMP/}"
  echo "Processing $relative_path"
  output_path="$OUTPUT/$relative_path"
  mkdir -p "$(dirname "$output_path")"
  if [[ $filepath == *.js ]]; then
    printf "/* eslint-disable */\n" | cat - "$filepath" > "$output_path"
  else
    cp "$filepath" "$output_path"
  fi
done )

npx tsc

echo "Stubs successfully generated and npm package ready to publish"