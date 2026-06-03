"use client";

import { useState, useEffect, useCallback } from "react";
import { Menu } from "lucide-react";
import Sidebar from "./Sidebar";
import TicketHeader from "./TicketHeader";
import TicketThread from "./TicketThread";
import TypingIndicator from "./TypingIndicator";
import SuggestedIssues from "./SuggestedIssues";
import InputBar from "./InputBar";
import { Ticket, Priority, TicketStatus } from "./types";
import { exportTicketAsMarkdown } from "../utils/export";

const PRIORITIES: Priority[] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

function generateTicketId(): string {
  return "EMO-" + Math.floor(1000 + Math.random() * 9000);
}

function createTicket(): Ticket {
  return {
    id: generateTicketId(),
    title: "",
    priority: PRIORITIES[Math.floor(Math.random() * PRIORITIES.length)],
    status: "OPEN",
    messages: [],
    createdAt: Date.now(),
  };
}

const LS_TICKETS = "emo-helpdesk-tickets";
const LS_ACTIVE = "emo-helpdesk-active";
const LS_THEME = "emo-helpdesk-theme";

// Distinctive marker the model appends before its hidden running summary.
// Deliberately not a plain word like "SUMMARY:" that a reply might emit naturally.
const CONTEXT_SENTINEL = "<<<CTX>>>";

// Build the single `message` string sent to the (stateless) backend. The user's
// raw text is never modified for display — only this wire payload carries the
// prior summary and the instruction to return an updated one.
function buildPrompt(priorSummary: string | undefined, userText: string): string {
  const parts: string[] = [];
  if (priorSummary) {
    parts.push(
      `Context from earlier in this conversation (do not mention or quote this directly): ${priorSummary}`
    );
    parts.push("");
  }
  parts.push(userText);
  parts.push("");
  parts.push(
    `After your reply to the user, output the exact marker ${CONTEXT_SENTINEL} on a new line, ` +
      `followed by an updated one- to two-sentence running summary of the whole conversation ` +
      `so far (fold in this latest exchange — do not just repeat the previous summary). ` +
      `Everything after ${CONTEXT_SENTINEL} is for your own future context and is hidden from the user.`
  );
  return parts.join("\n");
}

// Split a raw reply into the user-facing display text and the hidden summary.
// Parses the LAST sentinel so a sentinel appearing in the visible reply is safe.
function parseReply(raw: string): { display: string; summary: string | null } {
  const idx = raw.lastIndexOf(CONTEXT_SENTINEL);
  if (idx === -1) {
    // Model didn't comply — show the whole reply, keep the previous summary.
    return { display: raw.trim(), summary: null };
  }
  let display = raw.slice(0, idx).trim();
  const summary = raw.slice(idx + CONTEXT_SENTINEL.length).trim() || null;
  // Degenerate case: nothing before the marker — strip the marker and show the rest.
  if (!display) display = raw.split(CONTEXT_SENTINEL).join("").trim();
  return { display, summary };
}

