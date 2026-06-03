"use client";

import { Sun, Moon, Plus, X, Ticket } from "lucide-react";
import { Ticket as TicketType } from "./types";
import { formatDistanceToNow } from "../utils/time";

interface SidebarProps {
  tickets: TicketType[];
  activeTicketId: string | null;
  theme: "light" | "dark";
  onSelectTicket: (id: string) => void;
  onNewTicket: () => void;
  onDeleteTicket: (id: string) => void;
  onToggleTheme: () => void;
}

const priorityDot: Record<string, string> = {
  LOW: "bg-green-500",
  MEDIUM: "bg-yellow-500",
  HIGH: "bg-red-500",
  CRITICAL: "bg-pink-500",
};

export default function Sidebar({
  tickets,
  activeTicketId,
  theme,
  onSelectTicket,
  onNewTicket,
  onDeleteTicket,
  onToggleTheme,
}: SidebarProps) {
  return (
    <aside
      className="flex flex-col h-full border-r"
      style={{
        background: "var(--sidebar-bg)",
        borderColor: "var(--border)",
        width: "260px",
        minWidth: "260px",
      }}
    >
      {/* Header */}
      <div
        className="flex items-center gap-2 px-4 py-4 border-b"
        style={{ borderColor: "var(--border)" }}
      >
        <div
          className="flex items-center justify-center w-7 h-7 rounded"
          style={{ background: "var(--accent)" }}
        >
          <Ticket size={14} color="white" />
        </div>
        <span
          className="font-display text-base font-semibold tracking-tight"
          style={{ color: "var(--text-primary)" }}
        >
          Emotional Helpdesk
        </span>
      </div>

      {/* New Ticket Button */}
      <div className="px-3 py-3">
        <button
          onClick={onNewTicket}
          className="flex items-center gap-2 w-full px-3 py-2 rounded-md text-sm font-medium transition-colors"
          style={{
            background: "var(--accent)",
            color: "white",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.background = "var(--accent-hover)")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.background = "var(--accent)")
          }
        >
          <Plus size={14} />
          New Ticket
        </button>
      </div>

      {/* Ticket list */}
      <div className="flex-1 overflow-y-auto px-2 pb-2">
        {tickets.length === 0 && (
          <p
            className="text-xs px-2 py-4 text-center"
            style={{ color: "var(--text-xmuted)" }}
          >
            No open tickets.
            <br />
            Feelings bottled up successfully.
          </p>
        )}
        {tickets.map((ticket) => (
          <div
            key={ticket.id}
            className="group relative flex flex-col gap-1 px-3 py-2.5 rounded-md cursor-pointer mb-1 transition-colors"
            style={{
              background:
                activeTicketId === ticket.id
                  ? "var(--surface)"
                  : "transparent",
              border:
                activeTicketId === ticket.id
                  ? "1px solid var(--border)"
                  : "1px solid transparent",
            }}
            onClick={() => onSelectTicket(ticket.id)}
          >
            <div className="flex items-center gap-2">
              <span
                className={`w-2 h-2 rounded-full flex-shrink-0 ${priorityDot[ticket.priority]}`}
              />
              <span
                className="text-xs font-mono font-medium"
                style={{ color: "var(--text-muted)" }}
              >
                {ticket.id}
              </span>
              <span
                className="text-xs ml-auto"
                style={{ color: "var(--text-xmuted)" }}
              >
                {ticket.status === "RESOLVED" ? "✓" : ""}
              </span>
            </div>
            <p
              className="text-xs leading-snug line-clamp-2"
              style={{ color: "var(--text-secondary)" }}
            >
              {ticket.title || "New ticket"}
            </p>
            <p className="text-xs" style={{ color: "var(--text-xmuted)" }}>
              {formatDistanceToNow(ticket.createdAt)}
            </p>

            {/* Delete button */}
            <button
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-0.5 rounded"
              style={{ color: "var(--text-xmuted)" }}
              onClick={(e) => {
                e.stopPropagation();
                onDeleteTicket(ticket.id);
              }}
              title="Close ticket"
            >
              <X size={12} />
            </button>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div
        className="px-4 py-3 border-t flex items-center justify-between"
        style={{ borderColor: "var(--border)" }}
      >
        <span className="text-xs" style={{ color: "var(--text-xmuted)" }}>
          Dept. F&amp;E
        </span>
        <button
          onClick={onToggleTheme}
          className="p-1.5 rounded-md transition-colors"
          style={{ color: "var(--text-muted)" }}
          title="Toggle theme"
        >
          {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
        </button>
      </div>
    </aside>
  );
}
