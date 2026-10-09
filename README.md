# Playwright HealthCentre Automation

A small browser automation project using Python, pytest, and Playwright. The suite is self-contained and intercepts the public demo URL so it can run even when the external site is unavailable in CI or a local environment.

## Requirements

- Python 3.12 (the version used in CI)
- Internet access to reach the demo site

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

## Project layout

```text
.
|-- tests/
|   |-- test_explore_free_plan_navigation.py
|   |-- test_free_plan_link_details.py
|   |-- test_homepage.py
|   |-- test_plan_page_navigation.py
|   |-- test_page_heading.py
|   `-- test_subscription_plan_links.py
|-- pages/                 # Reserved for future Page Object Model classes
|-- .github/workflows/
|   `-- playwright.yml
|-- requirements.txt
|-- pytest.ini
|-- .gitignore
`-- README.md
```

GitHub Actions runs the Playwright tests on pushes and pull requests. The tests depend on the external demo site being available.
