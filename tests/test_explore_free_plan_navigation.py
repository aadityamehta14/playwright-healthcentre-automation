from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_explore_free_link_navigates_to_free_plan(page: Page):
    home = HomePage(page)
    home.open()
    home.click_explore_free()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/free")