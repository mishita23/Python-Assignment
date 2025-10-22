from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = "button[data-test='checkout']"
        self.cart_items = ".inventory_item_name"

    def get_cart_items(self):
        try:
            return [el.inner_text() for el in self.page.query_selector_all(self.cart_items)]
        except Exception as e:
            raise Exception(f"Unable to get items: {e}")

    def proceed_to_checkout(self):
        try:
            self.page.click(self.checkout_button)
        except Exception as e:
            raise Exception(f"Error in checkout : {e}")
