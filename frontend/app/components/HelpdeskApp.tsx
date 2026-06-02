"use client";

import { useState, useEffect, useCallback } from "react";
import { Menu, X } from "lucide-react";
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

export default function HomePage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [activeTicketId, setActiveTicketId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
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
      const first = createTicket();
      setTickets([first]);
      setActiveTicketId(first.id);
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

  // Persist active ticket
  useEffect(() => {
    if (!hydrated || !activeTicketId) return;
    localStorage.setItem(LS_ACTIVE, activeTicketId);
  }, [activeTicketId, hydrated]);

  const activeTicket = tickets.find((t) => t.id === activeTicketId) ?? null;

  const updateTicket = useCallback((id: string, updater: (t: Ticket) => Ticket) => {
    setTickets((prev) => prev.map((t) => (t.id === id ? updater(t) : t)));
  }, []);

  const handleNewTicket = () => {
    const ticket = createTicket();
    setTickets((prev) => [ticket, ...prev]);
    setActiveTicketId(ticket.id);
    setInput("");
    setError(null);
    setSidebarOpen(false);
  };

  const handleDeleteTicket = (id: string) => {
    setTickets((prev) => {
      const next = prev.filter((t) => t.id !== id);
      if (activeTicketId === id) {
        if (next.length > 0) {
          setActiveTicketId(next[0].id);
        } else {
          const fresh = createTicket();
          setTimeout(() => {
            setTickets([fresh]);
            setActiveTicketId(fresh.id);
          }, 0);
          return [];
        }
      }
      return next;
    });
  };

  const handleSelectTicket = (id: string) => {
    setActiveTicketId(id);
    setInput("");
    setError(null);
    setSidebarOpen(false);
  };

  const handleSubmit = async () => {
    if (!input.trim() || !activeTicket || loading) return;
    const text = input.trim();
    setInput("");
    setError(null);

    const userMsg = {
      id: crypto.randomUUID(),
      role: "user" as const,
      text,
      timestamp: Date.now(),
      starred: false,
    };

    updateTicket(activeTicket.id, (t) => ({
      ...t,
      title: t.title || text.slice(0, 60),
      messages: [...t.messages, userMsg],
      status: t.status === "OPEN" ? "IN_PROGRESS" : t.status,
    }));

    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      const agentMsg = {
        id: crypto.randomUUID(),
        role: "agent" as const,
        text: data.reply,
        timestamp: Date.now(),
        starred: false,
      };

      updateTicket(activeTicket.id, (t) => ({
        ...t,
        messages: [...t.messages, agentMsg],
      }));
    } catch {
      setError("Could not reach support. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestedIssue = (text: string) => {
    setInput(text);
    // submit immediately after state update
    setTimeout(() => {
      if (!activeTicket || loading) return;
      const userMsg = {
        id: crypto.randomUUID(),
        role: "user" as const,
        text,
        timestamp: Date.now(),
        starred: false,
      };
      updateTicket(activeTicket.id, (t) => ({
        ...t,
        title: t.title || text.slice(0, 60),
        messages: [...t.messages, userMsg],
        status: t.status === "OPEN" ? "IN_PROGRESS" : t.status,
      }));
      setInput("");
      setLoading(true);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "";
      fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      })
        .then((r) => {
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          return r.json();
        })
        .then((data) => {
          const agentMsg = {
            id: crypto.randomUUID(),
            role: "agent" as const,
            text: data.reply,
            timestamp: Date.now(),
            starred: false,
          };
          updateTicket(activeTicket.id, (t) => ({
            ...t,
            messages: [...t.messages, agentMsg],
          }));
        })
        .catch(() => setError("Could not reach support. Please try again."))
        .finally(() => setLoading(false));
    }, 0);
  };

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

        {activeTicket ? (
          <div className="flex flex-col flex-1 min-h-0">
            <TicketHeader
              ticket={activeTicket}
              onUpdateStatus={handleUpdateStatus}
              onUpdatePriority={handleUpdatePriority}
              onExport={handleExport}
            />

            <TicketThread
              messages={activeTicket.messages}
              onStarMessage={handleStarMessage}
              onCopyMessage={handleCopyMessage}
            />

            {loading && <TypingIndicator />}

            {activeTicket.messages.length === 0 && !loading && (
              <SuggestedIssues onSelect={handleSuggestedIssue} />
            )}

            <InputBar
              input={input}
              loading={loading}
              error={error}
              hasMessages={activeTicket.messages.length > 0}
              onChange={setInput}
              onSubmit={handleSubmit}
              onDismissError={() => setError(null)}
            />
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p style={{ color: "var(--text-xmuted)" }} className="text-sm">
              No ticket selected.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
