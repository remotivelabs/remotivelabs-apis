#!/bin/sh

#
# Downloads correct protoc compiler for correct platform during docker build
#

mkdir /apps
mkdir /app
export ARCH=$(uname -p)

if [ "$ARCH" = "aarch64" ] ; then export ARCH=aarch_64 ; else export ARCH=x86_64  ; fi

(wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.2/protoc-3.19.2-linux-$ARCH.zip -O /tmp/proto-compiler.zip &&
cd tmp && unzip proto-compiler.zip && mv /tmp/bin/protoc /bin/protoc && chmod 777 /bin/protoc)