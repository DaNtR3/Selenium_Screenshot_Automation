import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IUCNavigationFeature:

    def __init__(self, driver):
        self.driver = driver


    def security_system_feature(self, admin_nav_func, home_nav_func, take_screenshot_func):
        try:
            print("Starting security system feature navigation...")

            # First navigate to admin panel
            admin_nav_func()
            time.sleep(3)

            # Navigate to connection page
            print("Navigating to security system page...")

            # Go to left panel
            left_panel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"][aria-label="menu"]',
                    )
                )
            )
            time.sleep(1)
            left_panel.click()

            # Go to identity repository
            idrepo_opt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon"][aria-label="Identity Repository"]',
                    )
                )
            )
            time.sleep(1)
            idrepo_opt.click()

            # Go to security system tab
            security_system_opt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiListItem-root sidebar_sidebarItemHover__3ESE5 MuiListItem-dense MuiListItem-button"][aria-label="Security System"]',
                    )
                )
            )
            time.sleep(1)
            security_system_opt.click()

            # Click on decided security system
            click_security_system = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[href="/ECM/securitysystems/show/1"]')
                )
            )
            time.sleep(1)
            click_security_system.click()

            # Wait for page load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # If we're on the security page, capture
            if "securitysystems" in self.driver.current_url:
                print("Starting capture...")
                take_screenshot_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in security_system feature: {e}")
            raise


    def endpoint_feature(self, admin_nav_func, home_nav_func, take_screenshot_func):
        try:
            print("Starting endpoint feature navigation...")

            # First navigate to admin panel
            admin_nav_func()
            time.sleep(3)

            # Navigate to connection page
            print("Navigating to endpoint page...")

            # Go to left panel
            left_panel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"][aria-label="menu"]',
                    )
                )
            )
            time.sleep(1)
            left_panel.click()

            # Go to identity repository
            idrepo_opt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon"][aria-label="Identity Repository"]',
                    )
                )
            )
            time.sleep(1)
            idrepo_opt.click()

            # Go to security system tab
            security_system_opt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiListItem-root sidebar_sidebarItemHover__3ESE5 MuiListItem-dense MuiListItem-button"][aria-label="Security System"]',
                    )
                )
            )
            time.sleep(1)
            security_system_opt.click()

            # Go to endpoint tab
            endpoint_opt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[href="#tab_2-2"]'))
            )
            time.sleep(1)
            endpoint_opt.click()

            # Click on decided endpoint
            click_endpoint = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[href="/ECM/endpoints/show/768?savmodule="]')
                )
            )
            time.sleep(1)
            click_endpoint.click()

            # Click on accounts tab
            accounts_tab = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(text(), "Accounts")]')
                )
            )
            time.sleep(1)
            accounts_tab.click()

            time.sleep(5)

            # Wait for page load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//th[contains(text(), "Account Name")]')
                )
            )

            print("Starting capture for accounts...")
            take_screenshot_func()

            # Click on entitlements tab
            entitlements_tab = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(text(), "Entitlements")]')
                )
            )
            time.sleep(1)
            entitlements_tab.click()

            # Wait for page load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
            )

            print("Starting capture for entitlements...")
            take_screenshot_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in endpoint_feature: {e}")
            raise


    def connection_feature(self, admin_nav_func, home_nav_func, scroll_capture_func):
        try:
            print("Starting connection feature navigation...")

            # First navigate to admin panel
            admin_nav_func()
            time.sleep(3)

            # Navigate to connection page
            print("Navigating to connection page...")
            self.driver.get(
                "https://uat-mckesson.ssmcloud.net/ECM/ecmConfig/addnewconnection/26"
            )

            # Wait for page load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # If we're on the connection page, scroll and capture
            if "addnewconnection" in self.driver.current_url:
                print("Starting scroll and capture...")
                scroll_capture_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in connection_feature: {e}")
            raise
