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


### Develop and test locally

Put version in `__about__.py`. Beta versions should be suffixed with `b*`, example `0.2.0b1`

For initial build and generation of proto stubs, documentation and distribution package,  run  `./docker-build.sh`


Once stubs are generated you can use hatch to build distribution package

    hatch build

above command will output

    [wheel]
    dist/remotivelabs_broker-0.2.0b12-py3-none-any.whl

You can now install this library version in another terminal by doing

    pip3 install [your path]/dist/remotivelabs_broker-0.2.0b12-py3-none-any.whl

### Build and publish

Make sure to put version in `__about__.py`. Beta versions should be suffixed with `b*`, example `0.2.0b1`

    ./docker-build.sh
    hatch publish
> find username and password in less secret location ;)
## License

`remotivelabs-broker` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
