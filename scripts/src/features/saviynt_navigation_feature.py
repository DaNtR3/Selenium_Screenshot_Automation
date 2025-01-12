import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SaviyntNavigationFeature:
    def __init__(self, driver):
        self.driver = driver
        self.application_panel_locator = '[class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]'
        self.admin_panel_locator = '[href="/ECM/jobcontrol/joblist"]'
        self.home_page_locator = '[href="/ECMv6/request/requestHome"]'

    def admin_panel(self):
        #Go to application panel
        app_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.application_panel_locator))
        )
        #time.sleep(1)
        app_button.click()
            
        #Click on admin panel
        admin_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.admin_panel_locator))
        )
        #time.sleep(1)
        admin_button.click()
            
        
    def home_page(self):
        #Go to home page
        home_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.home_page_locator))
        )
        #time.sleep(1)
        home_button.click()
        

