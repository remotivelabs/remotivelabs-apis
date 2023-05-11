#!/bin/bash

#
# Build kotlin stubs for grpc-api
# The build.gradle.kts file depends on beeing invoked from this otherwise
# the proto files cannot be found
#

rm -rf tmp
mkdir tmp
cp -a ../protos tmp
find ./tmp/protos -name "*.proto" | xargs sed -i  -e 's/package base/package com.remotivelabs.apis/g'
docker run --rm -u gradle -v "$PWD":/home/gradle/project -w /home/gradle/project gradle gradle clean build --no-daemon
rm -rf tmp