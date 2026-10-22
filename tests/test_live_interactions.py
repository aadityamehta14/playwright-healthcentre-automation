import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


@pytest.mark.live_site
def test_standard_plan_care_record_card_requires_login(page: Page):
    plan = BasePage(page).open("/plans/standard")
    base_url = plan.base_url

    care_record_card = page.get_by_role("button", name="CareRecord", exact=False)
    expect(care_record_card).to_be_visible()
    care_record_card.click()

    expect(page).to_have_url(f"{base_url}/login")
    expect(page.get_by_role("heading", name="Log In", exact=True)).to_be_visible()
    expect(page.get_by_placeholder("you@example.com")).to_be_visible()


@pytest.mark.live_site
def test_premium_ai_careassist_requires_login_before_opening(page: Page):
    plan = BasePage(page).open("/plans/premium")
    base_url = plan.base_url

    care_assist_card = page.locator("article").filter(
        has=page.get_by_role("heading", name="AI CareAssist", exact=True)
    )
    expect(care_assist_card).to_be_visible()
    care_assist_card.click()

    expect(page).to_have_url(f"{base_url}/login-signup?mode=login")
    expect(page.get_by_role("heading", name="Log In", exact=True)).to_be_visible()
    email = page.get_by_placeholder("you@example.com")
    expect(email).to_be_visible()
    expect(email).to_have_attribute("type", "email")
    expect(email).to_have_attribute("required", "")

    email.fill("not-an-email")
    assert email.evaluate("(element) => element.validity.typeMismatch")


@pytest.mark.live_site
def test_facility_search_requires_a_region_before_enabling_city(page: Page):
    base_url = BasePage(page).base_url
    page.goto(f"{base_url}/select-facility", wait_until="domcontentloaded", timeout=60000)

    chemist = page.get_by_role("checkbox", name="Chemists", exact=True).first
    chemist.check()
    expect(chemist).to_be_checked()

    next_button = page.get_by_role("button", name="Next", exact=True)
    next_button.focus()
    page.keyboard.press("Enter")

    expect(page).to_have_url(f"{base_url}/choose-location")
    expect(page.get_by_role("heading", name="Where are you searching?", exact=True)).to_be_visible()

    city = page.get_by_role("button", name="City / Area (Optional)")
    expect(city).to_be_disabled()

    page.get_by_role("button", name="State / Region / Province").click()
    page.get_by_text("Lagos", exact=True).click()

    expect(city).to_be_enabled()


@pytest.mark.live_site
@pytest.mark.parametrize(
    ("path", "heading", "feature_names"),
    [
        (
            "/plans/standard",
            "Standard Digital Health Plan",
            ["CareRecord", "Medication", "MyLabTests", "MySymptoms", "CareChat", "CareSecure"],
        ),
        (
            "/plans/premium",
            "Premium Digital Health Plan",
            ["AI CareAssist", "CareMonitor", "RemoteCare", "ChildHealth", "CDHA Support", "PDHO Support"],
        ),
    ],
)
@pytest.mark.parametrize("viewport_width", [390, 768, 1440])
def test_standard_and_premium_plans_are_usable_at_common_viewports(
    page: Page, path: str, heading: str, feature_names: list[str], viewport_width: int
):
    plan = BasePage(page)
    base_url = plan.base_url
    page.set_viewport_size({"width": viewport_width, "height": 900})
    plan.open(path)

    expect(page.get_by_role("heading", name=heading, exact=True)).to_be_visible()
    for feature_name in feature_names:
        expect(page.get_by_role("heading", name=feature_name, exact=True)).to_be_visible()

    page_widths = page.evaluate(
        "() => ({viewport: document.documentElement.clientWidth, content: document.documentElement.scrollWidth})"
    )
    assert page_widths["content"] <= page_widths["viewport"], (
        f"{path} overflows horizontally at {viewport_width}px: {page_widths}"
    )
