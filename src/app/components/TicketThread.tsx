"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Copy, Star } from "lucide-react";
import { Message } from "./types";
import { formatDistanceToNow } from "../utils/time";

interface TicketThreadProps {
  messages: Message[];
  onStarMessage: (id: string) => void;
  onCopyMessage: (text: string) => void;
}

export default function TicketThread({
  messages,
  onStarMessage,
  onCopyMessage,
}: TicketThreadProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length]);

  return (
    <div data-testid="ticket-thread" className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
      <AnimatePresence initial={false}>
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className={`flex flex-col gap-1 ${msg.role === "user" ? "items-end" : "items-start"}`}
          >
            {/* Label */}
            <span
              className="text-xs font-mono px-1"
              style={{ color: "var(--text-xmuted)" }}
            >
              {msg.role === "user"
                ? "YOU (Ticket Submitter)"
                : "[HELPDESK BOT] (Level 1 Support)"}
            </span>

            {/* Bubble */}
            <div
              className={`relative group max-w-[75%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                msg.starred ? "ring-2 ring-yellow-400/60" : ""
              }`}
              style={
                msg.role === "user"
                  ? {
                      background: "var(--accent)",
                      color: "white",
                      borderBottomRightRadius: "4px",
                    }
                  : {
                      background: "var(--surface)",
                      color: "var(--text-primary)",
                      border: "1px solid var(--border)",
                      borderBottomLeftRadius: "4px",
                    }
              }
            >
              <p style={{ whiteSpace: "pre-wrap" }}>{msg.text}</p>

              {/* Action buttons — agent messages only */}
              {msg.role === "agent" && (
                <div className="absolute -bottom-7 left-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onCopyMessage(msg.text)}
                    className="flex items-center gap-1 px-2 py-1 rounded text-xs border transition-colors"
                    style={{
                      color: "var(--text-muted)",
                      borderColor: "var(--border)",
                      background: "var(--surface)",
                    }}
                    title="Copy response"
                  >
                    <Copy size={10} />
                    Copy
                  </button>
                  <button
                    onClick={() => onStarMessage(msg.id)}
                    className="flex items-center gap-1 px-2 py-1 rounded text-xs border transition-colors"
                    style={{
                      color: msg.starred ? "var(--star)" : "var(--text-muted)",
                      borderColor: msg.starred ? "var(--star)" : "var(--border)",
                      background: "var(--surface)",
                    }}
                    title={msg.starred ? "Unstar" : "Star this response"}
                  >
                    <Star size={10} fill={msg.starred ? "currentColor" : "none"} />
                    {msg.starred ? "Starred" : "Star"}
                  </button>
                </div>
              )}
            </div>

            {/* Timestamp */}
            <span
              className="text-xs px-1"
              style={{ color: "var(--text-xmuted)" }}
            >
              {formatDistanceToNow(msg.timestamp)}
            </span>
          </motion.div>
        ))}
      </AnimatePresence>

      <div ref={bottomRef} className="h-8" />
    </div>
  );
}
