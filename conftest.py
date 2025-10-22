import pytest
import json
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def config():
    with open("config/config.json") as f:
        return json.load(f)

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=700)
        page = browser.new_page()
        yield page
        browser.close()
