"""
remotiveLabs Python API for remotiveBroker.
See `version` below.

In addition to return codes, this package uses logging to convey operational
status. Logging is done to the name space "com.remotivelabs.broker".

As a user, enable basic logging in your application with:

```python
logging.basicConfig()
```

Disable logging for this package:

```python
logging.getLogger("com.remotivelabs.broker").propagate = False
```

Use sub module: `remotivelabs.broker.sync`.
"""

# SPDX-FileCopyrightText: 2022-present remotiveLabs <support@remotivelabs.com>
#
# SPDX-License-Identifier: Apache-2.0

from .__about__ import __version__
import logging

log: logging.Logger = logging.getLogger("com.remotivelabs.broker")
"""Package logging interface"""

log.addHandler(logging.NullHandler())

version: str = __version__
"""Library version"""
