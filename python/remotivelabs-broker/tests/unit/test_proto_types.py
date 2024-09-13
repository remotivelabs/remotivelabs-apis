import remotivelabs.broker as br


def test_create_empty_message():
    """Make sure we can instantiate a basic type"""
    _ = br.common_pb2.Empty
