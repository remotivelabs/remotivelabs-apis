from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Iterator

import friendlywords as fw
import pytest


REQUIRED_ENV_VARS = ["REMOTIVE_CLOUD_PROJECT"]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--itests", action="store_true", default=False, help="Run integration tests against a cloud instance")


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "itests: run integration tests")

    # make sure all required env vars are set for integration tests if --itests is given
    if config.getoption("--itests"):
        missing_env_vars = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
        if missing_env_vars:
            raise ValueError(f"Missing required environment variables for integration tests: {', '.join(missing_env_vars)}")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """
    skip integration tests if --itests is not given

    See https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    """
    if config.getoption("--itests"):
        return

    skip_itests = pytest.mark.skip(reason="need --itests option to run")
    for item in items:
        if "itests" in item.keywords:
            item.add_marker(skip_itests)
