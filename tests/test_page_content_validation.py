import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.plan_page import PlanPage


@pytest.mark.parametrize(
    ("link_name", "expected_path"),
    [
        ("Home", "/"),
        ("Health News", "/news"),
        ("About Us", "/about-us"),
        ("Reviews", "/published-reviews"),
        ("Contact Us", "/contact-us"),
    ],
)
def test_homepage_navigation_links_have_expected_routes(
    page: Page, link_name: str, expected_path: str
):
    home = HomePage(page)
    home.open()

    expect(home.navigation_link(link_name)).to_be_visible()
    expect(home.navigation_link(link_name)).to_have_attribute("href", expected_path)


@pytest.mark.parametrize(
    ("plan_name", "expected_heading"),
    [
        ("free", "Free Plan"),
        ("standard", "Standard Plan"),
        ("premium", "Premium Plan"),
    ],
)
def test_plan_page_has_matching_title_heading_and_home_link(
    page: Page, plan_name: str, expected_heading: str
):
    plan = PlanPage(page, plan_name)
    plan.open_plan()

    expect(page).to_have_title(expected_heading)
    expect(plan.heading()).to_have_text(expected_heading)
    expect(plan.back_home_link()).to_be_visible()
    expect(plan.back_home_link()).to_have_attribute("href", "/")
