from helpers import is_url_reachable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Use set_capability instead of desired_capabilities
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_experimental_option("perfLoggingPrefs", {
            "enableNetwork": True,
            "enablePage": False
        })

        cls.driver = webdriver.Chrome(options=options)

        cls.server_url = "https://cnt-797fe768-04fe-4845-94a8-272b4f21709c.containerhub.tripleten-services.com"
        if not is_url_reachable(cls.server_url):
            raise Exception(f"Server {cls.server_url} is not reachable.")

        cls.driver.get(cls.server_url)
        cls.driver.maximize_window()
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        from_address = "East 2nd Street, 601"
        to_address = "1300 1st St"
        self.page.set_from(from_address)
        self.page.set_to(to_address)
        assert self.page.get_from() == from_address
        assert self.page.get_to() == to_address

    def test_select_supportive_plan(self):
        """Test 2: Selecting Supportive plan"""
        self.page.click_call_taxi_button()

        if not self.page.is_supportive_plan_selected():
            self.page.select_supportive_plan()

        assert self.page.is_supportive_plan_selected(), "Supportive plan should be selected"

    def test_fill_phone_number(self):
        """Test 3: Filling in the phone number"""
        phone_number = "+1 123 123 12 12"
        self.page.set_phone_number(phone_number)

        sms_code = retrieve_phone_code(phone_number)
        self.page.set_sms_code(sms_code)

        assert self.page.is_phone_number_set(), "Phone number should be set"

    def test_add_credit_card(self):
        """Test 4: Adding a credit card"""
        self.page.click_payment_method_button()
        self.page.click_add_card_button()

        self.page.set_card_number("1234 5678 9100 0000")
        self.page.set_card_code("111")

        self.page.blur_card_code_field()
        self.page.click_link_button()
        self.page.close_payment_method_modal()

        assert self.page.is_card_added(), "Credit card should be added"

    def test_write_message_for_driver(self):
        """Test 5: Writing a comment for the driver"""
        message = "Bring some napkins please"
        self.page.set_message_for_driver(message)

        assert self.page.get_message_for_driver() == message, "Driver message did not match"

    def test_order_blanket_and_handkerchiefs(self):
        """Test 6: Ordering a Blanket and handkerchiefs"""
        self.page.click_blanket_and_handkerchiefs()

        assert self.page.is_blanket_and_handkerchiefs_selected(), "Blanket and handkerchiefs should be selected"

    def test_order_ice_cream(self):
        """Test 7: Ordering 2 Ice creams"""
        self.page.click_ice_cream_plus()
        self.page.click_ice_cream_plus()

        ice_cream_count = self.page.get_ice_cream_count()
        assert ice_cream_count == 2, f"Expected 2 ice creams, but got {ice_cream_count}"

    def test_order_taxi_supportive_plan(self):
        """Test 8: Order a taxi with the 'Supportive' tariff"""
        message = "Please call when you arrive"
        self.page.set_message_for_driver(message)

        self.page.click_order_button()

        assert self.page.is_car_search_modal_visible(), "Car search modal should appear after ordering taxi"
