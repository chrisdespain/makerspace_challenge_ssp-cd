import { Ticket } from "../components/types";

export function exportTicketAsMarkdown(ticket: Ticket): void {
  const lines: string[] = [
    `# Emotional Helpdesk — Ticket ${ticket.id}`,
    ``,
    `**Priority:** ${ticket.priority}`,
    `**Status:** ${ticket.status}`,
    `**Filed:** ${new Date(ticket.createdAt).toLocaleString()}`,
    `**Department:** Feelings & Emotions (F&E)`,
    `**SLA:** Whenever`,
    ``,
    `---`,
    ``,
    `## Ticket Thread`,
    ``,
  ];

  for (const msg of ticket.messages) {
    const label =
      msg.role === "user" ? "**YOU (Ticket Submitter)**" : "**[HELPDESK BOT] (Level 1 Support)**";
    const timestamp = new Date(msg.timestamp).toLocaleString();
    lines.push(`### ${label} — ${timestamp}`);
    lines.push(``);
    lines.push(msg.text);
    if (msg.starred) lines.push(`\n⭐ *Starred response*`);
    lines.push(``);
  }

  const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${ticket.id}.md`;
  a.click();
  URL.revokeObjectURL(url);
}
