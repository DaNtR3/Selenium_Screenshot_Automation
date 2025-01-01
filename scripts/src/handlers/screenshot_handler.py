import os
import pyautogui
import time
import string
import random
from datetime import datetime

class ScreenshotHandler:
    def __init__(self, driver, text_area_handler):
        self.driver = driver
        self.text_area_handler = text_area_handler
        # Generate a unique folder name for the screenshots
        self.temp_folder = self.generate_unique_folder_name()
        # Directory for saving screenshots
        self.screenshots_path = f'C:\DEV\Py_Selenium_Script 1\scripts\screenshots\{self.temp_folder}'

    def take_screenshot(self):
        """Take a screenshot of the current page."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.screenshots_path, exist_ok=True)

            # Zoom out the page before taking the screenshot
            self.driver.execute_script("document.body.style.zoom = '75%'")
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"saviynt_screenshot_{timestamp}.png"
            full_path = os.path.join(self.screenshots_path, filename)
            
            # Ensure page is loaded
            time.sleep(2)
            
            # Take the actual screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(full_path)
            print(f"Screenshot saved to: {full_path}")
            
        except Exception as e:
            print(f"Error taking screenshot: {e}")

    def scroll_and_capture(self):
        """Scroll the page and take screenshots at intervals."""
        try:
            #Expanding textareas
            self.text_area_handler()
            
            # Get viewport height
            viewport_height = self.driver.execute_script("return window.innerHeight")
            print(f"Viewport height: {viewport_height}")
            
            # Initialize scroll positions
            scroll_position = 0
            previous_scroll_position = -1
            
            while True:
                print(f"Current scroll position: {scroll_position}")
                
                # Scroll to the current position
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(2)  # Wait for dynamic content to load
                
                # Get current scroll position
                current_scroll_position = self.driver.execute_script("return window.scrollY")
                
                # Check if we've reached the end
                if current_scroll_position == previous_scroll_position:
                    print("Reached end of page")
                    break
                    
                # Take screenshot at current position
                self.take_screenshot()
                
                # Update positions
                scroll_position += int(viewport_height / 1.3)
                previous_scroll_position = current_scroll_position
        except Exception as e:
            print(f"Error in scroll_and_capture: {e}")
        
    def generate_unique_folder_name(self):
        try:
            # Get the current timestamp in a specific format (includes hour, minute, and second)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            #Generate random string of desired lenght
            random_string = ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k=5))
            # Combine the prefix, timestamp and random string to generate a unique name
            unique_folder_name = f"Temp_{timestamp}_{random_string}"
            return unique_folder_name
        except Exception as e:
            # Catch any exception
            print(f"Error occurred while generating the unique name: {e}")
            return None
            
        