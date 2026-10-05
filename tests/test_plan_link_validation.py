from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_all_plan_links_have_expected_routes(page: Page):
    home = HomePage(page)
    home.open()

    expect(home.explore_free_link()).to_have_attribute("href", "/plans/free")
    expect(home.explore_standard_link()).to_have_attribute("href", "/plans/standard")
    expect(home.explore_premium_link()).to_have_attribute("href", "/plans/premium")


def test_all_plan_links_are_unique_and_visible(page: Page):
    home = HomePage(page)
    home.open()

    free = home.explore_free_link()
    standard = home.explore_standard_link()
    premium = home.explore_premium_link()

    expect(free).to_be_visible()
    expect(standard).to_be_visible()
    expect(premium).to_be_visible()

    assert free.get_attribute("href") != standard.get_attribute("href")
    assert standard.get_attribute("href") != premium.get_attribute("href")
    assert free.get_attribute("href") != premium.get_attribute("href")
