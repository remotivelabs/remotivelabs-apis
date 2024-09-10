FROM ubuntu:22.04

ENV protofile=*.proto

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.11 \
        python3-pip \
        wget \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    grpcio-tools==1.44.0 \
    mypy-protobuf==3.3.0 \
    hatch==1.12.0 \
    pdoc==14.6.1 \
    json-schema-for-humans==1.0.2

# install the protobuf compiler
COPY --chmod=0755 docker/download_protoc.sh /tmp/download_protoc.sh
RUN /tmp/download_protoc.sh

# ... and the documentation plugin for protobuf compiler
COPY --chmod=0755 docker/download_protoc_gen_doc.sh /tmp/download_protoc_gen_doc.sh
RUN /tmp/download_protoc_gen_doc.sh

VOLUME /app
VOLUME /output

# Set up build script as entrypoint. It is possible to customize arguments to it using CMD or from command line
COPY --chmod=755 docker/entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
