import os
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
    def __init__(self, initializer: AppInitializer):
        self.initializer = initializer

    def main(self):
        if not self.initializer.username or not self.initializer.password:
            print(
                "Please set OKTA_USERNAME and CYBERARK_PASSWORD environment variables"
            )
            return
        try:
            # Perform login
            success = self.initializer.user_login.login_to_saviynt()
            if success:
                self.initializer.iuc_nav_logic.security_system_feature(
                    self.initializer.saviynt_navigation.admin_panel,
                    self.initializer.saviynt_navigation.home_page,
                    self.initializer.screenshot_handler.take_screenshot
                )

                self.initializer.iuc_nav_logic.endpoint_feature(
                    self.initializer.saviynt_navigation.admin_panel,
                    self.initializer.saviynt_navigation.home_page,
                    self.initializer.screenshot_handler.take_screenshot
                )

                self.initializer.iuc_nav_logic.connection_feature(
                    self.initializer.saviynt_navigation.admin_panel,
                    self.initializer.saviynt_navigation.home_page,
                    self.initializer.screenshot_handler.scroll_and_capture
                )
                file_path = self.initializer.file_handler.add_screenshots_to_template()
                self.initializer.email_handler.send_email(file_path)
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.initializer.driver:
                self.initializer.driver.quit()

if __name__ == "__main__":
    app_initializer = AppInitializer()
    app_start = AppStart(app_initializer)
    app_start.main()
