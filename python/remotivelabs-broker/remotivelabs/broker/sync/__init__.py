"""
Synchronous connection to the remotiveBroker API.

Create a connection with the method `remotivelabs.broker.sync.create_channel`.

This API uses protobuffer and gRPC stubs directly. Which are availble in the submodules:
- `remotivelabs.broker.sync.common_pb2`.
- `remotivelabs.broker.sync.common_pb2_grpc`.
- `remotivelabs.broker.sync.diagnostics_api_pb2`.
- `remotivelabs.broker.sync.diagnostics_api_pb2_grpc`.
- `remotivelabs.broker.sync.functional_api_pb2`.
- `remotivelabs.broker.sync.functional_api_pb2_grpc`.
- `remotivelabs.broker.sync.network_api_pb2`.
- `remotivelabs.broker.sync.network_api_pb2_grpc`.
- `remotivelabs.broker.sync.system_api_pb2`.
- `remotivelabs.broker.sync.system_api_pb2_grpc`.
- `remotivelabs.broker.sync.traffic_api_pb2`.
- `remotivelabs.broker.sync.traffic_api_pb2_grpc`.

For an example on how to use these we recommend looking at the samples for this library. Which is available at the repository remotiveLabs samples:

Link: <https://github.com/remotivelabs/remotivelabs-samples/tree/main/python>.
"""

from ..generated.sync import common_pb2
from ..generated.sync import common_pb2_grpc
from ..generated.sync import diagnostics_api_pb2
from ..generated.sync import diagnostics_api_pb2_grpc
from ..generated.sync import functional_api_pb2
from ..generated.sync import functional_api_pb2_grpc
from ..generated.sync import network_api_pb2
from ..generated.sync import network_api_pb2_grpc
from ..generated.sync import system_api_pb2
from ..generated.sync import system_api_pb2_grpc
from ..generated.sync import traffic_api_pb2
from ..generated.sync import traffic_api_pb2_grpc

from .signalcreator import SignalCreator

from .helper import create_channel
from .helper import publish_signals
from .helper import printer
from .helper import get_sha256
from .helper import generate_data
from .helper import upload_file
from .helper import download_file
from .helper import upload_folder
from .helper import reload_configuration
from .helper import check_license
from .helper import act_on_signal

__all__ = [
    'create_channel',
    'publish_signals',
    'printer',
    'get_sha256',
    'generate_data',
    'upload_file',
    'download_file',
    'upload_folder',
    'reload_configuration',
    'check_license',
    'act_on_signal',
]
