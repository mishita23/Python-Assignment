from playwright.sync_api import Page, expect

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.inventory_item = ".inventory_item"
        self.inventory_titles = ".inventory_item_name"
        self.cart_badge = ".shopping_cart_badge"
        self.cart_link = ".shopping_cart_link"
        self.details_add_button = "button[data-test='add-to-cart-sauce-labs-bike-light']" 
        self.generic_add_button = "button:has-text('Add to cart')"

    def get_inventory_titles(self):
        try:
            titles = [el.inner_text() for el in self.page.query_selector_all(self.inventory_titles)]
            assert titles, "No products found"
            return titles
        except Exception as e:
            raise Exception(f"Failed to fetch product titles: {e}")

    def add_to_cart(self, product_name: str):
        try:
            if self.page.url.endswith("inventory.html"):
                product_locator = self.page.locator(self.inventory_item).filter(has_text=product_name)
                add_button = product_locator.locator(self.generic_add_button)
                expect(add_button).to_be_visible(timeout=5000)
                add_button.click()
            elif "inventory-item.html" in self.page.url:

                add_button = self.page.locator(self.generic_add_button)
                expect(add_button).to_be_visible(timeout=5000)
                add_button.click()
            else:
                raise Exception("Unknown page")

        except Exception as e:
            raise Exception(f"Unable to add {product_name}: {e}")

    def open_product_details(self, product_name: str):
        try:
            self.page.locator(".inventory_item_name", has_text=product_name).click()
            expect(self.page.locator(".inventory_details_name")).to_be_visible()
        except Exception as e:
            raise Exception(f"Failed to open product details for {product_name}: {e}")

    def go_back_to_inventory(self):
        try:
            self.page.click("button[data-test='back-to-products']")
        except Exception as e:
            raise Exception(f"Failed to go back to inventory: {e}")

    def open_cart(self):
        try:
            self.page.click(self.cart_link)
        except Exception as e:
            raise Exception(f"Failed to open cart: {e}")

    def get_cart_count(self):
        try:
            if self.page.is_visible(self.cart_badge):
                return int(self.page.inner_text(self.cart_badge))
            return 0
        except:
            return 0
