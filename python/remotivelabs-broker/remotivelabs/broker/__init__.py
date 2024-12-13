"""
RemotiveLabs Python API for RemotiveBroker.

This API uses protobuffer and gRPC stubs directly, available in the submodules:
- `remotivelabs.broker.common_pb2`.
- `remotivelabs.broker.common_pb2_grpc`.
- `remotivelabs.broker.diagnostics_api_pb2`.
- `remotivelabs.broker.diagnostics_api_pb2_grpc`.
- `remotivelabs.broker.network_api_pb2`.
- `remotivelabs.broker.network_api_pb2_grpc`.
- `remotivelabs.broker.system_api_pb2`.
- `remotivelabs.broker.system_api_pb2_grpc`.
- `remotivelabs.broker.traffic_api_pb2`.
- `remotivelabs.broker.traffic_api_pb2_grpc`.

In addition to return codes, this package uses logging to convey operational
status. Logging is done to the namespace "remotivelabs.broker".


```python
# Disable logging for this package:
logging.getLogger("remotivelabs.broker").propagate = False
```
"""

# SPDX-FileCopyrightText: 2022-present remotiveLabs <support@remotivelabs.com>
#
# SPDX-License-Identifier: Apache-2.0
from .__about__ import __version__
from ._log import configure_logging
from .generated.sync import (
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

version: str = __version__
"""Library version"""

configure_logging()
