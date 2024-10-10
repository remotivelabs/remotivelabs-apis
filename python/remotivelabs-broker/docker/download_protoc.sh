#!/bin/bash
#
# Downloads correct protoc compiler for correct platform during docker build
#
PROTOC_VERSION="28.2"
BASE_URL="https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}"

ARCH=$(uname -m)
OS=$(uname -s)

case "${OS}-${ARCH}" in
    "Linux-x86_64")
        URL="${BASE_URL}-linux-x86_64.zip"
        ;;
    "Linux-aarch64")
        URL="${BASE_URL}-linux-aarch_64.zip"
        ;;
    "Darwin-arm64")
        URL="${BASE_URL}-osx-aarch_64.zip"
        ;;
    *)
        echo "Unsupported platform: ${OS}-${ARCH}"
        exit 1
        ;;
esac

# Create a temporary directory and set up cleanup
TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "Downloading protoc compiler for ${OS}-${ARCH} from: $URL"
wget "$URL" -O "$TMP_DIR/proto-compiler.zip"

unzip "$TMP_DIR/proto-compiler.zip" -d "$TMP_DIR"
mv "$TMP_DIR/bin/protoc" /usr/bin/protoc
chmod +x /usr/bin/protoc

echo "protoc compiler installed successfully!"
