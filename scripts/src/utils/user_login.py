import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SaviyntLogin:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def login_to_saviynt(self):
        """Login to Saviynt UAT using username and password."""
        try:
            # First, clear all cookies
            self.driver.delete_all_cookies()

            # Go to Google's main page first
            #self.driver.get("https://www.google.com")
            #time.sleep(2)

            # Then go to Saviynt UAT
            self.driver.get("https://uat-mckesson.ssmcloud.net/ECMv6/request/requestHome")
            #time.sleep(6)

            # Enter username
            username_field = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "input44"))
            )

            # Type like a human
            username_field.clear()
            for char in self.username:
                username_field.send_keys(char)
                #time.sleep(0.1)
            #time.sleep(1)

            # Click sign in button
            sign_in_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form36"]/div[2]/input'))
            )
            #time.sleep(1)
            sign_in_button.click()

            # Click Okta push button
            push_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-se="okta_verify-push"] a')
                )
            )
            #time.sleep(1)
            push_button.click()


            # Enter password
            password_field = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[class="password-with-toggle"]')
                )
            )

            # Type like a human
            password_field.clear()
            for char in self.password:
                password_field.send_keys(char)
                #time.sleep(0.1)
            #time.sleep(1)

            # Click verify button
            verify_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[class="button button-primary"]')
                )
            )
            #time.sleep(1)
            verify_button.click()

            # Wait for the page to load fully
            #time.sleep(2)

            print("Successfully logged in to Saviynt UAT!")

            return True

        except Exception as e:
            print(f"Login failed: {e}")
            return False
