from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "//input[@data-test='username']"
        self.password_input = "input[data-test='password']"
        self.login_button = "input[data-test='login-button']"
        self.error_msg = "h3[data-test='error']"

    def load(self, url: str):
        try:
            self.page.goto(url)
            assert "Swag Labs" in self.page.title(), "Page title mismatch"
        except Exception as e:
            raise Exception(f"Failed to load login page: {e}")

    def login(self, username: str, password: str):
        try:
            self.page.fill(self.username_input, username)
            self.page.fill(self.password_input, password)
            self.page.click(self.login_button)
        except Exception as e:
            raise Exception(f"Login failed: {e}")

    def is_error_displayed(self):
        try:
            return self.page.is_visible(self.error_msg)
        except:
            return False
