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


def test_homepage_main_heading_is_visible(page: Page):
    home = HomePage(page)
    home.open()

    expect(home.heading()).to_be_visible()
    expect(home.heading()).to_contain_text("Find Medical Facilities Near You")


def test_homepage_navigation_links_are_visible(page: Page):
    home = HomePage(page)
    home.open()

    for link_name in ["Home", "Health News", "About Us", "Reviews", "Contact Us"]:
        expect(home.page.get_by_role("link", name=link_name, exact=True)).to_be_visible()


def test_homepage_plan_cards_are_visible(page: Page):
    home = HomePage(page)
    home.open()

    for plan_name in ["Explore Free", "Explore Standard", "Explore Premium"]:
        expect(home.page.get_by_role("link", name=plan_name)).to_be_visible()


def test_explore_free_button_navigates_to_free_plan(page: Page):
    home = HomePage(page)
    home.open()

    home.explore_free_link().click()

    expect(page).to_have_url("https://healthcentreapp.netlify.app/plans/free")