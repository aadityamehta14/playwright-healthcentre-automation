import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.home_page import HomePage


@pytest.mark.parametrize(
    ("link_name", "expected_path", "expected_heading"),
    [
        ("Home", "/", "Find Medical Facilities Near You"),
        ("Health News", "/news", "HealthCentre News & Insights"),
        ("About Us", "/about-us", "Digital Health Built from Experience"),
        ("Reviews", "/published-reviews", "What people are saying"),
        ("Contact Us", "/contact-us", "Contact Us"),
    ],
)
def test_main_navigation_page_opens_and_reloads(
    page: Page, link_name: str, expected_path: str, expected_heading: str
):
    home = HomePage(page).open()

    home.navigation_link(link_name).click()

    expect(page).to_have_url(f"{home.base_url}{expected_path}")
    expect(BasePage(page).heading()).to_have_text(expected_heading)

    BasePage(page).reload()

    expect(page).to_have_url(f"{home.base_url}{expected_path}")
    expect(BasePage(page).heading()).to_have_text(expected_heading)
