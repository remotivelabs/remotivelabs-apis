from __future__ import annotations

import logging

import pytest

import remotivelabs.broker as br
import remotivelabs.broker.sync as br_sync


class Connection:  # pylint: disable=too-few-public-methods
    def __init__(self, url: str, api_key: str | None = None):
        self.channel = br_sync.create_channel(url, api_key)
        self.system_stub = br.system_api_pb2_grpc.SystemServiceStub(self.channel)


@pytest.fixture(name="broker_connection")
def fixture_broker_connection(broker_url):
    return Connection(broker_url)


@pytest.fixture(name="broker_configured")
def fixture_broker_configured(broker_connection):
    br_sync.upload_folder(broker_connection.system_stub, "tests/fixtures/configs/udp")
    br_sync.reload_configuration(broker_connection.system_stub)
    return broker_connection


@pytest.mark.server
def test_check_license(broker_connection):
    br_sync.check_license(broker_connection.system_stub)


@pytest.mark.server
def test_meta_fields(broker_configured):
    sc = br_sync.SignalCreator(broker_configured.system_stub)
    meta_speed = sc.get_meta("Speed", "ecu_A")
    parent_frame = sc.frame_by_signal("Speed", "ecu_A")
    assert parent_frame.name == "PropulsionFrame"  # pylint: disable=no-member
    meta_parent = sc.get_meta(parent_frame.name, "ecu_A")  # pylint: disable=no-member

    assert meta_speed.getDescription() == "Current velocity"
    assert meta_speed.getMax() == 90.0
    assert meta_speed.getMin() == 0
    assert meta_speed.getUnit() == "km/h"
    assert meta_speed.getSize() == 16
    assert meta_speed.getIsRaw() is False
    assert meta_parent.getIsRaw() is True

    assert meta_speed.getFactor() == 1.0
    assert meta_speed.getOffset() == 0.0
    assert meta_speed.getSenders() == ["ECUA"]
    assert meta_parent.getSenders() == ["ECUA"]
    assert meta_speed.getReceivers() == ["ReceiverA", "ReceiverB"]
    assert meta_parent.getCycleTime() == 42.0  # Cycle time is in parent frame
    assert meta_speed.getStartValue() == 2.0


@pytest.mark.server
def test_min_max(broker_configured, caplog):
    sc = br_sync.SignalCreator(broker_configured.system_stub)

    # Works
    sc.signal_with_payload("Speed", "ecu_A", ("double", 45.0))
    sc.signal_with_payload("Speed", "ecu_A", ("double", 0.0))
    sc.signal_with_payload("Speed", "ecu_A", ("double", 90.0))

    # Catch warning logs
    caplog.clear()
    with caplog.at_level(logging.INFO):
        assert len(caplog.records) == 0

        # Publing a value below mininum
        sc.signal_with_payload("Speed", "ecu_A", ("double", -1.0))
        assert caplog.records[0].message == 'Value below minimum value of 0.0 for signal "Speed"'

        # Publing a value above maximum
        sc.signal_with_payload("Speed", "ecu_A", ("double", 91.0))
        assert caplog.records[1].message == 'Value above maximum value of 90.0 for signal "Speed"'

        assert len(caplog.records) == 2


@pytest.mark.server
def test_list_signals(broker_configured):
    namespace = br.common_pb2.NameSpace(name="ecu_A")  # pylint: disable=no-member
    signals = broker_configured.system_stub.ListSignals(namespace)
    assert len(signals.frame) == 5
