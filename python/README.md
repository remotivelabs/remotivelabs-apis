# RemotiveLabs Python libraries

## Usage

Python RemotiveBroker API

https://pypi.org/project/remotivelabs-broker/

Published on [PyPi](https://pypi.org/) with the prefix `remotivelabs-` and with the user [remotivelabs](https://pypi.org/user/remotivelabs/).
All packages use [Hatch](https://hatch.pypa.io/) for packaging and publishing.



## Development

Install hatch on your development computer:

    pip install hatch

Any project related information is stored in `pyproject.toml`.

Hatch supplies a basic set of tools for development.
All operations should be done in an virtual environment created by hatch.

Go to the directory of the module which you are going to be working on.
For example:

    cd python/remotivelabs-broker

Create a local environment.

    hatch env create

Start a shell in the environment.

    hatch shell

While in this virtual environment the library is available as a python module without needing to be installed.

Build the library:

    hatch build

Update the package version by editing the file `__about__.py`.
This version stamp will be used in Pypi.
Follow [Semantic versioning](https://semver.org/).

Testing, with coverage:

    hatch run cov

Without coverage:

    hatch run no-cov

While in the hatch virtual environment.
Run the Python debugger:

    python -m pdb ...

