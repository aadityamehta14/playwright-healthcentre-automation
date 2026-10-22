import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.plan_page import PlanPage


@pytest.mark.parametrize(
    ("plan_name", "expected_heading", "expected_path"),
    [
        ("free", "Free Plan", "/plans/free"),
        ("standard", "Standard Plan", "/plans/standard"),
        ("premium", "Premium Plan", "/plans/premium"),
    ],
)
def test_plan_links_navigate_to_expected_pages_and_keep_correct_heading(
    page: Page, plan_name: str, expected_heading: str, expected_path: str
):
    home = HomePage(page)
    home.open()

    home.assert_link(f"Explore {expected_heading.split()[0]}", expected_path)
    home.get_by_role = home.page.get_by_role
    home.page.get_by_role("link", name=f"Explore {expected_heading.split()[0]}").click()

    plan = PlanPage(page, plan_name)
    expect(page).to_have_url(f"https://healthcentreapp.netlify.app{expected_path}")
    expect(plan.heading()).to_have_text(expected_heading)
    expect(plan.back_home_link()).to_be_visible()


def test_homepage_navigation_links_are_all_visible_and_unique(page: Page):
    home = HomePage(page)
    home.open()

    expected = ["Home", "Health News", "About Us", "Reviews", "Contact Us"]
    visible_links = [home.navigation_link(name) for name in expected]

    for link in visible_links:
        expect(link).to_be_visible()

    hrefs = [link.get_attribute("href") for link in visible_links]
    assert len(set(hrefs)) == len(hrefs)


def test_homepage_main_heading_and_plan_actions_are_ready_for_user_flow(page: Page):
    home = HomePage(page)
    home.open()

    expect(home.heading()).to_have_text("Find Medical Facilities Near You")
    expect(home.plan_links()).to_have_count(3)

    home.explore_standard_link().click()
    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/standard")
    expect(page.locator("h1")).to_have_text("Standard Plan")

    page.go_back()
    expect(page).to_have_url("https://healthcentreapp.netlify.app/")
    expect(home.heading()).to_be_visible()
