import os
import time
import argparse
import json
from dotenv import load_dotenv
from handlers.web_driver_handler import WebDriverManager
from dotenv import load_dotenv
from handlers.email_handler import EmailManager
from handlers.web_driver_handler import WebDriverManager
from utils.user_login import SaviyntLogin
from handlers.screenshot_handler import ScreenshotHandler
from handlers.text_area_handler import TextAreaHandler
from handlers.file_handler import FileHandler
from features.iuc_navigation_feature import IUCNavigationFeature
from features.saviynt_navigation_feature import SaviyntNavigationFeature

class AppInitializer:
    def __init__(self):
        # Load environment variables and set up
        load_dotenv()
        self.username = os.getenv("OKTA_USERNAME")
        self.password = os.getenv("CYBERARK_PASSWORD")
        self.driver = WebDriverManager.setup_driver(self)
        self.user_login = SaviyntLogin(self.driver, self.username, self.password)
        self.textarea_handler = TextAreaHandler(self.driver)
        self.email_handler = EmailManager()
        self.screenshot_handler = ScreenshotHandler(self.driver, self.textarea_handler.expand_all_textareas_conn)
        self.file_handler = FileHandler(self.screenshot_handler.screenshots_path)
        self.saviynt_navigation = SaviyntNavigationFeature(self.driver)
        self.iuc_nav_logic = IUCNavigationFeature(self.driver)

class AppStart:
    def __init__(self, initializer: AppInitializer, security_systems, endpoints, connection_keys):
        self.initializer = initializer
        # Deserialize the JSON strings back to Python objects (lists of dictionaries, etc.)
        self.security_systems = json.loads(security_systems) if security_systems else []
        self.endpoints = json.loads(endpoints) if endpoints else []
        self.connection_keys = json.loads(connection_keys) if connection_keys else []

    def main(self):
        start_time = time.time()
        if not self.initializer.username or not self.initializer.password:
            print("Please set OKTA_USERNAME and CYBERARK_PASSWORD environment variables")
            return
        try:
            # Perform login
            success = self.initializer.user_login.login_to_saviynt()
            if success:
                # Process security systems
                for system in self.security_systems:
                    system_key = system['id']
                    system_name = system['name']
                    print(f"Processing security system - Key: {system_key} - Name: {system_name}")
                    self.initializer.iuc_nav_logic.security_system_feature(
                        self.initializer.saviynt_navigation.admin_panel,
                        self.initializer.saviynt_navigation.home_page,
                        self.initializer.screenshot_handler.take_screenshot,
                        system_key, 
                        system_name
                    )
                # Process endpoints
                for endpoint in self.endpoints:
                    endpoint_key = endpoint['id']
                    endpoint_name = endpoint['name']
                    print(f"Processing endpoint - Key: {endpoint_key} - Name: {endpoint_name}")
                    self.initializer.iuc_nav_logic.endpoint_feature(
                        self.initializer.saviynt_navigation.admin_panel,
                        self.initializer.saviynt_navigation.home_page,
                        self.initializer.screenshot_handler.take_screenshot,
                        endpoint_key,
                        endpoint_name
                    )
                # Process unique connections
                for connection_key in self.connection_keys:
                    print(f"Processing connection ID: {connection_key}")
                    self.initializer.iuc_nav_logic.connection_feature(
                        self.initializer.saviynt_navigation.admin_panel,
                        self.initializer.saviynt_navigation.home_page,
                        self.initializer.screenshot_handler.scroll_and_capture,
                        connection_key
                    )
                file_path = self.initializer.file_handler.add_screenshots_to_template()
                self.initializer.email_handler.send_email(file_path, self.initializer.file_handler.remove_file)
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.initializer.driver:
                self.initializer.driver.quit()
            end_time = time.time()  # Capture end time in seconds
            duration_seconds = end_time - start_time  # Calculate duration in seconds
            duration_minutes = duration_seconds / 60  # Convert duration to minutes
            print(f"Process completed in {duration_minutes:.2f} minutes")  # Print time in minutes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--security_systems', type=str, help='JSON string of security systems')
    parser.add_argument('--endpoints', type=str, help='JSON string of endpoints')
    parser.add_argument('--connection_keys', type=str, help='JSON string of connection keys')
    args = parser.parse_args()

    initializer = AppInitializer()
    app = AppStart(initializer, args.security_systems, args.endpoints, args.connection_keys)
    app.main()