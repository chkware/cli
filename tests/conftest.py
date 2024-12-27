"""ConfTest"""

import pytest
from loguru import logger


@pytest.fixture(scope="session", autouse=True)
def disable_loguru() -> None:
    logger.disable("")
