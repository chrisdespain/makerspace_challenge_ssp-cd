import json
import pytest

BASE_URL = "http://localhost:3000"
MOCK_REPLY = "Thank you for filing this ticket. We will get to it eventually."


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "permissions": ["clipboard-read", "clipboard-write"],
    }


@pytest.fixture
def page(page):
    page.route(
        "**/api/chat",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": MOCK_REPLY}),
        ),
    )
    page.goto(BASE_URL)
    page.wait_for_selector("textarea")
    return page


@pytest.fixture
def page_with_message(page):
    """Page with one submitted user message and the mocked agent reply visible."""
    page.locator("textarea").fill("I need help processing my feelings about Mondays")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    return page


@pytest.fixture
def mobile_page(browser):
    """Page fixture using a mobile viewport (375x812, iPhone SE)."""
    context = browser.new_context(
        viewport={"width": 375, "height": 812},
        permissions=["clipboard-read", "clipboard-write"],
    )
    p = context.new_page()
    p.route(
        "**/api/chat",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": MOCK_REPLY}),
        ),
    )
    p.goto(BASE_URL)
    p.wait_for_selector("textarea")
    yield p
    context.close()
