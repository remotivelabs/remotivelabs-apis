"""
Configure logging according to best practicies for libraries

https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
"""

import logging


def configure_logging() -> None:
    logging.getLogger("remotivelabs.broker").addHandler(logging.NullHandler())
