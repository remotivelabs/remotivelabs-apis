"""
remotiveLabs Python API for remotiveBroker.
See `version` below.

Use sub module: `remotivelabs.broker.sync`.
"""

# SPDX-FileCopyrightText: 2022-present remotiveLabs <support@remotivelabs.com>
#
# SPDX-License-Identifier: Apache-2.0

from .__about__ import __version__
import logging

log = logging.getLogger("com.remotivelabs")
log.addHandler(logging.NullHandler())

version = __version__
"""Library version"""
