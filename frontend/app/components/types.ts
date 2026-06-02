export type Priority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type TicketStatus = "OPEN" | "IN_PROGRESS" | "RESOLVED";

export interface Message {
  id: string;
  role: "user" | "agent";
  text: string;
  timestamp: number;
  starred: boolean;
}

export interface Ticket {
  id: string;
  title: string;
  priority: Priority;
  status: TicketStatus;
  messages: Message[];
  createdAt: number;
}

export const PRIORITY_LABELS: Record<Priority, string> = {
  LOW: "🟢 LOW — I'm fine, probably",
  MEDIUM: "🟡 MEDIUM — Could be worse",
  HIGH: "🔴 HIGH — Please advise",
  CRITICAL: "🚨 CRITICAL — Immediate emotional triage required",
};

export const PRIORITY_SHORT: Record<Priority, string> = {
  LOW: "LOW",
  MEDIUM: "MEDIUM",
  HIGH: "HIGH",
  CRITICAL: "CRITICAL",
};

export const STATUS_LABELS: Record<TicketStatus, string> = {
  OPEN: "OPEN",
  IN_PROGRESS: "IN PROGRESS",
  RESOLVED: "RESOLVED",
};
