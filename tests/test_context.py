"""
Tests for hidden conversation context (the running summary) and per-ticket
error scoping.

The backend is stateless and only accepts a single `message` string, so context
is carried by (a) appending an instruction for the model to return a hidden
running summary after a sentinel, and (b) replaying that summary inside the
`message` payload on the next turn. The summary must never appear in the UI, and
the user bubble must always show the raw typed text — not the wrapped payload.
"""
import json
from playwright.sync_api import expect
from tests.constants import MOCK_REPLY

# Must match CONTEXT_SENTINEL in app/components/HelpdeskApp.tsx.
SENTINEL = "<<<CTX>>>"


def test_summary_sentinel_hidden_from_ui(page):
    """Input: the model returns a reply followed by the sentinel + a summary. Expected: only the reply shows; the sentinel and summary are hidden."""
    page.route(
        "**/api/chat",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": f"Here is the visible reply.\n{SENTINEL} secret running summary"}),
        ),
    )
    page.locator("textarea").fill("first message")
    page.locator("textarea").press("Enter")
    expect(
        page.get_by_test_id("ticket-thread").get_by_text("Here is the visible reply.")
    ).to_be_visible()
    expect(page.get_by_text("secret running summary")).to_have_count(0)
    expect(page.get_by_text(SENTINEL)).to_have_count(0)


def test_summary_only_reply_does_not_leak(page):
    """Input: the model returns ONLY a summary after the sentinel (no visible reply). Expected: the summary is never shown; a neutral placeholder appears instead."""
    page.route(
        "**/api/chat",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": f"{SENTINEL} leaked summary text"}),
        ),
    )
    page.locator("textarea").fill("hi")
    page.locator("textarea").press("Enter")
    expect(page.get_by_test_id("ticket-thread").get_by_text("(No response.)")).to_be_visible()
    expect(page.get_by_text("leaked summary text")).to_have_count(0)
    expect(page.get_by_text(SENTINEL)).to_have_count(0)


def test_prior_summary_sent_on_next_message(page):
    """Input: send two messages; the model returns a summary each time. Expected: the second request's payload carries the first summary, and no summary shows in the UI."""
    requests = []
    counter = {"n": 0}

    def handler(route):
        requests.append(route.request.post_data)
        counter["n"] += 1
        n = counter["n"]
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": f"Reply number {n}.\n{SENTINEL} SUMMARY_TOKEN_{n}"}),
        )

    page.route("**/api/chat", handler)

    page.locator("textarea").fill("first")
    page.locator("textarea").press("Enter")
    expect(page.get_by_test_id("ticket-thread").get_by_text("Reply number 1.")).to_be_visible()

    page.locator("textarea").fill("second")
    page.locator("textarea").press("Enter")
    expect(page.get_by_test_id("ticket-thread").get_by_text("Reply number 2.")).to_be_visible()

    assert len(requests) == 2
    # First turn has no prior context; second turn replays the first summary.
    assert "SUMMARY_TOKEN_1" not in requests[0]
    assert "SUMMARY_TOKEN_1" in requests[1]
    # The cached summary is never rendered.
    expect(page.get_by_text("SUMMARY_TOKEN_1")).to_have_count(0)


def test_user_bubble_shows_raw_text_not_wire_payload(page):
    """Input: submit a plain message. Expected: the bubble shows the raw text; the summary instruction and sentinel never leak into the thread."""
    page.route(
        "**/api/chat",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"reply": f"ok{SENTINEL}sum"}),
        ),
    )
    page.locator("textarea").fill("just the raw text")
    page.locator("textarea").press("Enter")
    thread = page.get_by_test_id("ticket-thread")
    expect(thread.get_by_text("just the raw text")).to_be_visible()
    # Scaffolding from the wire payload must not appear anywhere on screen.
    expect(page.get_by_text("After your reply")).to_have_count(0)
    expect(page.get_by_text(SENTINEL)).to_have_count(0)


def test_error_is_scoped_to_its_ticket(page):
    """Input: one healthy ticket, then a second ticket whose request fails. Expected: the error shows only on the failing ticket, not on the healthy one."""
    # First ticket succeeds via the default mocked reply.
    page.locator("textarea").fill("healthy ticket")
    page.locator("textarea").press("Enter")
    page.wait_for_selector(f"text={MOCK_REPLY}")
    # Open a new ticket and make its request fail.
    page.get_by_role("button", name="New Ticket").click()
    page.route("**/api/chat", lambda route: route.fulfill(status=500))
    page.locator("textarea").fill("doomed ticket")
    page.locator("textarea").press("Enter")
    expect(page.get_by_text("Could not reach support. Please try again.")).to_be_visible()
    # Switch back to the first (healthy) ticket — its view shows no error.
    page.locator("aside .font-mono").nth(1).click()
    expect(page.get_by_text("Could not reach support. Please try again.")).not_to_be_visible()
