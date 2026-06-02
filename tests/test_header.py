"""
Tests for the TicketHeader component: ticket ID display, status cycling,
priority dropdown, and export functionality.
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


def test_ticket_id_visible_in_header(page):
    expect(page.locator("span.font-mono.font-semibold").first).to_be_visible()


def test_ticket_id_matches_emo_pattern(page):
    id_text = page.locator("span.font-mono.font-semibold").first.text_content()
    assert re.match(r"EMO-\d{4}", id_text), f"Unexpected ticket ID format: {id_text}"


def test_priority_badge_visible(page):
    badge = _get_priority_badge(page)
    expect(badge).to_be_visible()


def test_status_badge_shows_open_on_new_ticket(page):
    expect(page.get_by_title("Click to change status")).to_contain_text("OPEN")


def test_status_cycles_open_to_in_progress(page):
    page.get_by_title("Click to change status").click()
    expect(page.get_by_title("Click to change status")).to_contain_text("IN PROGRESS")


def test_status_cycles_in_progress_to_resolved(page):
    page.get_by_title("Click to change status").click()
    page.get_by_title("Click to change status").click()
    expect(page.get_by_title("Click to change status")).to_contain_text("RESOLVED")


def test_status_cycles_resolved_back_to_open(page):
    for _ in range(3):
        page.get_by_title("Click to change status").click()
    expect(page.get_by_title("Click to change status")).to_contain_text("OPEN")


def test_priority_dropdown_opens_on_hover(page):
    badge = _get_priority_badge(page)
    badge.hover()
    expect(page.get_by_text("🟢 LOW — I'm fine, probably")).to_be_visible()


def test_priority_dropdown_shows_all_options(page):
    badge = _get_priority_badge(page)
    badge.hover()
    for label in PRIORITY_LABELS.values():
        expect(page.get_by_text(label)).to_be_visible()


def test_priority_change_to_critical(page):
    badge = _get_priority_badge(page)
    badge.hover()
    page.get_by_text(PRIORITY_LABELS["CRITICAL"]).click()
    expect(page.get_by_role("button", name="CRITICAL", exact=True).first).to_be_visible()


def test_priority_change_to_low(page):
    badge = _get_priority_badge(page)
    badge.hover()
    page.get_by_text(PRIORITY_LABELS["LOW"]).click()
    expect(page.get_by_role("button", name="LOW", exact=True).first).to_be_visible()


def test_export_button_visible(page):
    expect(page.get_by_title("Export ticket as Markdown")).to_be_visible()


def test_export_triggers_download(page_with_message):
    with page_with_message.expect_download() as download_info:
        page_with_message.get_by_title("Export ticket as Markdown").click()
    download = download_info.value
    assert re.match(r"EMO-\d{4}\.md", download.suggested_filename), (
        f"Unexpected filename: {download.suggested_filename}"
    )


def test_export_without_messages_still_works(page):
    with page.expect_download() as download_info:
        page.get_by_title("Export ticket as Markdown").click()
    download = download_info.value
    assert download.suggested_filename.endswith(".md")
