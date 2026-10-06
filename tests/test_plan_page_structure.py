from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_homepage_has_all_plan_links_in_pricing_section(page: Page):
    home = HomePage(page)
    home.open()

    plan_links = home.plan_links()

    expect(plan_links).to_have_count(3)
    expect(plan_links.nth(0)).to_have_attribute("href", "/plans/free")
    expect(plan_links.nth(1)).to_have_attribute("href", "/plans/standard")
    expect(plan_links.nth(2)).to_have_attribute("href", "/plans/premium")
