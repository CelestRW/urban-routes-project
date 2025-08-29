import helpers
import time
from selenium.common.exceptions import TimeoutException
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
        self.submit_button = (By.XPATH, "//button[contains(text(),'Call a taxi')]")
 
        self.supportive_plan = (By.XPATH, "//div[contains(@class, 'tcard')]//div[text()='Supportive']/..")
        self.active_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]")
 
        self.phone_input = (By.ID, "phone")
        self.next_button = (By.XPATH, "//button[contains(text(), 'Next')]")
        self.phone_code_input = (By.ID, "code")
        self.confirm_button = (By.XPATH, "//button[contains(text(), 'Confirm')]")
 
        self.payment_method_button = (By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Payment method']]")
        self.add_card_button = (
            By.XPATH,
            "//div[contains(@class, 'pp-row') and .//div[contains(@class, 'pp-title') and text()='Add card']]]"
        )
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.ID, "code")
        self.link_card_button = (By.XPATH, "//button[text()='Link']")
 
        self.comment_input = (By.ID, "comment")
        self.blanket_and_handkerchiefs_checkbox = (By.XPATH, "//input[@type='checkbox']")
        self.blanket_and_handkerchiefs_slider = (By.CLASS_NAME, "slider")
        self.ice_cream_button = (By.ID, "ice-cream")
        self.ice_cream_count = (By.CLASS_NAME, "ice-cream-count")
 
        self.order_button = (By.ID, "order")
        self.car_modal = (By.CLASS_NAME, "order-search")
 
        # ========== ADDRESS ==========
 
    def set_route(self, from_address, to_address):
        from_input = self.wait.until(EC.element_to_be_clickable((By.ID, "from")))
        from_input.clear()
        from_input.send_keys(from_address, Keys.DOWN, Keys.ENTER)
        time.sleep(1)  # Give dropdown time to resolve
 
        to_input = self.wait.until(EC.element_to_be_clickable((By.ID, "to")))
        to_input.clear()
        to_input.send_keys(to_address, Keys.DOWN, Keys.ENTER)
        time.sleep(1)  # Same here
 
        try:
            call_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Call a taxi')]"))
            )
            call_btn.click()
            time.sleep(1)
        except TimeoutException:
            print("[ERROR] 'Call a taxi' button not found or not clickable")
            self.driver.save_screenshot("call_taxi_button_fail.png")
            raise
 
    def get_from_address(self):
        return self.driver.find_element(By.ID, "from").get_attribute("value")
 
    def get_to_address(self):
        return self.driver.find_element(By.ID, "to").get_attribute("value")
 
    # ========== TARIFF PLAN ==========
    def select_supportive_plan(self):
        current = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcard.active")))
        if "Supportive" not in current.text:
            plan = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Supportive']")))
            plan.click()
            WebDriverWait(self.driver, 5).until(lambda d: self.is_supportive_plan_selected())
 
    def is_supportive_plan_selected(self):
        active_card = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcard.active")))
        return "Supportive" in active_card.text
 
    # ========== PHONE NUMBER ==========
    def enter_phone_number(self, phone_number):
        try:
            np_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "np-button")))
            np_button.click()
        except TimeoutException:
            pass
 
        phone_input = self.wait.until(EC.element_to_be_clickable((By.ID, "phone")))
        phone_input.clear()
        phone_input.send_keys(phone_number)
 
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))).click()
 
        code = helpers.retrieve_phone_code(self.driver)
        sms_input = self.wait.until(EC.element_to_be_clickable((By.ID, "code")))
        sms_input.send_keys(code)
 
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))).click()
 
    def is_phone_verified(self):
        phone_input = self.driver.find_element(By.ID, "phone")
        return phone_input.get_attribute("value") != ""
 
        # ========== PAYMENT ==========
 
    def enter_payment_method(self, card_number, card_code):
        # Click "Payment method" first
        try:
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pp-button"))).click()
            time.sleep(1)
        except TimeoutException:
            print("[ERROR] Payment method button not clickable")
            return
 
        # Wait for overlay to disappear
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        except TimeoutException:
            print("[INFO] Overlay still visible after clicking Payment Method")
 
        # Scroll to the "Add card" container
        try:
            add_card_container = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'pp-title') and text()='Add card']/ancestor::div[contains(@class, 'pp-row')]"
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_container)
            time.sleep(1)  # Let the DOM update
        except Exception as e:
            print(f"[ERROR] Couldn't find 'Add card' container: {e}")
            return
 
        # Wait until it's enabled
        try:
            self.wait.until(lambda d: "disabled" not in add_card_container.get_attribute("class"))
            print("[DEBUG] 'Add card' container is now enabled")
        except TimeoutException:
            print("[ERROR] 'Add card' never became enabled")
            self.driver.save_screenshot("add_card_disabled_timeout.png")
            return
 
        # Click it
        try:
            add_card_container.click()
            print("[DEBUG] Clicked 'Add card'")
        except Exception as e:
            print(f"[ERROR] Failed to click 'Add card': {e}")
            self.driver.save_screenshot("add_card_click_fail.png")
            return
 
        # Fill card
        self.set_card_number(card_number)
        self.set_card_code(card_code)
 
        # Click Link
        try:
            link_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Link']")))
            link_btn.click()
            print("[DEBUG] Clicked 'Link' button")
        except Exception as e:
            print(f"[ERROR] Failed to click 'Link': {e}")
            self.driver.save_screenshot("link_click_fail.png")
 
    def set_card_number(self, number):
        try:
            card_input = self.wait.until(EC.visibility_of_element_located((By.ID, "number")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", card_input)
            card_input.clear()
            card_input.send_keys(number)
            card_input.send_keys(Keys.TAB)
            print("[DEBUG] Entered card number and sent TAB")
        except Exception as e:
            print("[ERROR] Failed to set card number:", e)
            self.driver.save_screenshot("card_number_fail.png")
 
    def set_card_code(self, code):
        try:
            time.sleep(0.5)
            code_input = self.wait.until(EC.visibility_of_element_located((By.ID, "code")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", code_input)
            code_input.clear()
            code_input.send_keys(code)
            code_input.send_keys(Keys.TAB)
            print("[DEBUG] Entered card code and sent TAB")
        except Exception as e:
            print("[ERROR] Failed to set card code:", e)
            self.driver.save_screenshot("card_code_fail.png")
 
    def is_card_linked(self):
        payment = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pp-button")))
        return "Card" in payment.text
 
    # ========== COMMENT ==========
    def set_message_for_driver(self, message):
        comment_box = self.wait.until(EC.element_to_be_clickable((By.ID, "comment")))
        comment_box.clear()
        comment_box.send_keys(message)
 
    def get_message_for_driver(self):
        return self.driver.find_element(By.ID, "comment").get_attribute("value")
 
    # ========== BLANKET & HANDKERCHIEFS ==========
    def click_blanket_and_handkerchiefs_slider(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "slider"))).click()
 
    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        return checkbox.get_property("checked")
 
    # ========== ICE CREAM ==========
    def order_ice_cream(self, count):
        for i in range(count):
            print(f"[DEBUG] Trying to click ice cream button #{i + 1}")
            try:
                button = self.wait.until(EC.element_to_be_clickable((By.ID, "ice-cream")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                print(f"[DEBUG] Ice cream button #{i + 1} clicked")
            except TimeoutException:
                print(f"[ERROR] Ice cream button not found or not clickable on attempt #{i + 1}")
                self.driver.save_screenshot(f"ice_cream_click_fail_{i + 1}.png")
 
    def get_ice_cream_count(self):
        try:
            count = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ice-cream-count")))
            return int(count.text)
        except TimeoutException:
            print("[ERROR] Ice cream count element not found.")
            self.driver.save_screenshot("ice_cream_count_fail.png")
            return -1
 
    # ========== FINAL ORDER ==========
    def click_order_button(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        except TimeoutException:
            print("[INFO] Overlay still visible before clicking Order")
 
        try:
            order_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "order")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", order_btn)
            order_btn.click()
            print("[DEBUG] Order button clicked")
        except TimeoutException:
            print("[ERROR] Order button not found or not clickable")
            self.driver.save_screenshot("order_button_fail.png")
 
    def is_car_search_modal_visible(self):
        try:
            modal = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "order-search")))
            return modal.is_displayed()
        except TimeoutException:
            return False
