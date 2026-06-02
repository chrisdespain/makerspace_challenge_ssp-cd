"use client";

import { Download, ChevronDown } from "lucide-react";
import { Ticket, Priority, TicketStatus, PRIORITY_LABELS } from "./types";

interface TicketHeaderProps {
  ticket: Ticket;
  onUpdateStatus: (status: TicketStatus) => void;
  onUpdatePriority: (priority: Priority) => void;
  onExport: () => void;
}

const priorityStyles: Record<Priority, { bg: string; text: string }> = {
  LOW: { bg: "var(--tag-low)", text: "var(--tag-low-text)" },
  MEDIUM: { bg: "var(--tag-medium)", text: "var(--tag-medium-text)" },
  HIGH: { bg: "var(--tag-high)", text: "var(--tag-high-text)" },
  CRITICAL: { bg: "var(--tag-critical)", text: "var(--tag-critical-text)" },
};

const statusStyles: Record<TicketStatus, { bg: string; text: string }> = {
  OPEN: { bg: "var(--tag-open)", text: "var(--tag-open-text)" },
  IN_PROGRESS: { bg: "var(--tag-progress)", text: "var(--tag-progress-text)" },
  RESOLVED: { bg: "var(--tag-resolved)", text: "var(--tag-resolved-text)" },
};

const statusCycle: Record<TicketStatus, TicketStatus> = {
  OPEN: "IN_PROGRESS",
  IN_PROGRESS: "RESOLVED",
  RESOLVED: "OPEN",
};

const taglines = [
  "Assigned to: The Void",
  "SLA: Whenever",
  "Department: Feelings & Emotions (F&E)",
  "Escalation path: Screaming into a pillow",
  "Priority queue: First in, still there",
];

const PRIORITIES: Priority[] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
const STATUSES: TicketStatus[] = ["OPEN", "IN_PROGRESS", "RESOLVED"];

export default function TicketHeader({
  ticket,
  onUpdateStatus,
  onUpdatePriority,
  onExport,
}: TicketHeaderProps) {
  const tagline = taglines[ticket.id.charCodeAt(ticket.id.length - 1) % taglines.length];
  const pStyle = priorityStyles[ticket.priority];
  const sStyle = statusStyles[ticket.status];

  return (
    <div
      className="px-6 py-4 border-b flex-shrink-0"
      style={{
        background: "var(--surface)",
        borderColor: "var(--border)",
      }}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <div className="flex items-center gap-3 flex-wrap">
            <span
              className="font-mono text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              {ticket.id}
            </span>

            {/* Priority badge — clickable dropdown */}
            <div className="relative group">
              <button
                className="flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium"
                style={{ background: pStyle.bg, color: pStyle.text }}
              >
                {ticket.priority}
                <ChevronDown size={10} />
              </button>
              <div
                className="absolute left-0 top-full mt-1 z-10 rounded-md border shadow-lg overflow-hidden hidden group-focus-within:block group-hover:block"
                style={{
                  background: "var(--surface)",
                  borderColor: "var(--border)",
                  minWidth: "240px",
                }}
              >
                {PRIORITIES.map((p) => (
                  <button
                    key={p}
                    onClick={() => onUpdatePriority(p)}
                    className="flex w-full items-center px-3 py-2 text-xs text-left transition-colors"
                    style={{
                      color: "var(--text-secondary)",
                      background:
                        p === ticket.priority ? "var(--surface-hover)" : "transparent",
                    }}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.background = "var(--surface-hover)")
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.background =
                        p === ticket.priority ? "var(--surface-hover)" : "transparent")
                    }
                  >
                    {PRIORITY_LABELS[p]}
                  </button>
                ))}
              </div>
            </div>

            {/* Status badge — click to cycle */}
            <button
              onClick={() => onUpdateStatus(statusCycle[ticket.status])}
              className="px-2 py-0.5 rounded text-xs font-medium transition-opacity hover:opacity-80"
              style={{ background: sStyle.bg, color: sStyle.text }}
              title="Click to change status"
            >
              {ticket.status === "IN_PROGRESS" ? "IN PROGRESS" : ticket.status}
            </button>
          </div>

          <p
            className="text-xs mt-1.5 truncate max-w-lg"
            style={{ color: "var(--text-xmuted)" }}
          >
            {tagline}
          </p>

          {ticket.title && (
            <p
              className="text-sm mt-1.5 font-medium truncate max-w-lg"
              style={{ color: "var(--text-secondary)" }}
            >
              {ticket.title}
            </p>
          )}
        </div>

        <button
          onClick={onExport}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-colors flex-shrink-0"
          style={{
            color: "var(--text-muted)",
            borderColor: "var(--border)",
            background: "transparent",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "var(--surface-hover)";
            e.currentTarget.style.color = "var(--text-primary)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "transparent";
            e.currentTarget.style.color = "var(--text-muted)";
          }}
          title="Export ticket as Markdown"
        >
          <Download size={12} />
          Export
        </button>
      </div>
    </div>
  );
}
