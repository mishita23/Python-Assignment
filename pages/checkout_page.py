from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = "input[data-test='firstName']"
        self.last_name_input = "input[data-test='lastName']"
        self.postal_code_input = "input[data-test='postalCode']"
        self.continue_button = "input[data-test='continue']"
        self.finish_button = "button[data-test='finish']"
        self.confirmation_msg = ".complete-header"

    def fill_checkout_info(self, first_name, last_name, postal_code):
        try:
            self.page.fill(self.first_name_input, first_name)
            self.page.fill(self.last_name_input, last_name)
            self.page.fill(self.postal_code_input, postal_code)
            self.page.click(self.continue_button)
        except Exception as e:
            raise Exception(f"Checkout failed: {e}")

    def finish_purchase(self):
        try:
            self.page.click(self.finish_button)
        except Exception as e:
            raise Exception(f"Purchase failed: {e}")

    def get_confirmation_message(self):
        try:
            return self.page.inner_text(self.confirmation_msg)
        except Exception as e:
            raise Exception(f"Could not get confirmation: {e}")
