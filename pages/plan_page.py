from playwright.sync_api import Page

from pages.base_page import BasePage


class PlanPage(BasePage):
    """Page object for a pricing plan page."""

    def __init__(self, page: Page, plan_name: str):
        super().__init__(page)
        self.plan_name = plan_name

    def open_plan(self):
        self.page.goto(
            f"{self.base_url}/plans/{self.plan_name}",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        return self

    def heading(self):
        return self.page.locator("h1")

    def back_home_link(self):
        return self.page.get_by_role("link", name="Back to home")
