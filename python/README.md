# RemotiveLabs Broker API Python SDK

`remotivelabs-broker` - Python SDK for interacting with the RemotiveLabs Broker.

Published to PyPI on [https://pypi.org/project/remotivelabs-broker/](https://pypi.org/project/remotivelabs-broker/)

## Getting started

Prerequisites:

```bash
# Install poetry (and optionally poe plugin to simplify poetry command execution)
pipx install poetry
poetry self add 'poethepoet[poetry_plugin]'
```

Build and run:

```bash
cd python/remotivelabs-broker

# Install dependencies in a virtualenv
poetry install

# Build the library (output in dist/)
poetry build

# Check (test, lint, check types)
poetry poe check

# run standard test suite
poetry run pytest

# run tests against running broker
poetry run pytest -m server --broker <broker url>
```

If you need to (re)generate protobuf stubs, see [Building](#building).

## Building

Building the complete package, including protobuf stubs and documentation, is done using a docker container:

```bash
./python/remotivelabs-broker/docker-build.sh
```

## Versioning

Update the package version by editing the following `pyproject.toml` file.

Follow [Semantic versioning](https://semver.org/). Beta versions should be suffixed with `b*`, example `0.2.0b1`.

## Publishing

Published to PyPI on [https://pypi.org/project/remotivelabs-broker/](https://pypi.org/project/remotivelabs-broker/):

All RemotiveLabs libraries:
- share the same `remotivelabs` [namespace package](https://peps.python.org/pep-0420/).
- use the `remotivelabs-` prefix in the library name.
- are published with the [remotivelabs](https://pypi.org/user/remotivelabs/) user.

```bash
# Get token from Johan Rask
poetry config pypi-token.pypi <my-token>

# find username and password in less secret location
poetry publish
```
