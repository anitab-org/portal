import os
import pytest
from selenium import webdriver

browsers = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
}


@pytest.fixture(scope="class")
def browser(request):
    if 'DISPLAY' not in os.environ:
        pytest.skip('Test requires display server (export DISPLAY)')

    b = browsers[request.config.getoption("--browser-config")]()

    request.addfinalizer(lambda *args: b.quit())

    # inject class variables
    request.cls.browser = b

    return b


def pytest_addoption(parser):
    parser.addoption(
        "--browser-config",
        action="store",
        default="chrome",
        help="firefox, chrome are allowed parameters")
