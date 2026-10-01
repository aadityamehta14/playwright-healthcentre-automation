from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_premium_plan_link_is_visible(page: Page):
    home = HomePage(page)
    home.open()

    premium_plan_link = home.explore_premium_link()

    expect(premium_plan_link).to_be_visible()
    expect(premium_plan_link).to_have_attribute("href", "/plans/premium")


def test_premium_plan_link_navigates_to_premium_plan(page: Page):
    home = HomePage(page)
    home.open()
    home.explore_premium_link().click()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/premium")