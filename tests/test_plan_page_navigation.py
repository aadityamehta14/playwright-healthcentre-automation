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
