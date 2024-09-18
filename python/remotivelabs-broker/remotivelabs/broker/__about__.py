# SPDX-FileCopyrightText: 2022-present remotiveLabs <support@remotivelabs.com>
#
# SPDX-License-Identifier: Apache-2.0
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("remotivelabs-broker")
except PackageNotFoundError:
    __version__ = "unknown"
