import os

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Common browser/page helpers shared by the tests."""

    def __init__(self, page: Page, base_url: str | None = None):
        self.page = page
        self.base_url = (
            base_url or os.getenv("HEALTHCENTRE_BASE_URL", "https://healthcentreapp.netlify.app/")
        ).rstrip("/")

    def open(self, path: str = "/"):
        url = f"{self.base_url}{path}"
        last_error = None

        for _ in range(3):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                return self
            except Exception as exc:  # pragma: no cover - retry for flaky external page load
                last_error = exc
                self.page.wait_for_timeout(2000)

        raise last_error

    def reload(self):
        self.page.reload(wait_until="domcontentloaded", timeout=60000)
        return self

    def heading(self) -> Locator:
        return self.page.get_by_role("heading", level=1)

    def assert_loaded(self, *, expected_title: str | None = None, expected_path: str | None = None):
        if expected_title is not None:
            expect(self.page).to_have_title(expected_title)

        if expected_path is not None:
            expect(self.page).to_have_url(f"{self.base_url}{expected_path}")

        expect(self.heading()).to_be_visible()
        return self

    def link_named(self, name: str):
        return self.page.get_by_role("link", name=name, exact=True)

    def assert_link(self, name: str, href: str | None = None):
        link = self.link_named(name)
        expect(link).to_be_visible()
        if href is not None:
            expect(link).to_have_attribute("href", href)
        return link
