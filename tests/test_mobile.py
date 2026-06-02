"""
Tests for mobile viewport behavior: sidebar toggle, overlay dismiss,
and ticket selection closing the sidebar.
"""
from playwright.sync_api import expect


def test_mobile_topbar_visible(mobile_page):
    expect(mobile_page.locator(".md\\:hidden").first).to_be_visible()


def test_mobile_sidebar_hidden_by_default(mobile_page):
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_visible()


def test_mobile_hamburger_opens_sidebar(mobile_page):
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    expect(mobile_page.get_by_role("button", name="New Ticket")).to_be_visible()


def test_mobile_overlay_closes_sidebar(mobile_page):
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    expect(mobile_page.get_by_role("button", name="New Ticket")).to_be_visible()
    # Click the dark overlay behind the sidebar
    mobile_page.locator(".fixed.inset-0.z-20").click()
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_visible()


def test_mobile_new_ticket_closes_sidebar(mobile_page):
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    mobile_page.get_by_role("button", name="New Ticket").click()
    # handleNewTicket calls setSidebarOpen(false)
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_visible()


def test_mobile_select_ticket_closes_sidebar(mobile_page):
    # Create a second ticket first
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    mobile_page.get_by_role("button", name="New Ticket").click()
    # Re-open sidebar and select the second ticket
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    mobile_page.locator("aside .font-mono").nth(1).click()
    # handleSelectTicket calls setSidebarOpen(false)
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_visible()


def test_mobile_active_ticket_id_in_topbar(mobile_page):
    # The mobile topbar shows the active ticket's EMO-XXXX ID
    topbar_text = mobile_page.locator(".md\\:hidden").first.text_content()
    assert "EMO-" in topbar_text
