from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_heading_visible(page: Page):
    home = HomePage(page)
    home.open()
    heading = home.heading()
    expect(heading).to_be_visible()
    print(heading.text_content())  # run with pytest -s to see this