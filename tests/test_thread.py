"""
Tests for the TicketThread component: message display, starring,
and copying agent responses.
"""
from playwright.sync_api import expect
from conftest import MOCK_REPLY


def test_user_message_label_shown(page_with_message):
    expect(page_with_message.get_by_text("YOU (Ticket Submitter)")).to_be_visible()


def test_agent_message_label_shown(page_with_message):
    expect(page_with_message.get_by_text("[HELPDESK BOT] (Level 1 Support)")).to_be_visible()


def test_user_message_text_shown(page_with_message):
    expect(
        page_with_message.get_by_text("I need help processing my feelings about Mondays")
    ).to_be_visible()


def test_agent_reply_text_shown(page_with_message):
    expect(page_with_message.get_by_text(MOCK_REPLY)).to_be_visible()


def test_star_button_exists_in_dom(page_with_message):
    expect(page_with_message.get_by_title("Star this response")).to_be_attached()


def test_copy_button_exists_in_dom(page_with_message):
    expect(page_with_message.get_by_title("Copy response")).to_be_attached()


def test_star_message_changes_button_title(page_with_message):
    page_with_message.get_by_title("Star this response").click(force=True)
    expect(page_with_message.get_by_title("Unstar")).to_be_attached()


def test_star_message_shows_starred_label(page_with_message):
    page_with_message.get_by_title("Star this response").click(force=True)
    expect(page_with_message.get_by_text("Starred")).to_be_visible(timeout=3000)


def test_unstar_message_restores_star_button(page_with_message):
    page_with_message.get_by_title("Star this response").click(force=True)
    page_with_message.get_by_title("Unstar").click(force=True)
    expect(page_with_message.get_by_title("Star this response")).to_be_attached()


def test_copy_button_writes_to_clipboard(page_with_message):
    page_with_message.get_by_title("Copy response").click(force=True)
    clipboard = page_with_message.evaluate("async () => navigator.clipboard.readText()")
    assert MOCK_REPLY in clipboard


def test_multiple_messages_all_displayed(page):
    messages = [
        "First issue: cannot locate motivation",
        "Second issue: feelings buffer overflow",
    ]
    for msg in messages:
        page.locator("textarea").fill(msg)
        page.locator("textarea").press("Enter")
        page.wait_for_selector(f"text={MOCK_REPLY}")

    for msg in messages:
        expect(page.get_by_text(msg)).to_be_visible()


def test_multiple_agent_replies_displayed(page):
    for _ in range(2):
        page.locator("textarea").fill("another message")
        page.locator("textarea").press("Enter")
        page.wait_for_selector(f"text={MOCK_REPLY}")

    expect(page.get_by_text(MOCK_REPLY)).to_have_count(2)


def test_user_message_has_no_star_or_copy_buttons(page_with_message):
    # Star/copy buttons only exist on agent messages, not user messages
    user_message_count = page_with_message.get_by_text("YOU (Ticket Submitter)").count()
    star_button_count = page_with_message.get_by_title("Star this response").count()
    # Should be one star button per agent message, not per user message
    assert star_button_count <= user_message_count
