#!/bin/bash
#
# Downloads the correct documentation generator plugin for the Google Protocol Buffers compiler
#
PROTOC_GEN_DOC_VERSION="1.5.1"
BASE_URL="https://github.com/pseudomuto/protoc-gen-doc/releases/download/v${PROTOC_GEN_DOC_VERSION}/protoc-gen-doc_${PROTOC_GEN_DOC_VERSION}"

ARCH=$(uname -m)
OS=$(uname -s)

case "${OS}-${ARCH}" in
    "Linux-x86_64")
        URL="${BASE_URL}_linux_amd64.tar.gz"
        ;;
    "Linux-aarch64")
        URL="${BASE_URL}_linux_arm64.tar.gz"
        ;;
    "Darwin-arm64")
        URL="${BASE_URL}_darwin_arm64.tar.gz"
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

echo "Downloading protoc-gen-doc for ${OS}-${ARCH} from: $URL"
wget "$URL" -O "$TMP_DIR/protoc-gen-doc.tar.gz"

tar -zxf "$TMP_DIR/protoc-gen-doc.tar.gz" -C "$TMP_DIR"
mv "$TMP_DIR/protoc-gen-doc" /usr/bin/protoc-gen-doc
chmod +x /usr/bin/protoc-gen-doc

echo "protoc compiler documentation plugin installed successfully!"
