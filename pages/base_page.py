from playwright.sync_api import Page


class BasePage:
    """Common browser/page helpers shared by the tests."""

    def __init__(self, page: Page, base_url: str = "https://healthcentreapp.netlify.app/"):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/"):
        self.page.goto(
            f"{self.base_url}{path}",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        return self
