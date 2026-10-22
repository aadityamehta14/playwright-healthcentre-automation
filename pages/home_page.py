from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the HealthCentreApp homepage."""

    def __init__(self, page: Page):
        super().__init__(page)

    def navigation_link(self, name: str):
        return self.page.get_by_role("link", name=name, exact=True)

    def navigation_links(self):
        return self.page.locator("nav a")

    def explore_free_link(self):
        return self.page.get_by_role("link", name="Explore Free")

    def explore_standard_link(self):
        return self.page.get_by_role("link", name="Explore Standard")

    def explore_premium_link(self):
        return self.page.get_by_role("link", name="Explore Premium")

    def plan_links(self):
        return self.page.locator('a[href*="/plans/"]').filter(has_text="Explore")

    def click_explore_free(self):
        self.explore_free_link().click()
        return self
