"""
Tests for the TicketHeader component: ticket ID display, status cycling,
priority dropdown, and export functionality.

The header only renders once a ticket exists, so these tests use the
`page_with_message` fixture, which submits one message to create a ticket.
A ticket is born IN PROGRESS (it is filed together with its first message).
"""
import re
from playwright.sync_api import expect

PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
PRIORITY_LABELS = {
    "LOW": "🟢 LOW — I'm fine, probably",
    "MEDIUM": "🟡 MEDIUM — Could be worse",
    "HIGH": "🔴 HIGH — Please advise",
    "CRITICAL": "🚨 CRITICAL — Immediate emotional triage required",
}


def _get_priority_badge(page):
    """Return the visible priority badge button in the header."""
    for p in PRIORITIES:
        btn = page.get_by_role("button", name=p, exact=True)
        if btn.count() > 0:
            return btn.first
    raise AssertionError("No priority badge found in header")


def test_ticket_id_visible_in_header(page_with_message):
    """Input: a filed ticket. Expected: the ticket ID is visible in the header."""
    expect(page_with_message.locator("span.font-mono.font-semibold").first).to_be_visible()


def test_ticket_id_matches_emo_pattern(page_with_message):
    """Input: read the header ticket ID. Expected: it matches the EMO-#### format."""
    id_text = page_with_message.locator("span.font-mono.font-semibold").first.text_content()
    assert re.match(r"EMO-\d{4}", id_text), f"Unexpected ticket ID format: {id_text}"


def test_priority_badge_visible(page_with_message):
    """Input: a filed ticket. Expected: a priority badge (one of LOW/MEDIUM/HIGH/CRITICAL) is visible."""
    badge = _get_priority_badge(page_with_message)
    expect(badge).to_be_visible()


def test_status_badge_shows_in_progress_on_new_ticket(page_with_message):
    """Input: a newly filed ticket. Expected: the status badge reads IN PROGRESS."""
    expect(page_with_message.get_by_title("Click to change status")).to_contain_text("IN PROGRESS")


def test_status_cycles_in_progress_to_resolved(page_with_message):
    """Input: click the status badge once (from IN PROGRESS). Expected: it changes to RESOLVED."""
    page_with_message.get_by_title("Click to change status").click()
    expect(page_with_message.get_by_title("Click to change status")).to_contain_text("RESOLVED")


def test_status_cycles_resolved_to_open(page_with_message):
    """Input: click the status badge twice (from IN PROGRESS). Expected: it reaches OPEN."""
    page_with_message.get_by_title("Click to change status").click()
    page_with_message.get_by_title("Click to change status").click()
    expect(page_with_message.get_by_title("Click to change status")).to_contain_text("OPEN")


def test_status_cycles_back_to_in_progress(page_with_message):
    """Input: click the status badge three times (full cycle). Expected: it returns to IN PROGRESS."""
    for _ in range(3):
        page_with_message.get_by_title("Click to change status").click()
    expect(page_with_message.get_by_title("Click to change status")).to_contain_text("IN PROGRESS")


def test_priority_dropdown_opens_on_hover(page_with_message):
    """Input: hover over the priority badge. Expected: the LOW option label appears."""
    badge = _get_priority_badge(page_with_message)
    badge.hover()
    expect(page_with_message.get_by_text("🟢 LOW — I'm fine, probably")).to_be_visible()


def test_priority_dropdown_shows_all_options(page_with_message):
    """Input: hover over the priority badge. Expected: all four priority option labels appear."""
    badge = _get_priority_badge(page_with_message)
    badge.hover()
    for label in PRIORITY_LABELS.values():
        expect(page_with_message.get_by_text(label)).to_be_visible()


def test_priority_change_to_critical(page_with_message):
    """Input: open the priority dropdown and pick CRITICAL. Expected: the badge now reads CRITICAL."""
    badge = _get_priority_badge(page_with_message)
    badge.hover()
    page_with_message.get_by_text(PRIORITY_LABELS["CRITICAL"]).click()
    expect(page_with_message.get_by_role("button", name="CRITICAL", exact=True).first).to_be_visible()


def test_priority_change_to_low(page_with_message):
    """Input: open the priority dropdown and pick LOW. Expected: the badge now reads LOW."""
    badge = _get_priority_badge(page_with_message)
    badge.hover()
    page_with_message.get_by_text(PRIORITY_LABELS["LOW"]).click()
    expect(page_with_message.get_by_role("button", name="LOW", exact=True).first).to_be_visible()


def test_export_button_visible(page_with_message):
    """Input: a filed ticket. Expected: the 'Export ticket as Markdown' button is visible."""
    expect(page_with_message.get_by_title("Export ticket as Markdown")).to_be_visible()


def test_export_triggers_download(page_with_message):
    """Input: click Export on a filed ticket. Expected: a file named EMO-####.md downloads."""
    with page_with_message.expect_download() as download_info:
        page_with_message.get_by_title("Export ticket as Markdown").click()
    download = download_info.value
    assert re.match(r"EMO-\d{4}\.md", download.suggested_filename), (
        f"Unexpected filename: {download.suggested_filename}"
    )
