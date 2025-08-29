import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
from pages import UrbanRoutesPage
import helpers
import data
 
class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
 
        options = Options()
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
 
        cls.driver = webdriver.Chrome(options=options)
 
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            cls.driver.get(data.URBAN_ROUTES_URL)
        else:
            raise Exception("URL not reachable")
 
        cls.page = UrbanRoutesPage(cls.driver)
 
    def test_set_address(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
 
        assert routes_page.get_from_address() == data.ADDRESS_FROM
        assert routes_page.get_to_address() == data.ADDRESS_TO
 
    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
 
        assert routes_page.is_supportive_plan_selected()
 
    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.enter_phone_number(data.PHONE_NUMBER)
 
        assert routes_page.is_phone_verified()
 
    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.enter_payment_method(data.CARD_NUMBER, data.CARD_CODE)
 
        assert routes_page.is_card_linked()
 
    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
 
        assert routes_page.get_message_for_driver() == data.MESSAGE_FOR_DRIVER
 
    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.click_blanket_and_handkerchiefs_slider()
 
        assert routes_page.is_blanket_and_handkerchiefs_selected()
 
    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.order_ice_cream(2)
 
        assert routes_page.get_ice_cream_count() == 2
 
    def test_car_search_modal_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.enter_phone_number(data.PHONE_NUMBER)
        routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        routes_page.click_order_button()
 
        assert routes_page.is_car_search_modal_visible()
 
 
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
