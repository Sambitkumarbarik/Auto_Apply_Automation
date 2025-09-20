from playwright.sync_api import Page
import logging

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.naukri.com/nlogin/login"
        self.username_input = "#usernameField"
        self.password_input = "#passwordField"
        self.login_button = "button[type='submit']"

    def navigate(self):
        """Navigate to login page"""
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str) -> bool:
        """
        Perform login with given credentials
        Returns True if login successful, False otherwise
        """
        try:
            self.page.fill(self.username_input, email)
            self.page.fill(self.password_input, password)
            self.page.click(self.login_button)
            
            # Wait for navigation after login
            self.page.wait_for_load_state("networkidle")
            
            # Verify login success (check for some element that's only visible after login)
            return self.page.is_visible("text=My Naukri")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False
