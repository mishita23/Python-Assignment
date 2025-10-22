import pytest
import csv
import os
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.flaky(reruns=2)
@pytest.mark.parametrize("user", ["valid_user", "invalid_user"])
def test_purchase_flow(browser, config, user):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)
    cart_page = CartPage(browser)
    checkout_page = CheckoutPage(browser)
# login
    login_page.load(config["base_url"])
    login_page.login(config[user]["username"], config[user]["password"])

    if user == "invalid_user":
        assert login_page.is_error_displayed(), "Error not showing, for invalid user"
        return

# screenshot after login
    os.makedirs(config["screenshots_dir"], exist_ok=True)
    browser.screenshot(path=f'{config["screenshots_dir"]}/done_login.png')

#inventory page
    with open("data/products.csv", newline="") as csvfile:
        products = [row["product_name"] for row in csv.DictReader(csvfile)]

#check if products are in inventory list or not
    inventory_titles = inventory_page.get_inventory_titles()
    for product in products:
        assert product in inventory_titles, f"{product} not found in inventory list"

# add first product to cart, open second in detailed view, and add go back, add other two to cart
    inventory_page.add_to_cart(products[0])
    inventory_page.open_product_details(products[1])
    inventory_page.add_to_cart(products[1])
    inventory_page.go_back_to_inventory()
    for product in products[2:]:
        inventory_page.add_to_cart(product)

# check cart count
    assert inventory_page.get_cart_count() == len(products), "Cart count mismatch"
    browser.screenshot(path=f'{config["screenshots_dir"]}/cart_after_adding.png')

    inventory_page.open_cart()
    cart_items = cart_page.get_cart_items()
    assert set(products) == set(cart_items), "Cart items mismatch with added items"

    cart_page.proceed_to_checkout()

# checkout details
    with open("data/checkout_data.csv", newline="", encoding="utf-8") as csvfile:
        data = list(csv.DictReader(csvfile))[0]
        checkout_page.fill_checkout_info(data["first_name"], data["last_name"], data["postal_code"])

#confirmation
    checkout_page.finish_purchase()
    msg = checkout_page.get_confirmation_message()
    assert "THANK YOU FOR YOUR ORDER" in msg.upper(), "Order confirmation message not found"

    browser.screenshot(path=f'{config["screenshots_dir"]}/order_done.png')
