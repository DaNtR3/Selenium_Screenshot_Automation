import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TextAreaHandler:
    
    def __init__(self, driver):
        self.textarea_selector="textarea"
        self.driver = driver

    def expand_all_textareas_conn(self):
        """Expand all textareas to fit their content."""
        try:
            textareas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.textarea_selector))
            )
            
            for textarea in textareas:
                textarea_height = int(textarea.get_attribute('offsetHeight'))
                scroll_height = int(textarea.get_attribute('scrollHeight'))
                
                if scroll_height > textarea_height:
                    self.driver.execute_script(f"arguments[0].style.height = '{scroll_height}px';", textarea)
                    print(f"Expanding textarea: From {textarea_height}px to {scroll_height}px.")
                else:
                    print(f"Textarea is already fully expanded: {textarea_height}px.")
            time.sleep(0.2)
        
        except Exception as e:
            print(f"Error expanding textareas: {e}")