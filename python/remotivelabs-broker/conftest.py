import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--broker",
        action="store",
        default="http://localhost:50051",
        type=str,
        help="Broker URI to run test against.",
    )


@pytest.fixture
def broker_url(request):
    return request.config.getoption("--broker")
