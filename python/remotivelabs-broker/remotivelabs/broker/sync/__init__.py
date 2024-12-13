"""
Synchronous connection to the remotiveBroker API.

Create a connection with the method `remotivelabs.broker.sync.create_channel`.

For an example on how to use these we recommend looking at the samples for this library.
Which is available at the repository remotiveLabs samples:

Link: <https://github.com/remotivelabs/remotivelabs-samples/tree/main/python>.
"""

# Prefer import from root module. We keep this import for backwards compatibility.
from ..generated.sync import (
    common_pb2,  # noqa: F401
    common_pb2_grpc,  # noqa: F401
    diagnostics_api_pb2,  # noqa: F401
    diagnostics_api_pb2_grpc,  # noqa: F401
    network_api_pb2,  # noqa: F401
    network_api_pb2_grpc,  # noqa: F401
    system_api_pb2,  # noqa: F401
    system_api_pb2_grpc,  # noqa: F401
    traffic_api_pb2,  # noqa: F401
    traffic_api_pb2_grpc,  # noqa: F401
)
from .client import (
    BrokerException,
    Client,
    SignalIdentifier,
    SignalsInFrame,
    SignalValue,
)
from .helper import (
    act_on_scripted_signal,
    act_on_signal,
    check_license,
    create_channel,
    download_file,
    generate_data,
    get_sha256,
    printer,
    publish_signals,
    reload_configuration,
    upload_file,
    upload_folder,
)
from .signalcreator import SignalCreator

__all__ = [
    "SignalsInFrame",
    "Client",
    "SignalIdentifier",
    "SignalValue",
    "SignalCreator",
    "BrokerException",
    "create_channel",
    "publish_signals",
    "printer",
    "get_sha256",
    "generate_data",
    "upload_file",
    "download_file",
    "upload_folder",
    "reload_configuration",
    "check_license",
    "act_on_signal",
    "act_on_scripted_signal",
    "common_pb2",
    "common_pb2_grpc",
    "diagnostics_api_pb2",
    "diagnostics_api_pb2_grpc",
    "network_api_pb2",
    "network_api_pb2_grpc",
    "system_api_pb2",
    "system_api_pb2_grpc",
    "traffic_api_pb2",
    "traffic_api_pb2_grpc",
]
