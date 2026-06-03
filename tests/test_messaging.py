"""
Tests for message submission: button click, Enter key, Shift+Enter,
suggested issues, loading indicator, and error handling.
"""
from playwright.sync_api import expect
from tests.constants import MOCK_REPLY


def test_textarea_visible(page):
    """Input: open the app. Expected: the message input box is visible."""
    expect(page.locator("textarea")).to_be_visible()


def test_textarea_placeholder_text(page):
    """Input: open the app. Expected: the input shows the 'Describe your issue...' placeholder."""
    expect(page.locator("textarea")).to_have_attribute(
        "placeholder", "Describe your issue in detail. Attach feelings if applicable."
    )


def test_submit_button_disabled_when_input_empty(page):
    """Input: open the app with an empty input. Expected: the Submit Ticket button is disabled."""
    expect(page.get_by_role("button", name="Submit Ticket")).to_be_disabled()


def test_submit_button_enabled_when_input_filled(page):
    """Input: type some text into the input. Expected: the Submit Ticket button becomes enabled."""
    page.locator("textarea").fill("test input")
    expect(page.get_by_role("button", name="Submit Ticket")).to_be_enabled()


def test_submit_via_button_shows_user_message(page):
    """Input: type a message and click Submit Ticket. Expected: the message appears in the thread."""
    page.locator("textarea").fill("I am overwhelmed by spreadsheets")
    page.get_by_role("button", name="Submit Ticket").click()
    # Scope to the thread: the text also appears in the sidebar + header titles.
    expect(
        page.get_by_test_id("ticket-thread").get_by_text("I am overwhelmed by spreadsheets")
    ).to_be_visible()


def test_submit_via_enter_sends_message(page):
    """Input: type a message and press Enter. Expected: the message appears in the thread."""
    page.locator("textarea").fill("Requesting a hotfix for my anxiety")
    page.locator("textarea").press("Enter")
    expect(
        page.get_by_test_id("ticket-thread").get_by_text("Requesting a hotfix for my anxiety")
    ).to_be_visible()


def test_shift_enter_does_not_submit(page):
    """Input: type text and press Shift+Enter. Expected: nothing is submitted (no user message)."""
    page.locator("textarea").fill("first line")
    page.locator("textarea").press("Shift+Enter")
    expect(page.get_by_text("YOU (Ticket Submitter)")).not_to_be_visible()


def test_agent_reply_appears_after_submit(page):
    """Input: submit a message (agent reply is mocked). Expected: the mocked reply appears."""
    page.locator("textarea").fill("My work-life balance threw a 500 error")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text(MOCK_REPLY)).to_be_visible()


def test_textarea_clears_after_submit(page):
    """Input: submit a message. Expected: the input box is cleared afterward."""
    page.locator("textarea").fill("some message")
    page.locator("textarea").press("Enter")
    expect(page.locator("textarea")).to_have_value("")


def test_submit_button_label_changes_to_add_comment_after_first_message(page):
    """Input: submit the first message. Expected: the button label changes to 'Add Comment'."""
    page.locator("textarea").fill("first message")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_role("button", name="Add Comment")).to_be_visible()


def test_typing_indicator_appears_while_loading(page):
    """Input: submit a message while the reply is still pending. Expected: the 'composing a response' indicator shows."""
    # Hold the /api/chat request open so the loading state persists while we
    # assert. NOTE: a blocking time.sleep() inside a sync route handler blocks
    # Playwright's own driver thread, so expect() can't poll until the response
    # is already sent and the indicator is gone. Leaving the request pending
    # (never fulfilling) keeps `loading` true without blocking the driver.
    page.route("**/api/chat", lambda route: None)
    page.locator("textarea").fill("testing loading state")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("composing a response... please hold")).to_be_visible()


def test_typing_indicator_not_shown_on_other_ticket(page):
    """Input: submit a message (reply pending), then open a New Ticket. Expected: the draft view does NOT show the other ticket's 'composing' indicator."""
    # Hold the request open so the first ticket stays in the loading state.
    page.route("**/api/chat", lambda route: None)
    page.locator("textarea").fill("waiting on this one")
    page.locator("textarea").press("Enter")
    # The indicator shows on the ticket that is actually waiting.
    expect(page.get_by_text("composing a response... please hold")).to_be_visible()
    # Switching to a fresh draft must not carry the other ticket's indicator over.
    page.get_by_role("button", name="New Ticket").click()
    expect(page.get_by_text("composing a response... please hold")).not_to_be_visible()


def test_suggested_issue_submits_on_click(page):
    """Input: click a suggested-issue pill. Expected: it is submitted and a reply appears."""
    page.get_by_text("My motivation has stopped responding").click()
    expect(
        page.get_by_test_id("ticket-thread").get_by_text("My motivation has stopped responding")
    ).to_be_visible()
    expect(page.get_by_text(MOCK_REPLY)).to_be_visible()


def test_all_suggested_issues_are_visible(page):
    """Input: open a new ticket. Expected: all six suggested-issue prompts are visible."""
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
    """Input: submit a message. Expected: the suggested-issues strip is hidden."""
    page.locator("textarea").fill("hello")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_text("Common issues — select one to file immediately:")).not_to_be_visible()


def test_api_error_shows_banner(page):
    """Input: submit a message when the API returns 500. Expected: an error banner appears."""
    page.route("**/api/chat", lambda route: route.fulfill(status=500))
    page.locator("textarea").fill("trigger an error")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("Could not reach support. Please try again.")).to_be_visible()


def test_dismiss_error_banner(page):
    """Input: trigger the error banner, then click Dismiss. Expected: the banner goes away."""
    page.route("**/api/chat", lambda route: route.fulfill(status=500))
    page.locator("textarea").fill("trigger error")
    page.locator("textarea").press("Enter")
    page.wait_for_selector("text=Could not reach support. Please try again.")
    page.get_by_title("Dismiss").click()
    expect(page.get_by_text("Could not reach support. Please try again.")).not_to_be_visible()


def test_status_changes_to_in_progress_after_first_message(page):
    """Input: submit the first message. Expected: the ticket status reads IN PROGRESS."""
    page.locator("textarea").fill("opening a ticket")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.get_by_title("Click to change status")).to_contain_text("IN PROGRESS")
