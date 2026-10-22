import os
import re
from collections.abc import Iterator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, expect

from pages.base_page import BasePage


@pytest.fixture
def authenticated_page(browser: Browser) -> Iterator[Page]:
    storage_state = os.getenv("HEALTHCENTRE_STORAGE_STATE")
    if not storage_state:
        pytest.skip("Set HEALTHCENTRE_STORAGE_STATE to a dedicated test-account state file.")

    state_path = Path(storage_state)
    if not state_path.is_file():
        pytest.fail(f"HEALTHCENTRE_STORAGE_STATE file does not exist: {state_path}")

    context = browser.new_context(storage_state=str(state_path))
    page = context.new_page()
    yield page
    context.close()


@pytest.mark.live_site
def test_child_health_timeline_and_guardians_sections_navigate(
    authenticated_page: Page,
):
    base = BasePage(authenticated_page)
    base.open("/premium/child-health")

    authenticated_page.get_by_role(
        "button", name=re.compile("Longitudinal Health Timeline")
    ).click()
    expect(authenticated_page).to_have_url(
        f"{base.base_url}/premium/child-health/timeline"
    )
    expect(
        authenticated_page.get_by_role(
            "heading", name="Child Health Timeline", exact=True
        )
    ).to_be_visible()

    authenticated_page.get_by_role(
        "button", name="Guardians & Transition", exact=True
    ).click()
    expect(authenticated_page).to_have_url(
        f"{base.base_url}/premium/child-health/account"
    )
    expect(
        authenticated_page.get_by_role(
            "heading", name="Guardians & Transition Control", exact=True
        )
    ).to_be_visible()

    authenticated_page.get_by_role(
        "button", name="View Lifetime Timeline", exact=True
    ).click()
    expect(authenticated_page).to_have_url(
        f"{base.base_url}/premium/child-health/timeline"
    )
    expect(
        authenticated_page.get_by_role(
            "heading", name="Child Health Timeline", exact=True
        )
    ).to_be_visible()


@pytest.mark.live_site
def test_child_health_timeline_filters_and_search_are_interactive(
    authenticated_page: Page,
):
    base = BasePage(authenticated_page)
    base.open("/premium/child-health/timeline")

    growth_filter = authenticated_page.get_by_role("button", name=re.compile("^Growth"))
    all_records_filter = authenticated_page.get_by_role(
        "button", name=re.compile("^All Records")
    )
    expect(growth_filter).to_be_visible()
    expect(all_records_filter).to_be_visible()
    growth_filter.click()
    expect(growth_filter).to_have_class(re.compile("bg-orange-500"))
    expect(all_records_filter).not_to_have_class(re.compile("bg-orange-500"))

    search = authenticated_page.get_by_role(
        "textbox", name="Search clinical events..."
    )
    search.fill("automation-no-matching-clinical-event")
    expect(
        authenticated_page.get_by_text("No records match your filter", exact=True)
    ).to_be_visible()
    search.clear()
    expect(search).to_have_value("")


@pytest.mark.live_site
def test_growth_measurement_requires_weight_and_does_not_save_empty_form(
    authenticated_page: Page,
):
    base = BasePage(authenticated_page)
    base.open("/premium/child-health/growth")

    authenticated_page.get_by_role("button", name="Add measurement").click()
    dialog = authenticated_page.get_by_role("dialog", name="Add growth measurement")
    expect(dialog).to_be_visible()

    date_field = dialog.locator('input[type="date"]')
    weight_field = dialog.locator('input[type="number"]').first
    expect(date_field).to_have_attribute("required", "")
    expect(weight_field).to_have_attribute("required", "")
    assert not weight_field.evaluate("(element) => element.checkValidity()")

    authenticated_page.get_by_role("button", name="Save measurement").click()
    expect(dialog).to_be_visible()
    assert not weight_field.evaluate("(element) => element.checkValidity()")

    authenticated_page.get_by_role("button", name="Close").click()
    expect(dialog).to_have_count(0)


@pytest.mark.live_site
def test_immunisation_record_dialog_can_be_cancelled_without_saving(
    authenticated_page: Page,
):
    base = BasePage(authenticated_page)
    base.open("/premium/child-health/immunisation")

    authenticated_page.get_by_role("button", name="Add Vaccine Record").click()
    dialog = authenticated_page.get_by_role("dialog", name="Add immunisation record")
    expect(dialog).to_be_visible()
    expect(
        dialog.get_by_role("heading", name="Add Vaccine Record", exact=True)
    ).to_be_visible()

    authenticated_page.get_by_role("button", name="Cancel", exact=True).click()
    expect(dialog).to_have_count(0)
    expect(
        authenticated_page.get_by_role(
            "heading", name="Immunisation Tracker", exact=False
        )
    ).to_be_visible()


@pytest.mark.live_site
def test_child_health_care_guidance_page_opens_from_dashboard(
    authenticated_page: Page,
):
    base = BasePage(authenticated_page)
    base.open("/premium/child-health")

    authenticated_page.get_by_role("button", name="View Care Guidance").click()
    expect(authenticated_page).to_have_url(
        f"{base.base_url}/premium/child-health/newborn-care"
    )
    expect(
        authenticated_page.get_by_role(
            "heading", name=re.compile("Clinical Care Guidance")
        )
    ).to_be_visible()
