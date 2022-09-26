import google.protobuf
import remotivelabs.broker.sync as br
import pytest

# Warning these tests require a RemotiveBroker up and running
# server address:
_SERVER_URL = 'http://127.0.0.1:50051'
_SERVER_APIKEY = 'offline'


class Connection:
    def __init__(self):
        self.channel = br.create_channel(_SERVER_URL, _SERVER_APIKEY)
        self.network_stub = br.network_api_pb2_grpc.NetworkServiceStub(self.channel)
        self.system_stub = br.system_api_pb2_grpc.SystemServiceStub(self.channel)

# Setup broker with predefined settings
@pytest.fixture
def broker_connection():
    return Connection()

# Setup broker configured for testing
@pytest.fixture
def broker_configured(broker_connection):
    br.upload_folder(broker_connection.system_stub, "tests/configuration_udp")
    br.reload_configuration(broker_connection.system_stub)
    return broker_connection

@pytest.mark.server
def test_check_license(broker_connection):
    br.check_license(broker_connection.system_stub)

@pytest.mark.server
def test_meta_fields(broker_configured):
    sc = br.SignalCreator(broker_configured.system_stub)
    meta_speed = sc.get_meta('Speed', 'ecu_A')
    parent_frame = sc.frame_by_signal('Speed', 'ecu_A')
    assert parent_frame.name == 'PropulsionFrame'
    meta_parent = sc.get_meta(parent_frame.name, 'ecu_A')

    assert meta_speed.getDescription() == "Current velocity"
    assert meta_speed.getMax() == 90.0
    assert meta_speed.getMin() == 0
    assert meta_speed.getUnit() == "km/h"
    assert meta_speed.getSize() == 16
    assert meta_speed.getIsRaw() == False
    assert meta_parent.getIsRaw() == True
    assert meta_speed.getFactor() == 1.0
    assert meta_speed.getOffset() == 0.0
    assert meta_speed.getSenders() == ['ECUA']
    assert meta_parent.getSenders() == ['ECUA']
    assert meta_speed.getReceivers() == ['ReceiverA', 'ReceiverB']
    assert meta_parent.getCycleTime() == 42.0 # Cycle time is in parent frame
    assert meta_speed.getStartValue() == 2.0

def test_min_max(broker_configured):
    sc = br.SignalCreator(broker_configured.system_stub)

    # Works
    sc.signal_with_payload('Speed', 'ecu_A', ('double', 45.0))
    sc.signal_with_payload('Speed', 'ecu_A', ('double', 0.0))
    sc.signal_with_payload('Speed', 'ecu_A', ('double', 90.0))

    # Try to publing a value below mininum, API prevents this
    with pytest.raises(ValueError):
        sc.signal_with_payload('Speed', 'ecu_A', ('double', -1.0))

    # Try to publing a value above maximum
    with pytest.raises(ValueError):
        sc.signal_with_payload('Speed', 'ecu_A', ('double', 91.0))

