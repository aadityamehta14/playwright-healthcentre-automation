import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


RESPONSIVE_PAGES = [
    ("/", "Find Medical Facilities Near You"),
    ("/news", "HealthCentre News & Insights"),
    ("/about-us", "Digital Health Built from Experience"),
    ("/published-reviews", "What people are saying"),
    ("/contact-us", "Contact Us"),
    ("/location-services", "Find Medical Facilities"),
    ("/careers", "Become a Community Digital Health Assistant (CDHA)"),
    ("/pdho", "Partner Digital Health Organisation (PDHO)"),
]

VIEWPORTS = [
    pytest.param("mobile", 390, 844, id="mobile"),
    pytest.param("tablet", 768, 1024, id="tablet"),
    pytest.param("desktop", 1440, 900, id="desktop"),
]


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


def test_plan_links_remain_visible_on_mobile(page: Page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto("https://healthcentreapp.netlify.app/")

    expect(page.get_by_role("link", name="Explore Free")).to_be_visible()
    expect(page.get_by_role("link", name="Explore Standard")).to_be_visible()
    expect(page.get_by_role("link", name="Explore Premium")).to_be_visible()


@pytest.mark.live_site
@pytest.mark.parametrize(("path", "expected_heading"), RESPONSIVE_PAGES)
@pytest.mark.parametrize(("device_type", "width", "height"), VIEWPORTS)
def test_deployed_pages_are_responsive(
    page: Page,
    path: str,
    expected_heading: str,
    device_type: str,
    width: int,
    height: int,
):
    page.set_viewport_size({"width": width, "height": height})
    base_url = BasePage(page).base_url
    response = page.goto(
        f"{base_url}{path}",
        wait_until="domcontentloaded",
        timeout=60000,
    )

    assert response is not None
    assert response.ok, f"{path} returned HTTP {response.status} on {device_type}"
    expect(page).to_have_url(f"{base_url}{path}")
    expect(
        page.get_by_role("heading", name=expected_heading, exact=True)
    ).to_be_visible(timeout=30000)

    no_horizontal_overflow = page.evaluate(
        "() => document.documentElement.scrollWidth <= document.documentElement.clientWidth"
    )
    assert no_horizontal_overflow, (
        f"{path} has horizontal overflow at {width}x{height} ({device_type})"
    )
