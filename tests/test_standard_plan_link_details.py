from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_standard_plan_link_is_visible(page: Page):
    home = HomePage(page)
    home.open()

    standard_plan_link = home.explore_standard_link()

    expect(standard_plan_link).to_be_visible()
    expect(standard_plan_link).to_have_attribute("href", "/plans/standard")


def test_standard_plan_link_navigates_to_standard_plan(page: Page):
    home = HomePage(page)
    home.open()
    home.explore_standard_link().click()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/standard")
