# Make sure we are on same or lower version of protoc than we
# This Dockerfile ensures that we are using libprotoc 3.19.2
# but this is is determined by the version of grpcio-tools

FROM ubuntu:jammy


ARG URL_PROTOC_DOC=https://github.com/pseudomuto/protoc-gen-doc/releases/download/v1.5.1/protoc-gen-doc_1.5.1_linux_amd64.tar.gz
RUN apt-get update && apt-get install -y python3.11 python3-pip wget unzip
RUN pip install hatch json-schema-for-humans
RUN pip3 install grpcio-tools==1.44.0
RUN pip3 install hatch
RUN pip3 install pdoc
RUN pip3 install mypy-protobuf==3.3.0
COPY docker/download_protoc.sh .
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN sh download_protoc.sh


RUN wget ${URL_PROTOC_DOC} -O /tmp/protoc.tar.gz && \
        tar zxfv /tmp/protoc.tar.gz protoc-gen-doc && \
        mv protoc-gen-doc /usr/bin -v

VOLUME /app
ENV protofile=*.proto
VOLUME /ouput

CMD ["./python/remotivelabs-broker/docker/build-all-in-docker.sh"]
