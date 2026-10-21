import pytest
from playwright.sync_api import Page, expect


SIGNUP_URL = "https://healthcentreapp.netlify.app/login-signup?mode=signup"


@pytest.mark.live_site
def test_signup_form_validates_required_fields_and_email_format(page: Page):
    response = page.goto(SIGNUP_URL, wait_until="commit", timeout=60000)
    assert response is not None
    assert response.ok
    expect(page.get_by_role("heading", name="Create your account")).to_be_visible(
        timeout=60000
    )

    for placeholder in [
        "Your first name",
        "Your surname",
        "you@example.com",
        "Enter email again",
    ]:
        field = page.get_by_placeholder(placeholder)
        expect(field).to_be_visible()
        expect(field).to_have_attribute("required", "")
        assert field.evaluate("(element) => element.validity.valueMissing")

    email = page.get_by_placeholder("you@example.com")
    expect(email).to_have_attribute("type", "email")

    email.fill("not-an-email")
    assert email.evaluate("(element) => element.validity.typeMismatch")

    email.fill("member@example.com")
    assert email.evaluate("(element) => element.checkValidity()")


@pytest.mark.live_site
def test_signup_rejects_mismatched_email_addresses(page: Page):
    response = page.goto(SIGNUP_URL, wait_until="commit", timeout=60000)
    assert response is not None
    assert response.ok
    expect(page.get_by_role("heading", name="Create your account")).to_be_visible(
        timeout=60000
    )

    # Block requests after page load so this validation test cannot create an account.
    page.route("**/*", lambda route: route.abort())

    page.get_by_placeholder("Your first name").fill("Test")
    page.get_by_placeholder("Your surname").fill("Member")
    page.get_by_placeholder("you@example.com").fill("member@example.com")
    page.get_by_placeholder("Enter email again").fill("different@example.com")
    page.get_by_role("button", name="Create Account").click()

    expect(page.get_by_text("Email addresses do not match.", exact=True)).to_be_visible(
        timeout=10000
    )
    expect(page).to_have_url(SIGNUP_URL)
