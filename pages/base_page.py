from playwright.sync_api import Page


class BasePage:
    """Common browser/page helpers shared by the tests."""

    def __init__(self, page: Page, base_url: str = "https://healthcentreapp.netlify.app/"):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/"):
        url = f"{self.base_url}{path}"
        last_error = None

        for attempt in range(3):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                return self
            except Exception as exc:  # pragma: no cover - retry for flaky external page load
                last_error = exc
                self.page.wait_for_timeout(2000)

        raise last_error
