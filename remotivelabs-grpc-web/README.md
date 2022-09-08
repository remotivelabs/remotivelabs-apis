# WEB-GRPC Stubs

# Usage

```
npm install remotivelabs-grpc-web
```

# Build from source 

## Build grpc-web-generator

```
docker build -t remotivelabs/grpc-web-generator .
```

## Generate stubs

From this directory

```sh
mkdir generated 

docker run  \
  -v $(pwd)/../protos:/protofile \
  -v $(pwd)/generated:/output \
  -e "protofile=*.proto" remotivelabs/grpc-web-generator
```
