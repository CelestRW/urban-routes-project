# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from helpers import is_url_reachable

@pytest.fixture(scope="class")
def driver(request):
    options = Options()
    options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

    service = Service()  # Add path to chromedriver if needed, e.g. Service("path/to/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    server_url = "https://cnt-6b6b6f2c-4d5b-4554-9172-cd2ae1c71c5e.containerhub.tripleten-services.com"
    if not is_url_reachable(server_url):
        driver.quit()
        pytest.skip(f"Server {server_url} is not reachable.")

    driver.get(server_url)
    request.cls.driver = driver  # Attach driver to the test class for easy access

    yield driver

    driver.quit()
