"""
Tests for ticket lifecycle: create, select, delete, sidebar display.
"""
import re
from playwright.sync_api import expect
from conftest import MOCK_REPLY


def test_page_loads_with_ticket_id(page):
    expect(page.locator("text=/EMO-\\d{4}/").first).to_be_visible()


def test_suggested_issues_visible_on_empty_ticket(page):
    expect(page.get_by_text("Common issues — select one to file immediately:")).to_be_visible()


def test_new_ticket_button_visible(page):
    expect(page.get_by_role("button", name="New Ticket")).to_be_visible()


def test_new_ticket_creates_sidebar_entry(page):
    page.get_by_role("button", name="New Ticket").click()
    expect(page.locator("aside .font-mono")).to_have_count(2)


def test_new_ticket_becomes_active(page):
    page.get_by_role("button", name="New Ticket").click()
    first_sidebar_id = page.locator("aside .font-mono").first.text_content()
    # The header should show the newly created ticket
    expect(page.locator(f"text={first_sidebar_id}").first).to_be_visible()


def test_sidebar_shows_new_ticket_label_before_first_message(page):
    expect(page.locator("aside").get_by_text("New ticket")).to_be_visible()


def test_ticket_title_updates_after_first_message(page):
    page.locator("textarea").fill("Memory leak in my personal life")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    expect(page.locator("aside").get_by_text("Memory leak in my personal life")).to_be_visible()


def test_select_different_ticket_switches_active(page):
    page.get_by_role("button", name="New Ticket").click()
    page.get_by_role("button", name="New Ticket").click()
    third_id = page.locator("aside .font-mono").nth(2).text_content()
    page.locator("aside .font-mono").nth(2).click()
    expect(page.locator(f"text={third_id}").first).to_be_visible()


def test_selecting_ticket_from_sidebar_shows_its_messages(page):
    # Submit a message on the first ticket
    page.locator("textarea").fill("Original ticket message")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    # Create and switch to a new ticket
    page.get_by_role("button", name="New Ticket").click()
    expect(page.get_by_text("Original ticket message")).not_to_be_visible()
    # Switch back to first ticket
    page.locator("aside .font-mono").nth(1).click()
    expect(page.get_by_text("Original ticket message")).to_be_visible()


def test_delete_ticket_removes_from_sidebar(page):
    page.get_by_role("button", name="New Ticket").click()
    initial_count = page.locator("aside .font-mono").count()
    page.get_by_title("Close ticket").first.click(force=True)
    expect(page.locator("aside .font-mono")).to_have_count(initial_count - 1)


def test_delete_active_ticket_selects_next_ticket(page):
    page.get_by_role("button", name="New Ticket").click()
    # Delete the first (active) ticket
    page.get_by_title("Close ticket").first.click(force=True)
    # A ticket should still be selected (textarea still accessible)
    expect(page.locator("textarea")).to_be_visible()


def test_delete_last_ticket_auto_creates_replacement(page):
    page.get_by_title("Close ticket").first.click(force=True)
    page.wait_for_selector("textarea")
    expect(page.locator("text=/EMO-\\d{4}/").first).to_be_visible()
