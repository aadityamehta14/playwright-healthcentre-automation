from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_page_title(page: Page):
    home = HomePage(page)
    home.open()
    expect(page).to_have_title("HealthCentreApp")


def test_page_url(page: Page):
    home = HomePage(page)
    home.open()
    expect(page).to_have_url("https://healthcentreapp.netlify.app/")