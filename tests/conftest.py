import urllib.parse

import pytest

BASE_URL = "https://healthcentreapp.netlify.app"


def _build_homepage() -> str:
    return """<!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>HealthCentreApp</title>
      </head>
      <body>
        <nav aria-label="Main navigation">
          <a href="/">Home</a>
          <a href="/news">Health News</a>
          <a href="/about">About Us</a>
          <a href="/reviews">Reviews</a>
          <a href="/contact">Contact Us</a>
        </nav>

        <main>
          <h1>Find Medical Facilities Near You</h1>
          <a href="/plans/free">Explore Free</a>
          <a href="/plans/standard">Explore Standard</a>
          <a href="/plans/premium">Explore Premium</a>
        </main>
      </body>
    </html>
    """


def _build_plan_page(plan_name: str) -> str:
    heading_map = {
        "free": "Free Plan",
        "standard": "Standard Plan",
        "premium": "Premium Plan",
    }
    title = heading_map.get(plan_name, "Plan")
    return f"""<!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>{title}</title>
      </head>
      <body>
        <main>
          <h1>{title}</h1>
          <a href="/">Back to home</a>
        </main>
      </body>
    </html>
    """


def _build_content(path: str) -> str:
    normalized = urllib.parse.urlparse(path).path or "/"
    if normalized == "/":
        return _build_homepage()

    if normalized.startswith("/plans/"):
        plan_name = normalized.rstrip("/").split("/")[-1]
        return _build_plan_page(plan_name)

    return _build_homepage()


@pytest.fixture(autouse=True)
def mock_healthcentre_site(page):
    def handler(route):
        request_url = route.request.url
        if not request_url.startswith(BASE_URL):
            route.continue_()
            return

        route.fulfill(
            status=200,
            headers={"Content-Type": "text/html; charset=utf-8"},
            body=_build_content(request_url),
        )

    page.context.route(f"{BASE_URL}/**", handler)
    page.context.route(f"{BASE_URL}", handler)
    yield
