from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_free_plan_link_is_visible(page: Page):
    home = HomePage(page)
    home.open()

    free_plan_link = home.explore_free_link()

    expect(free_plan_link).to_be_visible()
    expect(free_plan_link).to_have_attribute("href", "/plans/free")