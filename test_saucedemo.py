import os
import re

import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.getenv("SAUCEDEMO_URL", "https://saucedemo.com").rstrip("/")
USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")


@pytest.fixture
def page(browser):
    context = browser.new_context()
    try:
        yield context.new_page()
    finally:
        context.close()


def test_saucedemo_checkout_happy_path(page: Page) -> None:
    page.goto(BASE_URL)

    expect(page).to_have_title("Swag Labs")
    expect(page.get_by_role("textbox", name="Username")).to_be_visible()
    expect(page.get_by_role("textbox", name="Password")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.get_by_text("Products", exact=True)).to_be_visible()

    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    expect(product).to_be_visible()
    product.get_by_role("button", name="Add to cart").click()

    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    page.get_by_role("button", name=re.compile(r"Cart.*1.*")).click()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".cart_item")).to_contain_text("Sauce Labs Backpack")

    page.get_by_role("button", name="Checkout").click()

    page.get_by_role("textbox", name="First Name").fill("Test")
    page.get_by_role("textbox", name="Last Name").fill("Customer")
    page.get_by_role("textbox", name="Zip/Postal Code").fill("10001")
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
    expect(page.locator(".cart_item")).to_contain_text("Sauce Labs Backpack")
    expect(page.get_by_text("Item total: $29.99")).to_be_visible()

    page.get_by_role("button", name="Finish").click()

    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    expect(page.get_by_role("heading", name="Thank you for your order!")).to_be_visible()
    expect(page.get_by_text("Your order has been dispatched")).to_be_visible()
