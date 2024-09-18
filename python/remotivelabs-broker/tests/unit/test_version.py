from importlib.metadata import version

from remotivelabs.broker import __about__


def test_version_matches_package() -> None:
    # setup
    package_version = version("remotivelabs-broker")

    # when
    about_version = __about__.__version__

    # then
    assert (
        package_version == about_version
    ), f"Version mismatch: package version is {package_version}, but __about__.__version__ is {about_version}"


def test_version_not_unknown() -> None:
    assert __about__.__version__ != "unknown", "Version is 'unknown', which suggests the package is not properly installed"
