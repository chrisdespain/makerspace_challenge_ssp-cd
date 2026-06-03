"""
Frontend proactive access-gate flow.

On load the app probes GET /api/access. When a code is required, a full-screen
gate is shown before the app; entering the correct code unlocks it and the code
rides along on subsequent /api/chat calls as the X-Access-Code header.
"""
import json

import pytest
from playwright.sync_api import expect

from tests.constants import BASE_URL, MOCK_REPLY


@pytest.fixture
def gated_page(page):
    """A page where the backend requires the access code 'letmein'.

    Overrides the not-required default from conftest. /api/access and /api/chat
    both validate the X-Access-Code header against 'letmein'.
    """
    def access_handler(route):
        # Playwright normalizes header names to lowercase.
        valid = route.request.headers.get("x-access-code") == "letmein"
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"required": True, "valid": valid}),
        )

    def chat_handler(route):
        if route.request.headers.get("x-access-code") == "letmein":
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"reply": MOCK_REPLY}),
            )
        else:
            route.fulfill(
                status=401,
                content_type="application/json",
                body=json.dumps({"detail": "Invalid or missing access code"}),
            )

    page.route("**/api/access", access_handler)
    page.route("**/api/chat", chat_handler)
    page.reload()  # re-probe with the now-gated backend
    return page


def test_gate_screen_shown_when_required(gated_page):
    """Input: load the app when a code is required and none is stored. Expected: the gate screen shows and the app (textarea) is hidden."""
    expect(
        gated_page.get_by_text("This app is access-restricted. Enter your access code to continue.")
    ).to_be_visible()
    expect(gated_page.locator("textarea")).to_have_count(0)


def test_wrong_code_shows_error(gated_page):
    """Input: enter a wrong code and Unlock. Expected: an 'Invalid access code' error, still gated."""
    gated_page.get_by_placeholder("Access code").fill("wrong")
    gated_page.get_by_role("button", name="Unlock").click()
    expect(gated_page.get_by_text("Invalid access code")).to_be_visible()
    expect(gated_page.locator("textarea")).to_have_count(0)


def test_correct_code_unlocks_and_app_works(gated_page):
    """Input: enter the correct code, then file a ticket. Expected: the app unlocks and a reply comes back."""
    gated_page.get_by_placeholder("Access code").fill("letmein")
    gated_page.get_by_role("button", name="Unlock").click()
    # App is now visible.
    expect(gated_page.locator("textarea")).to_be_visible()
    # And /api/chat works because the stored code rides along as the header.
    gated_page.locator("textarea").fill("hello")
    gated_page.locator("textarea").press("Enter")
    expect(gated_page.get_by_test_id("ticket-thread").get_by_text(MOCK_REPLY)).to_be_visible()


def test_no_gate_when_not_required(page):
    """Input: load with the default (not-required) backend. Expected: no gate — the app renders directly."""
    # The default `page` fixture mocks /api/access as not-required.
    expect(page.locator("textarea")).to_be_visible()
    expect(
        page.get_by_text("This app is access-restricted. Enter your access code to continue.")
    ).to_have_count(0)
