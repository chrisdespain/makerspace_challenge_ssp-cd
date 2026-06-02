"""
Tests for dark/light theme toggling and localStorage persistence.
"""
from playwright.sync_api import expect


def _get_html_classes(page) -> str:
    return page.evaluate("document.documentElement.className")


def test_default_theme_is_light(page):
    assert "dark" not in _get_html_classes(page)


def test_theme_toggle_button_visible(page):
    expect(page.get_by_title("Toggle theme")).to_be_visible()


def test_toggle_switches_to_dark_mode(page):
    page.get_by_title("Toggle theme").click()
    assert "dark" in _get_html_classes(page)


def test_toggle_switches_back_to_light_mode(page):
    page.get_by_title("Toggle theme").click()
    page.get_by_title("Toggle theme").click()
    assert "dark" not in _get_html_classes(page)


def test_dark_mode_persists_after_reload(page):
    page.get_by_title("Toggle theme").click()
    page.reload()
    page.wait_for_selector("textarea")
    assert "dark" in _get_html_classes(page)


def test_light_mode_persists_after_reload(page):
    # Default is light; reload and confirm it stays light
    page.reload()
    page.wait_for_selector("textarea")
    assert "dark" not in _get_html_classes(page)
