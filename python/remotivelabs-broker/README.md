# RemotiveLabs Broker

[![PyPI - Version](https://img.shields.io/pypi/v/remotivelabs-broker.svg)](https://pypi.org/project/remotivelabs-broker)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/remotivelabs-broker.svg)](https://pypi.org/project/remotivelabs-broker)

-----

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)
- [Development](#development)
- [License](#license)

## Installation
Install into your Python environment with _PIP_:

    pip install remotivelabs-broker


## Examples
Examples using this library are found in the [Remotive Labs samples repository](https://github.com/remotivelabs/remotivelabs-samples).

## Development
This project is managed with [Hatch](https://hatch.pypa.io/latest/).

Create an environment.

    hatch env create

Start a shell in the environment.

    hatch shell

### Generate stubs
This project has a script in the project file for generation. Generate stubs from proto files with:

    hatch run generate_stubs

## License

`remotivelabs-broker` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

