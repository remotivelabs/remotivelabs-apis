FROM ubuntu:20.04 AS builder

ARG MAKEFLAGS=-j8

RUN apt-get update && apt-get install -y \
  automake \
  build-essential \
  git \
  libtool \
  make

RUN git clone https://github.com/grpc/grpc-web /github/grpc-web

WORKDIR /github/grpc-web

RUN git checkout tags/1.2.1

## Install gRPC and protobuf

RUN ./scripts/init_submodules.sh

RUN cd third_party/grpc && make && make install

RUN cd third_party/grpc/third_party/protobuf && make install

## Install all the gRPC-web plugin

RUN make install-plugin

FROM ubuntu:20.04

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include

## Create the gRPC client
ENV import_style=commonjs,binary
ENV grpc_web_import_style=commonjs+dts
ENV mode=grpcwebtext
VOLUME /protofile
ENV protofile=echo.proto
VOLUME /output
#ENV output=/protofile/generated

#protoc  --js_out=import_style=commonjs,binary:. --grpc-web_out=import_style=typescript,mode=grpcweb:.


CMD find /protofile -type f -name "*.proto" -exec protoc \
  -I=/protofile \
  {} \
  --js_out=import_style=$import_style:/output \
  --grpc-web_out=import_style=$grpc_web_import_style,mode=$mode:/output \;


