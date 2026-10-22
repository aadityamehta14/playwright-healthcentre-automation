import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


DEPLOYED_PAGES = [
    ("/", "Find Medical Facilities Near You"),
    ("/news", "HealthCentre News & Insights"),
    ("/about-us", "Digital Health Built from Experience"),
    ("/published-reviews", "What people are saying"),
    ("/contact-us", "Contact Us"),
    ("/location-services", "Find Medical Facilities"),
    ("/careers", "Become a Community Digital Health Assistant (CDHA)"),
    ("/pdho", "Partner Digital Health Organisation (PDHO)"),
    ("/national-edition", "HealthCentreApp National Edition"),
    ("/voucher-info", "Gift a HealthCentreApp Subscription"),
    ("/advert-info", "Advertise on HealthCentreApp"),
    ("/refer-a-friend", "Share HealthCentreApp"),
    ("/reviews/published", "What people are saying"),
    ("/ai-help", "AI Assistant"),
    ("/terms", "Terms of Use"),
    ("/privacy", "Privacy Policy"),
    ("/cookies", "Cookie Policy"),
    ("/ai-policy", "AI Policy"),
]

HOMEPAGE_SERVICE_ROUTES = [
    "/location-services",
    "/careers",
    "/pdho",
    "/national-edition",
    "/voucher-info",
    "/advert-info",
    "/reviews/published",
    "/ai-help",
]


@pytest.mark.live_site
@pytest.mark.parametrize(("path", "expected_heading"), DEPLOYED_PAGES)
def test_deployed_page_route_loads_with_expected_heading(
    page: Page, path: str, expected_heading: str
):
    base_url = BasePage(page).base_url
    response = page.goto(
        f"{base_url}{path}",
        wait_until="domcontentloaded",
        timeout=60000,
    )

    assert response is not None
    assert response.ok, f"{path} returned HTTP {response.status}"
    expect(page).to_have_url(f"{base_url}{path}")
    expect(page.get_by_role("heading", name=expected_heading, exact=True)).to_be_visible(
        timeout=30000
    )


@pytest.mark.live_site
@pytest.mark.parametrize("path", HOMEPAGE_SERVICE_ROUTES)
def test_homepage_links_point_to_deployed_service_routes(page: Page, path: str):
    base_url = BasePage(page).base_url
    response = page.goto(base_url, wait_until="domcontentloaded", timeout=60000)

    assert response is not None
    assert response.ok, f"Homepage returned HTTP {response.status}"

    link = page.locator(f'a[href="{path}"]').first
    expect(link).to_be_visible()
    link.click()

    expect(page).to_have_url(f"{base_url}{path}")
