import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope="function", autouse="True")
def browser_set():
    driver_options = webdriver.ChromeOptions()
    browser.config.driver_options = driver_options

    yield
    browser.quit()