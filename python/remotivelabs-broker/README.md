# RemotiveLabs Broker

[![PyPI - Version](https://img.shields.io/pypi/v/remotivelabs-broker.svg)](https://pypi.org/project/remotivelabs-broker)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/remotivelabs-broker.svg)](https://pypi.org/project/remotivelabs-broker)

- [Link to **Samples**](https://github.com/remotivelabs/remotivelabs-samples/tree/main/python).
- [Link to **Documentation**](https://docs.remotivelabs.com/apis/python/remotivelabs/broker).

-----

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)
- [Build and Publish](#build-and-publish)
- [License](#license)

## Installation

Install into your Python environment with _PIP_:

    pip install remotivelabs-broker

## Examples

Examples using this library are found in the [Remotive Labs samples repository](https://github.com/remotivelabs/remotivelabs-samples).


## Develop and test locally

Put version in `__about__.py`. Beta versions should be suffixed with `b*`, example `0.2.0b1`

```bash
# For initial build and generation of proto stubs, documentation and distribution package
./docker-build.sh

Once stubs are generated you can use `hatch` to (re)-build distribution package. Use e.g. [pipx](https://github.com/pypa/pipx) to install `hatch`.

```bash
# install hatch in isolated env
pipx install hatch

# rebuild
hatch build
> [wheel]
> dist/remotivelabs_broker-<version>-py3-none-any.whl

# you can now install this library version in a virtualenv by opening a new terminal and doing:
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install dist/remotivelabs_broker-<version>-py3-none-any.whl

# test that the package is importable
python -c "import remotivelabs.broker.sync as br; print(dir(br.SignalCreator))"

# when you are done, exit the virtualenv
deactivate
```

## Build and publish

Make sure to put version in `__about__.py`. Beta versions should be suffixed with `b*`, example `0.2.0b1`

```
./docker-build.sh
hatch publish
```
find username and password in less secret location
or use
```
hatch publish --user __token__
```
## License

`remotivelabs-broker` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
