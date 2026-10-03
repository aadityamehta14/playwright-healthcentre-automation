import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "width,height",
    [
        (390, 844),
        (768, 1024),
        (1440, 900),
    ],
)
def test_homepage_is_responsive(page: Page, width: int, height: int):
    page.set_viewport_size({"width": width, "height": height})
    page.goto("https://healthcentreapp.netlify.app/")

    expect(page).to_have_url("https://healthcentreapp.netlify.app/")
    expect(page.locator("h1")).to_be_visible()

    no_horizontal_scroll = page.evaluate(
        "() => document.documentElement.scrollWidth <= window.innerWidth"
    )
    assert no_horizontal_scroll
