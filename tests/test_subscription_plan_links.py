from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_subscription_plan_links_are_visible(page: Page):
    home = HomePage(page)
    home.open()

    expect(home.explore_free_link()).to_be_visible()
    expect(home.explore_standard_link()).to_be_visible()
    expect(home.explore_premium_link()).to_be_visible()