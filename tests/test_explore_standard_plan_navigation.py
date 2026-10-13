from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.plan_page import PlanPage


def test_explore_standard_link_opens_standard_plan(page: Page):
    home = HomePage(page)
    home.open()
    home.explore_standard_link().click()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/standard")
    expect(PlanPage(page, "standard").heading()).to_have_text("Standard Plan")
