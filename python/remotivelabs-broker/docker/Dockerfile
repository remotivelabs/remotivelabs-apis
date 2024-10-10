FROM python:3.10-slim

ENV protofile=*.proto \
  # python config
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip config
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry config
  POETRY_VERSION=1.8 \
  POETRY_VIRTUALENVS_IN_PROJECT=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# See https://python-poetry.org/docs/#ci-recommendations
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry self add 'poethepoet[poetry_plugin]'

# install the protobuf compiler
COPY --chmod=0755 docker/download_protoc.sh /tmp/download_protoc.sh
RUN /tmp/download_protoc.sh

# ... and the documentation plugin for protobuf compiler
COPY --chmod=0755 docker/download_protoc_gen_doc.sh /tmp/download_protoc_gen_doc.sh
RUN /tmp/download_protoc_gen_doc.sh

# Set up build script and entrypoint. It is possible to customize arguments to it using CMD or from command line
COPY --chmod=755 docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY --chmod=755 docker/build.sh /usr/local/bin/build.sh

VOLUME /app
WORKDIR /app

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
