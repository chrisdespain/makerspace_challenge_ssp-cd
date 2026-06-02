"""
Tests for message submission: button click, Enter key, Shift+Enter,
suggested issues, loading indicator, and error handling.
"""
import json
from playwright.sync_api import expect
from conftest import MOCK_REPLY


def test_textarea_visible(page):
    expect(page.locator("textarea")).to_be_visible()


def test_textarea_placeholder_text(page):
    expect(page.locator("textarea")).to_have_attribute(
        "placeholder", "Describe your issue in detail. Attach feelings if applicable."
    )


def test_submit_button_disabled_when_input_empty(page):
    expect(page.get_by_role("button", name="Submit Ticket")).to_be_disabled()


def test_submit_button_enabled_when_input_filled(page):
    page.locator("textarea").fill("test input")
    expect(page.get_by_role("button", name="Submit Ticket")).to_be_enabled()


def test_submit_via_button_shows_user_message(page):
    page.locator("textarea").fill("I am overwhelmed by spreadsheets")
    page.get_by_role("button", name="Submit Ticket").click()
    expect(page.get_by_text("I am overwhelmed by spreadsheets")).to_be_visible()


def test_submit_via_enter_sends_message(page):
    page.locator("textarea").fill("Requesting a hotfix for my anxiety")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("Requesting a hotfix for my anxiety")).to_be_visible()


def test_shift_enter_does_not_submit(page):
    page.locator("textarea").fill("first line")
    page.locator("textarea").press("Shift+Enter")
    expect(page.get_by_text("YOU (Ticket Submitter)")).not_to_be_visible()


def test_agent_reply_appears_after_submit(page):
    page.locator("textarea").fill("My work-life balance threw a 500 error")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text(MOCK_REPLY)).to_be_visible()


def test_textarea_clears_after_submit(page):
    page.locator("textarea").fill("some message")
    page.locator("textarea").press("Enter")
    expect(page.locator("textarea")).to_have_value("")


def test_submit_button_label_changes_to_add_comment_after_first_message(page):
    page.locator("textarea").fill("first message")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_role("button", name="Add Comment")).to_be_visible()


def test_typing_indicator_appears_while_loading(page):
    def delayed_route(route):
        import time
        time.sleep(0.3)
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": "delayed reply"}),
        )

    page.route("**/api/chat", delayed_route)
    page.locator("textarea").fill("testing loading state")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("composing a response... please hold")).to_be_visible()


def test_suggested_issue_submits_on_click(page):
    page.get_by_text("My motivation has stopped responding").click()
    expect(page.get_by_text("My motivation has stopped responding")).to_be_visible()
    expect(page.get_by_text(MOCK_REPLY)).to_be_visible()


def test_all_suggested_issues_are_visible(page):
    expected = [
        "My motivation has stopped responding",
        "Unexpected feelings in production",
        "Memory leak in my personal life",
        "My work-life balance threw a 500 error",
        "Critical: imposter syndrome detected",
        "Requesting a hotfix for my anxiety",
    ]
    for issue in expected:
        expect(page.get_by_text(issue)).to_be_visible()


def test_suggested_issues_hidden_after_message_submitted(page):
    page.locator("textarea").fill("hello")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_text("Common issues — select one to file immediately:")).not_to_be_visible()


def test_api_error_shows_banner(page):
    page.route("**/api/chat", lambda route: route.fulfill(status=500))
    page.locator("textarea").fill("trigger an error")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("Could not reach support. Please try again.")).to_be_visible()


def test_dismiss_error_banner(page):
    page.route("**/api/chat", lambda route: route.fulfill(status=500))
    page.locator("textarea").fill("trigger error")
    page.locator("textarea").press("Enter")
    page.wait_for_selector("text=Could not reach support. Please try again.")
    page.get_by_title("Dismiss").click()
    expect(page.get_by_text("Could not reach support. Please try again.")).not_to_be_visible()


def test_status_changes_to_in_progress_after_first_message(page):
    page.locator("textarea").fill("opening a ticket")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_title("Click to change status")).to_contain_text("IN PROGRESS")
