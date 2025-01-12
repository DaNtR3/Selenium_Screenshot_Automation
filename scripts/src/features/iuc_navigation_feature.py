import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IUCNavigationFeature:

    def __init__(self, driver):
        self.driver = driver


    def security_system_feature(self, admin_nav_func, home_nav_func, take_screenshot_func, systemkey, systemname):
        try:
            print(f"Starting security system feature navigation for systemkey: {systemkey}...")

            # First navigate to admin panel
            admin_nav_func()
            #time.sleep(3)

            # Navigate to connection page
            print("Navigating to security system page...")

            # Go to left panel
            left_panel = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"][aria-label="menu"]',
                    )
                )
            )
            #time.sleep(1)
            left_panel.click()

            # Go to identity repository
            idrepo_opt = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon"][type="button"][aria-label="Identity Repository"]',
                    )
                )
            )
            #time.sleep(1)
            idrepo_opt.click()

            # Go to security system tab
            security_system_opt = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[href="/ECM/securitysystems/list"]',
                    )
                )
            )
            #time.sleep(0.5)
            security_system_opt.click()

            #Click on search bar
            ss_searchbar = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[id="dtsearch_securitysystemsList"]',
                    )
                )
            )
            # Type the security system name in the search bar
            ss_searchbar.clear()
            for char in systemname:
                ss_searchbar.send_keys(char)
                #time.sleep(0.1)
            #time.sleep(1)

            # Search the security system
            search_ss = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[id="search_securitysystemsList"]',
                    )
                )
            )
            #time.sleep(1)
            search_ss.click()

            #time.sleep(2)

            # Click on decided security system
            click_security_system = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'[href="/ECM/securitysystems/show/{systemkey}"]')
                )
            )
            #time.sleep(1)
            click_security_system.click()

            # Wait for page load
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # If we're on the security page, capture
            if "securitysystems" in self.driver.current_url:
                print(f"Starting capture for systemkey: {systemkey}...")
                take_screenshot_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in security_system feature for systemkey: {systemkey}: {e}")
            raise


    def endpoint_feature(self, admin_nav_func, home_nav_func, take_screenshot_func, endpointkey, endpoint_name):
        try:
            print(f"Starting endpoint feature navigation for endpointkey: {endpointkey}...")

            # First navigate to admin panel
            admin_nav_func()
            #time.sleep(3)

            # Navigate to connection page
            print("Navigating to endpoint page...")

            # Go to left panel
            left_panel = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"][aria-label="menu"]',
                    )
                )
            )
            #time.sleep(1)
            left_panel.click()

            # Go to identity repository
            idrepo_opt = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon"][type="button"][aria-label="Identity Repository"]',
                    )
                )
            )
            #time.sleep(5)
            idrepo_opt.click()

            # Go to security system tab
            security_system_opt = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[href="/ECM/securitysystems/list"]',
                    )
                )
            )
            #time.sleep(0.5)
            security_system_opt.click()

            # Go to endpoint tab
            endpoint_opt = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[href="#tab_2-2"]'))
            )
            #time.sleep(1)
            endpoint_opt.click()

            #Click on search bar
            ep_searchbar = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '[id="dtsearch_endpointsList"]',
                    )
                )
            )
            # Type the endpoint name in the search bar
            ep_searchbar.clear()
            for char in endpoint_name:
                ep_searchbar.send_keys(char)
                #time.sleep(0.1)
            #time.sleep(1)

            # Search the endpoint
            search_ep = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '[id="search_endpointsList"]',
                    )
                )
            )
            #time.sleep(1)
            search_ep.click()

            #time.sleep(3)

            # Click on decided endpoint
            click_endpoint = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'[href="/ECM/endpoints/show/{endpointkey}?savmodule="]')
                )
            )
            #time.sleep(1)
            click_endpoint.click()

            # Click on accounts tab
            accounts_tab = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(text(), "Accounts")]')
                )
            )
            #time.sleep(1)
            accounts_tab.click()

            #time.sleep(5)

            # Wait for page load
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//th[contains(text(), "Account Name")]')
                )
            )

            print("Starting capture for accounts...")
            take_screenshot_func()

            # Click on entitlements tab
            entitlements_tab = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(text(), "Entitlements")]')
                )
            )
            #time.sleep(1)
            entitlements_tab.click()

            # Wait for the page load (up to 60 seconds)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'EntitlementValueList')]/tbody"))
            )

            print("Starting capture for entitlements...")
            take_screenshot_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in endpoint_feature for endpointkey: {endpointkey}: {e}")
            raise


    def connection_feature(self, admin_nav_func, home_nav_func, scroll_capture_func, connectionkey):
        try:
            print(f"Starting connection feature navigation for connectionkey: {connectionkey}...")

            # First navigate to admin panel
            admin_nav_func()
            #time.sleep(3)

            # Navigate to connection page
            print("Navigating to connection page...")
            self.driver.get(
                f"https://uat-mckesson.ssmcloud.net/ECM/ecmConfig/addnewconnection/{connectionkey}"
            )

            # Wait for page load
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # If we're on the connection page, scroll and capture
            if "addnewconnection" in self.driver.current_url:
                print(f"Starting scroll and capture for connectionkey: {connectionkey}...")
                scroll_capture_func()

            print("Navigating back to home page...")
            home_nav_func()

        except Exception as e:
            print(f"Error in connection_feature for connectionkey: {connectionkey}: {e}")
            raise
