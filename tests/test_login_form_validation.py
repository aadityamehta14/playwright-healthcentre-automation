import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


@pytest.mark.live_site
def test_login_form_validates_required_fields_and_email_format(page: Page):
    base_url = BasePage(page).base_url
    response = page.goto(
        f"{base_url}/login-signup?mode=login",
        wait_until="commit",
        timeout=60000,
    )

    assert response is not None
    assert response.ok
    expect(page.get_by_role("heading", name="Log In", exact=True)).to_be_visible(
        timeout=60000
    )

    email = page.get_by_placeholder("you@example.com")
    password = page.get_by_placeholder("Enter your password")

    for field in [email, password]:
        expect(field).to_have_attribute("required", "")
        assert field.evaluate("(element) => element.validity.valueMissing")

    expect(email).to_have_attribute("type", "email")
    email.fill("not-an-email")
    assert email.evaluate("(element) => element.validity.typeMismatch")

    email.fill("member@example.com")
    assert email.evaluate("(element) => element.checkValidity()")
    assert not password.evaluate("(element) => element.checkValidity()")

    password.fill("Test-password-123")
    assert password.evaluate("(element) => element.checkValidity()")
