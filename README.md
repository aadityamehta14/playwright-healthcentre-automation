# Playwright HealthCentre Automation

A small browser automation project using Python, pytest, and Playwright. The suite is self-contained and intercepts the public demo URL so it can run even when the external site is unavailable in CI or a local environment.

## Requirements

- Python 3.12 (the version used in CI)
- No internet access is needed to run the test suite; demo-site requests are intercepted by a local fixture.

## Setup

Run these commands in PowerShell from the project root:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run tests

```powershell
python -m pytest
```

To see `print()` output from tests, use:

```powershell
python -m pytest -s
```

To run the live deployed-page checks and signup form validation checks (requires internet access):

```powershell
python -m pytest -m live_site
```

The live checks verify deployed routes and homepage links, Standard and Premium feature access/login gates (including ChildHealth), login and signup email validation, facility-search selection and dependent location fields, and plan-page layouts at phone, tablet, and desktop widths. They do not submit credentials, create an account, start an AI chat, or save facility data. ChildHealth profile-form validation requires a signed-in test account and is not part of the automated suite. The currently rendered signup form has no phone-number field, so phone validation is not covered. The regular suite continues to use local mock pages.

Set `HEALTHCENTRE_BASE_URL` when checking another deployment:

```powershell
$env:HEALTHCENTRE_BASE_URL = "https://your-deployment.example"
python -m pytest -m live_site
```

Authenticated ChildHealth interaction tests require a separate Playwright storage-state file for a dedicated test account. Do not use real patient data or commit/share the state file:

```powershell
$env:HEALTHCENTRE_STORAGE_STATE = "C:\path\to\child-health-test-account.json"
python -m pytest tests/test_live_child_health_authenticated.py -m live_site
```

Without `HEALTHCENTRE_STORAGE_STATE`, these authenticated tests are skipped. They cover read-only navigation, timeline filters/search, required-field validation for an empty growth measurement, and cancelling the vaccine-record form without saving.

## Project layout

```text
.
|-- tests/
|   |-- conftest.py
|   |-- test_explore_free_plan_navigation.py
|   |-- test_explore_standard_plan_navigation.py
|   |-- test_free_plan_link_details.py
|   |-- test_homepage.py
|   |-- test_page_content_validation.py
|   |-- test_plan_page_navigation.py
|   |-- test_page_heading.py
|   |-- test_signup_form_validation.py
|   `-- test_subscription_plan_links.py
|-- pages/                 # Reserved for future Page Object Model classes
|-- .github/workflows/
|   `-- playwright.yml
|-- requirements.txt
|-- pytest.ini
|-- .gitignore
`-- README.md
```

GitHub Actions runs the Playwright tests on pushes and pull requests. The tests use local mock pages, so they do not depend on the external demo site being available.
