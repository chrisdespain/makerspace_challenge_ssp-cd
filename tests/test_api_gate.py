"""
Backend access-gate tests (FastAPI TestClient — no browser, no OpenAI calls).

The /api/chat endpoint requires a matching X-Access-Code header only when
APP_ACCESS_CODE is configured; with it unset (local dev) the gate is open.
"""
import os

# Let the OpenAI client construct at import time even without a real key — the
# gate tests never reach an actual OpenAI call.
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")

from fastapi.testclient import TestClient  # noqa: E402
from api.index import app  # noqa: E402

client = TestClient(app)


def test_gate_blocks_when_code_missing(monkeypatch):
    """Input: APP_ACCESS_CODE set, request without the header. Expected: 401."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    r = client.post("/api/chat", json={"message": "hi"})
    assert r.status_code == 401


def test_gate_blocks_wrong_code(monkeypatch):
    """Input: APP_ACCESS_CODE set, wrong header. Expected: 401."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    r = client.post("/api/chat", json={"message": "hi"}, headers={"X-Access-Code": "nope"})
    assert r.status_code == 401


def test_gate_allows_correct_code(monkeypatch):
    """Input: APP_ACCESS_CODE set, correct header, no OpenAI key. Expected: gate passes — 500 for the missing key, not 401."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    r = client.post("/api/chat", json={"message": "hi"}, headers={"X-Access-Code": "secret123"})
    assert r.status_code == 500
    assert "OPENAI_API_KEY" in r.json()["detail"]


def test_no_gate_when_unset(monkeypatch):
    """Input: APP_ACCESS_CODE unset (local dev), no header. Expected: gate open — 500 for the missing key, not 401."""
    monkeypatch.delenv("APP_ACCESS_CODE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    r = client.post("/api/chat", json={"message": "hi"})
    assert r.status_code == 500
    assert "OPENAI_API_KEY" in r.json()["detail"]


def test_access_probe_not_required_when_unset(monkeypatch):
    """Input: GET /api/access with APP_ACCESS_CODE unset. Expected: required=false, valid=true (no gate)."""
    monkeypatch.delenv("APP_ACCESS_CODE", raising=False)
    body = client.get("/api/access").json()
    assert body == {"required": False, "valid": True}


def test_access_probe_required_without_code(monkeypatch):
    """Input: GET /api/access with code set but no header. Expected: required=true, valid=false (show gate)."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    body = client.get("/api/access").json()
    assert body == {"required": True, "valid": False}


def test_access_probe_valid_with_correct_code(monkeypatch):
    """Input: GET /api/access with the correct header. Expected: required=true, valid=true (unlock)."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    body = client.get("/api/access", headers={"X-Access-Code": "secret123"}).json()
    assert body == {"required": True, "valid": True}


def test_access_probe_invalid_with_wrong_code(monkeypatch):
    """Input: GET /api/access with a wrong header. Expected: required=true, valid=false."""
    monkeypatch.setenv("APP_ACCESS_CODE", "secret123")
    body = client.get("/api/access", headers={"X-Access-Code": "nope"}).json()
    assert body == {"required": True, "valid": False}
