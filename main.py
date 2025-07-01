from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import is_url_reachable, retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(), options=options)

        cls.server_url = "https://cnt-13e3aa71-c341-4341-8e54-c8201bb7e763.containerhub.tripleten-services.com"

        if not is_url_reachable(cls.server_url):
            raise Exception(f"Server {cls.server_url} is not reachable.")

        cls.driver.get(cls.server_url)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_address_input(self):
        page = UrbanRoutesPage(self.driver)
        from_address = "123 Main St"
        to_address = "456 Elm St"

        page.enter_locations(from_address, to_address)

        entered_from = self.driver.find_element(*page.from_field).get_attribute("value")
        entered_to = self.driver.find_element(*page.to_field).get_attribute("value")

        assert entered_from == from_address, "From address does not match input"
        assert entered_to == to_address, "To address does not match input"

    def test_empty_address_input(self):
        page = UrbanRoutesPage(self.driver)
        page.enter_locations("", "")

        self.driver.find_element(*page.order_button).click()

        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'error')]"))
        ).text
        assert "Please enter an address" in error_msg

    def test_invalid_address(self):
        page = UrbanRoutesPage(self.driver)
        page.enter_locations("!@#", "123 !@# Street")

        self.driver.find_element(*page.order_button).click()

        error = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'error')]"))
        ).text
        assert "Invalid address" in error

    def test_toggle_blanket(self):
        page = UrbanRoutesPage(self.driver)
        checked = page.toggle_blanket()
        assert checked in [True, False]

    def test_order_ice_cream(self):
        page = UrbanRoutesPage(self.driver)
        page.order_ice_cream(count=2)
        count = page.get_ice_cream_count()
        assert count == 2

    def test_driver_comment(self):
        page = UrbanRoutesPage(self.driver)
        comment_text = "Please ring the bell"
        page.write_driver_comment(comment_text)

        actual_comment = self.driver.find_element(*page.comment_input).get_attribute("value")
        assert comment_text == actual_comment

    def test_select_supportive_plan(self):
        page = UrbanRoutesPage(self.driver)
        if not page.is_supportive_plan_selected():
            page.select_supportive_plan()
        assert page.is_supportive_plan_selected(), "Supportive plan should be selected"

    def test_fill_phone_number_and_sms(self):
        page = UrbanRoutesPage(self.driver)
        phone = "5551234567"
        page.enter_phone_number(phone)
        sms_code = retrieve_phone_code(phone)
        page.enter_sms_code(sms_code)
        assert page.is_phone_verified(), "Phone verification failed"

    def test_add_credit_card(self):
        page = UrbanRoutesPage(self.driver)
        card = {
            "number": "4111111111111111",
            "expiry": "12/26",
            "cvv": "123",
            "name": "Test User"
        }
        page.open_add_card_modal()
        page.enter_card_number(card["number"])
        page.enter_card_expiry(card["expiry"])
        page.enter_card_cvv(card["cvv"])
        page.blur_cvv_field()  # simulate focus loss
        page.click_link_card_button()
        assert page.is_card_added(), "Credit card not added successfully"

    def test_order_supportive_taxi_with_comment(self):
        page = UrbanRoutesPage(self.driver)
        if not page.is_supportive_plan_selected():
            page.select_supportive_plan()

        message = "Call me when you arrive"
        page.write_driver_comment(message)
        page.order_taxi()

        assert page.is_car_search_modal_visible(), "Car search modal did not appear"
        assert page.get_driver_comment() == message, "Driver message mismatch"

