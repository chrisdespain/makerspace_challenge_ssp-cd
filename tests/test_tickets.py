"""
Tests for ticket lifecycle: draft state on load, ticket creation on the
first message, selection, and deletion.

A ticket does not exist until the first message is submitted. Before that the
app is in a "draft" state (no EMO ID, no sidebar entry, no header).
"""
from playwright.sync_api import expect
from tests.constants import MOCK_REPLY


def _submit(page, text):
    """Submit a message and wait for the mocked agent reply."""
    page.locator("textarea").fill(text)
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")


def test_no_ticket_on_load(page):
    """Input: open the app. Expected: draft state — the open-a-ticket prompt shows and no ticket is listed."""
    expect(page.get_by_text("Describe your issue to open a ticket")).to_be_visible()
    expect(page.locator("aside .font-mono")).to_have_count(0)


def test_suggested_issues_visible_in_draft(page):
    """Input: open the app (draft). Expected: the 'Common issues' prompt strip is visible."""
    expect(page.get_by_text("Common issues — select one to file immediately:")).to_be_visible()


def test_new_ticket_button_visible(page):
    """Input: open the app. Expected: the 'New Ticket' button is visible."""
    expect(page.get_by_role("button", name="New Ticket")).to_be_visible()


def test_first_message_creates_ticket_id(page):
    """Input: submit a first message. Expected: a ticket ID in the form EMO-#### appears."""
    _submit(page, "My first issue")
    expect(page.locator("text=/EMO-\\d{4}/").first).to_be_visible()


def test_first_message_creates_sidebar_entry(page):
    """Input: submit a first message. Expected: one ticket entry appears in the sidebar."""
    _submit(page, "My first issue")
    expect(page.locator("aside .font-mono")).to_have_count(1)


def test_new_ticket_button_returns_to_draft(page):
    """Input: file a ticket, then click 'New Ticket'. Expected: draft returns and no new sidebar entry is added until the next submit."""
    _submit(page, "My first issue")
    expect(page.locator("aside .font-mono")).to_have_count(1)
    page.get_by_role("button", name="New Ticket").click()
    expect(page.get_by_text("Describe your issue to open a ticket")).to_be_visible()
    expect(page.locator("aside .font-mono")).to_have_count(1)


def test_ticket_title_updates_after_first_message(page):
    """Input: submit a first message. Expected: the sidebar entry's title is that message."""
    _submit(page, "Memory leak in my personal life")
    expect(page.locator("aside").get_by_text("Memory leak in my personal life")).to_be_visible()


def test_select_different_ticket_switches_active(page):
    """Input: file two tickets, then click the older one in the sidebar. Expected: its ID becomes the active header ID."""
    _submit(page, "First ticket")
    page.get_by_role("button", name="New Ticket").click()
    _submit(page, "Second ticket")
    # Newest is on top, so the older "First ticket" is the second sidebar entry.
    older_id = page.locator("aside .font-mono").nth(1).text_content()
    page.locator("aside .font-mono").nth(1).click()
    expect(page.locator(f"text={older_id}").first).to_be_visible()


def test_selecting_ticket_shows_its_messages(page):
    """Input: file two tickets, then switch between them. Expected: each thread shows only its own message."""
    _submit(page, "Original ticket message")
    page.get_by_role("button", name="New Ticket").click()
    _submit(page, "Second ticket message")
    thread = page.get_by_test_id("ticket-thread")
    # Currently viewing the second ticket: the first ticket's message is not in this thread.
    expect(thread.get_by_text("Original ticket message")).not_to_be_visible()
    # Switch to the first ticket (older entry, index 1).
    page.locator("aside .font-mono").nth(1).click()
    expect(thread.get_by_text("Original ticket message")).to_be_visible()


def test_delete_ticket_removes_from_sidebar(page):
    """Input: with two filed tickets, close one. Expected: the sidebar count drops by one."""
    _submit(page, "First ticket")
    page.get_by_role("button", name="New Ticket").click()
    _submit(page, "Second ticket")
    expect(page.locator("aside .font-mono")).to_have_count(2)
    page.get_by_title("Close ticket").first.click(force=True)
    expect(page.locator("aside .font-mono")).to_have_count(1)


def test_delete_active_ticket_selects_next_ticket(page):
    """Input: with two filed tickets, delete the active one. Expected: another ticket stays selected (its header ID shows)."""
    _submit(page, "First ticket")
    page.get_by_role("button", name="New Ticket").click()
    _submit(page, "Second ticket")
    page.get_by_title("Close ticket").first.click(force=True)
    expect(page.locator("text=/EMO-\\d{4}/").first).to_be_visible()
    expect(page.locator("aside .font-mono")).to_have_count(1)


def test_delete_last_ticket_returns_to_draft(page):
    """Input: file one ticket, then delete it. Expected: draft state returns (no auto-created replacement)."""
    _submit(page, "Only ticket")
    page.get_by_title("Close ticket").first.click(force=True)
    expect(page.get_by_text("Describe your issue to open a ticket")).to_be_visible()
    expect(page.locator("aside .font-mono")).to_have_count(0)
