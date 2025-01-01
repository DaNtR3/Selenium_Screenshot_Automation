import os
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverManager:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-save-password-bubble")
            options.add_experimental_option(
                "prefs",
                {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                },
            )
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            if os.path.exists(
                "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ):
                options.binary_location = (
                    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                )

            self.driver = webdriver.Chrome(options=options)

            # Apply stealth settings
            stealth(
                self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

            return self.driver

        except Exception as e:
            print(f"Error setting up the WebDriver: {e}")
            return None
