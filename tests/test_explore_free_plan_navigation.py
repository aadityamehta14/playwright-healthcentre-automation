from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_explore_free_link_navigates_to_free_plan(page: Page):
    home = HomePage(page)
    home.open()
    home.click_explore_free()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/free")
    expect(page.get_by_role("heading", name="Free Plan")).to_be_visible()


def test_browser_back_returns_from_free_plan_to_homepage(page: Page):
    home = HomePage(page)
    home.open()
    home.click_explore_free()

    page.go_back()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/")
    expect(HomePage(page).heading()).to_be_visible()