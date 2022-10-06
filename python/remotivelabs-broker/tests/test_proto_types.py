import google.protobuf
import remotivelabs.broker.sync as br

# Tests

def test_empty():
    e = br.common_pb2.Empty
    assert is_protobuf_type(e)

def is_protobuf_type(obj):
    return isinstance(obj, google.protobuf.pyext.cpp_message.GeneratedProtocolMessageType)

