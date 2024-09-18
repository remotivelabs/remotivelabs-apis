from remotivelabs.broker.sync.client import Client


def test_client_initialization():
    client = Client()
    assert client.client_id == "broker_client"


def test_client_custom_id():
    client = Client("custom_client")
    assert client.client_id == "custom_client"
