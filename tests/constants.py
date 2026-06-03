"""Shared constants for the Playwright e2e test suite.

Kept separate from conftest.py so tests can import these values without
importing the conftest module directly (an anti-pattern — conftest is for
pytest fixtures/hooks, which are auto-discovered, not imported).
"""

BASE_URL = "http://localhost:3000"
MOCK_REPLY = "Thank you for filing this ticket. We will get to it eventually."
