"""
Tests for mobile viewport behavior: sidebar toggle, overlay dismiss,
and ticket selection closing the sidebar.
"""
from playwright.sync_api import expect

from tests.constants import MOCK_REPLY


def test_mobile_topbar_visible(mobile_page):
    """Input: open the app on a mobile viewport. Expected: the mobile top bar is visible."""
    expect(mobile_page.locator(".md\\:hidden").first).to_be_visible()


def test_mobile_sidebar_hidden_by_default(mobile_page):
    """Input: open the app on mobile. Expected: the sidebar is off-screen (not in the viewport)."""
    # Sidebar hides by sliding off-canvas (-translate-x-full), so it stays in the
    # DOM and "visible"; assert it's out of the viewport instead.
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_in_viewport()


def test_mobile_hamburger_opens_sidebar(mobile_page):
    """Input: tap the hamburger button. Expected: the sidebar slides in (New Ticket visible)."""
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    expect(mobile_page.get_by_role("button", name="New Ticket")).to_be_visible()


def test_mobile_overlay_closes_sidebar(mobile_page):
    """Input: open the sidebar, then tap the dark overlay. Expected: the sidebar slides back off-screen."""
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    expect(mobile_page.get_by_role("button", name="New Ticket")).to_be_visible()
    # Click the dark overlay behind the sidebar
    mobile_page.locator(".fixed.inset-0.z-20").click()
    # Sidebar hides by sliding off-canvas (-translate-x-full), so it stays in the
    # DOM and "visible"; assert it's out of the viewport instead.
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_in_viewport()


def test_mobile_new_ticket_closes_sidebar(mobile_page):
    """Input: open the sidebar and tap New Ticket. Expected: the sidebar closes (slides off-screen)."""
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    mobile_page.get_by_role("button", name="New Ticket").click()
    # handleNewTicket calls setSidebarOpen(false)
    # Sidebar hides by sliding off-canvas (-translate-x-full), so it stays in the
    # DOM and "visible"; assert it's out of the viewport instead.
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_in_viewport()


def test_mobile_select_ticket_closes_sidebar(mobile_page):
    """Input: file a ticket, open the sidebar, and tap that ticket. Expected: the sidebar closes."""
    # File a ticket so there is a sidebar entry to select.
    mobile_page.locator("textarea").fill("mobile ticket")
    mobile_page.locator("textarea").press("Enter")
    mobile_page.wait_for_selector(f"text={MOCK_REPLY}")
    # Open the sidebar and tap the ticket entry.
    mobile_page.locator(".md\\:hidden").first.locator("button").first.click()
    mobile_page.locator("aside .font-mono").first.click()
    # handleSelectTicket calls setSidebarOpen(false); the sidebar slides off-canvas
    # (-translate-x-full) so it stays in the DOM — assert it's out of the viewport.
    expect(mobile_page.get_by_role("button", name="New Ticket")).not_to_be_in_viewport()


def test_mobile_active_ticket_id_in_topbar(mobile_page):
    """Input: file a ticket on mobile. Expected: the top bar shows that ticket's EMO-#### ID."""
    mobile_page.locator("textarea").fill("mobile ticket")
    mobile_page.locator("textarea").press("Enter")
    mobile_page.wait_for_selector(f"text={MOCK_REPLY}")
    topbar_text = mobile_page.locator(".md\\:hidden").first.text_content()
    assert "EMO-" in topbar_text
