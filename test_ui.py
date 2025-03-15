import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have
from selene.core.query import value

LOGIN = "linus@torvalds.org"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


def test_login_through_api():
    with allure.step("Login with API"):
        result = requests.post(
            url=API_URL + "login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_add_and_remove_item_to_cart():
    with allure.step("Add product to cart via API"):
        payload = "addtocart_43.EnteredQuantity: 1"
        result = requests.post(
            url=API_URL + "addproducttocart/details/43/1",
            data=payload,
            headers={'Accept': 'application/json'}
        )
        allure.attach(body=result.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")

    with allure.step("Check item visibility in cart"):
        browser.element("[class='page shopping-cart-page'").should(have.text("Smartphone"))

    with allure.step("Delete item from cart"):
        item_value = browser.element("[name='removefromcart']").get(value)
        payload = {f"removefromcart": {item_value},
                   "updatecart": 'Update shopping cart',
                   "discountcouponcode": '',
                   "giftcardcouponcode": '',
                   }
        result = requests.post(API_URL + "cart", data=payload)
        cookie = result.cookies.get("Nop.customer")
        allure.attach(body=result.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
        browser.open(WEB_URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")
        browser.element("[class='page shopping-cart-page']").should(have.text("Your Shopping Cart is empty!"))