export default function HomePage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [activeTicketId, setActiveTicketId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  // IDs of tickets with an in-flight /api/chat request. Per-ticket (not a single
  // global flag) so the "composing..." indicator only shows on the ticket that
  // is actually waiting, and switching to another ticket stays clean.
  const [loadingIds, setLoadingIds] = useState<string[]>([]);
  // Errors keyed by ticket ID (per-ticket, like loadingIds) so a failure on one
  // ticket never surfaces on another.
  const [errorsByTicket, setErrorsByTicket] = useState<Record<string, string>>({});
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  // Load from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem(LS_THEME) as "light" | "dark" | null;
    if (savedTheme) setTheme(savedTheme);

    const savedTickets = localStorage.getItem(LS_TICKETS);
    const parsed: Ticket[] = savedTickets ? JSON.parse(savedTickets) : [];

    if (parsed.length === 0) {
      // No tickets yet — start in draft mode; a ticket is created (and listed)
      // only when the first message is submitted.
      setActiveTicketId(null);
    } else {
      setTickets(parsed);
      const savedActive = localStorage.getItem(LS_ACTIVE);
      setActiveTicketId(
        savedActive && parsed.find((t) => t.id === savedActive)
          ? savedActive
          : parsed[0].id
      );
    }
    setHydrated(true);
  }, []);

  // Apply theme class to <html>
  useEffect(() => {
    if (!hydrated) return;
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem(LS_THEME, theme);
  }, [theme, hydrated]);

  // Persist tickets
  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(LS_TICKETS, JSON.stringify(tickets));
  }, [tickets, hydrated]);

  // Persist active ticket (clear the key in draft mode)
  useEffect(() => {
    if (!hydrated) return;
    if (activeTicketId) localStorage.setItem(LS_ACTIVE, activeTicketId);
    else localStorage.removeItem(LS_ACTIVE);
  }, [activeTicketId, hydrated]);

  const activeTicket = tickets.find((t) => t.id === activeTicketId) ?? null;
  // Whether the currently-viewed ticket is awaiting a reply.
  const activeLoading = activeTicketId != null && loadingIds.includes(activeTicketId);
  // Error for the currently-viewed ticket only.
  const activeError = activeTicketId ? errorsByTicket[activeTicketId] ?? null : null;

  const setTicketError = (id: string, message: string) =>
    setErrorsByTicket((prev) => ({ ...prev, [id]: message }));
  const clearTicketError = (id: string) =>
    setErrorsByTicket((prev) => {
      if (!(id in prev)) return prev;
      const next = { ...prev };
      delete next[id];
      return next;
    });

  const updateTicket = useCallback((id: string, updater: (t: Ticket) => Ticket) => {
    setTickets((prev) => prev.map((t) => (t.id === id ? updater(t) : t)));
  }, []);

  const handleNewTicket = () => {
    // Enter draft mode — no ticket is created or listed until the first submit.
    setActiveTicketId(null);
    setInput("");
    setSidebarOpen(false);
  };

  const handleDeleteTicket = (id: string) => {
    setTickets((prev) => {
      const next = prev.filter((t) => t.id !== id);
      if (activeTicketId === id) {
        // Select the next remaining ticket, or drop to draft mode if none left.
        setActiveTicketId(next.length > 0 ? next[0].id : null);
      }
      return next;
    });
  };

  const handleSelectTicket = (id: string) => {
    setActiveTicketId(id);
    setInput("");
    setSidebarOpen(false);
  };

  const submitMessage = async (rawText: string) => {
    const text = rawText.trim();
    if (!text) return;
    // Block re-submitting a ticket that's already awaiting a reply. A draft
    // (no active ticket) is always allowed — it creates a new ticket.
    if (activeTicket && loadingIds.includes(activeTicket.id)) return;

    setInput("");

    // The bubble always shows the raw typed text — never the context-wrapped
    // wire payload built below.
    const userMsg = {
      id: crypto.randomUUID(),
      role: "user" as const,
      text,
      timestamp: Date.now(),
      starred: false,
    };

    // Capture the prior running summary for this conversation before we mutate.
    const priorSummary = activeTicket?.summary;

    // Materialize a ticket on the first submit (draft mode), otherwise append
    // to the active ticket. `targetId` is the canonical ID every async write
    // below keys off — never `activeTicketId` — so concurrent replies across
    // tickets always land on the right one. (Same-ticket turns are serialized
    // by the loading guard above, so its summary updates stay consistent.)
    let targetId: string;
    if (activeTicket) {
      targetId = activeTicket.id;
      updateTicket(targetId, (t) => ({
        ...t,
        title: t.title || text.slice(0, 60),
        messages: [...t.messages, userMsg],
        status: t.status === "OPEN" ? "IN_PROGRESS" : t.status,
      }));
    } else {
      const newTicket: Ticket = {
        ...createTicket(),
        title: text.slice(0, 60),
        status: "IN_PROGRESS",
        messages: [userMsg],
      };
      targetId = newTicket.id;
      setTickets((prev) => [newTicket, ...prev]);
      setActiveTicketId(newTicket.id);
    }

    clearTicketError(targetId);
    setLoadingIds((prev) => [...prev, targetId]);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Wire payload carries prior context + the summary instruction.
        body: JSON.stringify({ message: buildPrompt(priorSummary, text) }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // Split the model's reply into what the user sees and the hidden summary.
      const { display, summary } = parseReply(data.reply ?? "");

      const agentMsg = {
        id: crypto.randomUUID(),
        role: "agent" as const,
        text: display,
        timestamp: Date.now(),
        starred: false,
      };

      updateTicket(targetId, (t) => ({
        ...t,
        messages: [...t.messages, agentMsg],
        // Keep the prior summary if the model didn't return a new one.
        summary: summary ?? t.summary,
      }));
    } catch {
      setTicketError(targetId, "Could not reach support. Please try again.");
    } finally {
      setLoadingIds((prev) => prev.filter((id) => id !== targetId));
    }
  };

  const handleSubmit = () => submitMessage(input);
  const handleSuggestedIssue = (text: string) => submitMessage(text);

  const handleStarMessage = (msgId: string) => {
    if (!activeTicketId) return;
    updateTicket(activeTicketId, (t) => ({
      ...t,
      messages: t.messages.map((m) =>
        m.id === msgId ? { ...m, starred: !m.starred } : m
      ),
    }));
  };

  const handleCopyMessage = (text: string) => {
    navigator.clipboard.writeText(text).catch(() => {});
  };

  const handleUpdateStatus = (status: TicketStatus) => {
    if (!activeTicketId) return;
    updateTicket(activeTicketId, (t) => ({ ...t, status }));
  };

  const handleUpdatePriority = (priority: Priority) => {
    if (!activeTicketId) return;
    updateTicket(activeTicketId, (t) => ({ ...t, priority }));
  };

  const handleExport = () => {
    if (activeTicket) exportTicketAsMarkdown(activeTicket);
  };

  if (!hydrated) return null;

  return (
    <div className="flex h-full overflow-hidden" style={{ background: "var(--bg)" }}>
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar — desktop always visible, mobile slide-in */}
      <div
        className={`
          fixed md:relative inset-y-0 left-0 z-30
          transform transition-transform duration-200
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
      >
        <Sidebar
          tickets={tickets}
          activeTicketId={activeTicketId}
          theme={theme}
          onSelectTicket={handleSelectTicket}
          onNewTicket={handleNewTicket}
          onDeleteTicket={handleDeleteTicket}
          onToggleTheme={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
        />
      </div>

      {/* Main area */}
      <div className="flex flex-col flex-1 min-w-0 h-full">
        {/* Mobile topbar */}
        <div
          className="flex md:hidden items-center gap-3 px-4 py-3 border-b flex-shrink-0"
          style={{
            background: "var(--surface)",
            borderColor: "var(--border)",
          }}
        >
          <button
            onClick={() => setSidebarOpen(true)}
            style={{ color: "var(--text-muted)" }}
          >
            <Menu size={18} />
          </button>
          <span className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
            {activeTicket?.id ?? "Emotional Helpdesk"}
          </span>
        </div>

        <div className="flex flex-col flex-1 min-h-0">
          {activeTicket && (
            <TicketHeader
              ticket={activeTicket}
              onUpdateStatus={handleUpdateStatus}
              onUpdatePriority={handleUpdatePriority}
              onExport={handleExport}
            />
          )}

          {activeTicket ? (
            <TicketThread
              messages={activeTicket.messages}
              onStarMessage={handleStarMessage}
              onCopyMessage={handleCopyMessage}
            />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center px-6 text-center">
              <p
                className="text-base font-medium"
                style={{ color: "var(--text-secondary)" }}
              >
                Describe your issue to open a ticket
              </p>
              <p className="text-sm mt-1.5" style={{ color: "var(--text-xmuted)" }}>
                An EMO ticket is created when you send your first message.
              </p>
            </div>
          )}

          {activeLoading && <TypingIndicator />}

          {(!activeTicket || activeTicket.messages.length === 0) && !activeLoading && (
            <SuggestedIssues onSelect={handleSuggestedIssue} />
          )}

          <InputBar
            input={input}
            loading={activeLoading}
            error={activeError}
            hasMessages={!!activeTicket && activeTicket.messages.length > 0}
            onChange={setInput}
            onSubmit={handleSubmit}
            onDismissError={() => activeTicketId && clearTicketError(activeTicketId)}
          />
        </div>
      </div>
    </div>
  );
}
