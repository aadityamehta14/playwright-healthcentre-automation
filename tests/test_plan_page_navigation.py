import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.plan_page import PlanPage


@pytest.mark.parametrize("plan_name", ["free", "standard", "premium"])
def test_plan_page_back_to_home_navigation(page: Page, plan_name: str):
    plan = PlanPage(page, plan_name)
    plan.open_plan()

    plan.back_home_link().click()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/")
    expect(HomePage(page).heading()).to_be_visible()


@pytest.mark.parametrize(
    ("plan_name", "expected_heading"),
    [
        ("free", "Free Plan"),
        ("standard", "Standard Plan"),
        ("premium", "Premium Plan"),
    ],
)
def test_reloading_plan_page_keeps_the_same_plan_open(
    page: Page, plan_name: str, expected_heading: str
):
    plan = PlanPage(page, plan_name).open_plan()

    plan.reload()

    expect(page).to_have_url(
        f"https://healthcentreapp.netlify.app/plans/{plan_name}"
    )
    expect(plan.heading()).to_have_text(expected_heading)
