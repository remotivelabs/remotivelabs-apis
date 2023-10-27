# Make sure we are on same or lower version of protoc than we
# This Dockerfile ensures that we are using libprotoc 3.19.2
# but this is is determined by the version of grpcio-tools

FROM rvolosatovs/protoc:3.3.0

RUN apk add --no-cache python3 py3-pip  build-base linux-headers
RUN apk add --no-cache python3-dev

RUN pip3 install grpcio-tools==1.44.0

VOLUME /protofile
ENV protofile=echo.proto
VOLUME /ouput

ENTRYPOINT []

CMD python3  -m grpc_tools.protoc \
 -I /protofile \
 --python_out=/output \
 --grpc_python_out=/output \
 /protofile/$protofile
