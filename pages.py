from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.submit_button = (By.XPATH, "//button[contains(text(),'Call Taxi')]")

        self.supportive_plan = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Supportive']]")
        self.active_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]")

        self.phone_input = (By.ID, "phone")
        self.phone_code_input = (By.ID, "code")

        self.add_card_button = (By.CLASS_NAME, "add-button")
        self.card_number_input = (By.NAME, "number")
        self.card_expiry_input = (By.NAME, "expiry")
        self.card_cvv_input = (By.NAME, "code")
        self.link_card_button = (By.XPATH, "//button[text()='Link']")
        self.card_preview = (By.CLASS_NAME, "card-preview")

        self.comment_input = (By.ID, "comment")
        self.blanket_toggle = (By.ID, "blanket")
        self.ice_cream_button = (By.ID, "ice-cream")
        self.ice_cream_count = (By.CLASS_NAME, "ice-cream-count")

        self.order_button = (By.ID, "order")
        self.car_modal = (By.CLASS_NAME, "order-search")

    # ========== Location ==========
    def set_from(self, address):
        from_input = self.wait.until(EC.element_to_be_clickable(self.from_field))
        from_input.clear()
        from_input.send_keys(address, Keys.DOWN, Keys.ENTER)

    def set_to(self, address):
        to_input = self.wait.until(EC.element_to_be_clickable(self.to_field))
        to_input.clear()
        to_input.send_keys(address, Keys.DOWN, Keys.ENTER)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute("value")

    # ========== Tariff Plan ==========
    def click_call_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def is_supportive_plan_selected(self):
        active = self.wait.until(EC.presence_of_element_located(self.active_tariff))
        return "Supportive" in active.text

    def select_supportive_plan(self):
        if not self.is_supportive_plan_selected():
            self.wait.until(EC.element_to_be_clickable(self.supportive_plan)).click()

    # ========== Phone ==========
    def set_phone_number(self, number):
        phone = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone.clear()
        phone.send_keys(number)

    def set_sms_code(self, code):
        code_input = self.wait.until(EC.element_to_be_clickable(self.phone_code_input))
        code_input.clear()
        code_input.send_keys(code)

    def is_phone_number_set(self):
        return self.driver.find_element(*self.phone_input).get_attribute("value") != ""

    # ========== Payment ==========
    def click_payment_method_button(self):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

    def click_add_card_button(self):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

    def set_card_number(self, number):
        field = self.wait.until(EC.presence_of_element_located(self.card_number_input))
        field.clear()
        field.send_keys(number)

    def set_card_code(self, code):
        field = self.wait.until(EC.presence_of_element_located(self.card_cvv_input))
        field.clear()
        field.send_keys(code)

    def blur_card_code_field(self):
        field = self.wait.until(EC.presence_of_element_located(self.card_cvv_input))
        field.send_keys(Keys.TAB)

    def click_link_button(self):
        self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()

    def close_payment_method_modal(self):
        self.wait.until(EC.invisibility_of_element_located(self.link_card_button))

    def is_card_added(self):
        return self.wait.until(EC.visibility_of_element_located(self.card_preview)).is_displayed()

    # ========== Driver Comment ==========
    def set_message_for_driver(self, message):
        comment_field = self.wait.until(EC.element_to_be_clickable(self.comment_input))
        comment_field.clear()
        comment_field.send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.comment_input).get_attribute("value")

    # ========== Extras ==========
    def click_blanket_and_handkerchiefs(self):
        self.set_blanket(True)

    def is_blanket_and_handkerchiefs_selected(self):
        return self.set_blanket(True)

    def set_blanket(self, enable=True):
        blanket = self.wait.until(EC.element_to_be_clickable(self.blanket_toggle))
        is_checked = blanket.get_property("checked")
        if enable != is_checked:
            blanket.click()
        return blanket.get_property("checked")

    def click_ice_cream_plus(self):
        self.wait.until(EC.element_to_be_clickable(self.ice_cream_button)).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ice_cream_count).text)

    # ========== Final Order ==========
    def click_order_button(self):
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    def is_car_search_modal_visible(self):
        return self.wait.until(EC.presence_of_element_located(self.car_modal)).is_displayed()
