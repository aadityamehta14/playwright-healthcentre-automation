from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the HealthCentreApp homepage."""

    def __init__(self, page: Page):
        super().__init__(page)

    def heading(self):
        return self.page.locator("h1")

    def explore_free_link(self):
        return self.page.get_by_role("link", name="Explore Free")

    def explore_standard_link(self):
        return self.page.get_by_role("link", name="Explore Standard")

    def explore_premium_link(self):
        return self.page.get_by_role("link", name="Explore Premium")

    def click_explore_free(self):
        self.explore_free_link().click()
        return self
