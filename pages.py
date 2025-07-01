from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")

    # More specific locator for submit / call taxi button (update text if needed)
    submit_button = (By.XPATH, "//button[contains(text(),'Call Taxi')]")

    supportive_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Supportive']]")
    active_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]")
    phone_input = (By.ID, "phone")
    phone_code_input = (By.ID, "code")
    add_card_button = (By.CLASS_NAME, "add-button")
    card_number_input = (By.NAME, "number")
    card_code_input = (By.NAME, "code")
    link_card_button = (By.XPATH, "//button[text()='Link']")
    comment_input = (By.ID, "comment")
    blanket_toggle = (By.ID, "blanket")
    ice_cream_button = (By.ID, "ice-cream")
    ice_cream_count = (By.CLASS_NAME, "ice-cream-count")
    order_button = (By.ID, "order")
    car_modal = (By.CLASS_NAME, "order-search")
    error_message = (By.CLASS_NAME, "error")  # Update based on your app's actual error message class or locator

    # Actions
    def enter_locations(self, from_address, to_address):
        from_input = self.wait.until(EC.element_to_be_clickable(self.from_field))
        from_input.clear()
        from_input.send_keys(from_address)
        from_input.send_keys(Keys.DOWN, Keys.ENTER)

        to_input = self.wait.until(EC.element_to_be_clickable(self.to_field))
        to_input.clear()
        to_input.send_keys(to_address)
        to_input.send_keys(Keys.DOWN, Keys.ENTER)

    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def select_supportive_tariff(self):
        current_tariff = self.wait.until(EC.presence_of_element_located(self.active_tariff))
        if "Supportive" not in current_tariff.text:
            self.wait.until(EC.element_to_be_clickable(self.supportive_tariff)).click()

    def enter_phone_number(self, number):
        phone_field = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone_field.clear()
        phone_field.send_keys(number)

    def enter_phone_code(self, code):
        code_field = self.wait.until(EC.element_to_be_clickable(self.phone_code_input))
        code_field.clear()
        code_field.send_keys(code)

    def add_credit_card(self, number, code):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

        card_number = self.wait.until(EC.presence_of_element_located(self.card_number_input))
        card_number.clear()
        card_number.send_keys(number)

        card_cvv = self.driver.find_element(*self.card_code_input)
        card_cvv.clear()
        card_cvv.send_keys(code)
        card_cvv.send_keys(Keys.TAB)

        self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()

    def write_driver_comment(self, comment):
        comment_field = self.wait.until(EC.element_to_be_clickable(self.comment_input))
        comment_field.clear()
        comment_field.send_keys(comment)

    def toggle_blanket(self):
        blanket = self.wait.until(EC.element_to_be_clickable(self.blanket_toggle))
        blanket.click()
        return blanket.get_property("checked")

    def order_ice_cream(self, count=2):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ice_cream_button)).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ice_cream_count).text)

    def place_order(self):
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    def is_car_modal_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.car_modal)).is_displayed()
