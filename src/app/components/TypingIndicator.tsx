"use client";

import { motion } from "framer-motion";

export default function TypingIndicator() {
  return (
    <div className="flex flex-col items-start gap-1 px-6 py-2">
      <span
        className="text-xs font-mono px-1"
        style={{ color: "var(--text-xmuted)" }}
      >
        [HELPDESK BOT] (Level 1 Support)
      </span>
      <div
        className="flex items-center gap-3 rounded-xl px-4 py-3 border"
        style={{
          background: "var(--surface)",
          borderColor: "var(--border)",
          borderBottomLeftRadius: "4px",
        }}
      >
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.span
              key={i}
              className="w-1.5 h-1.5 rounded-full"
              style={{ background: "var(--text-xmuted)" }}
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{
                duration: 1.2,
                repeat: Infinity,
                delay: i * 0.2,
                ease: "easeInOut",
              }}
            />
          ))}
        </div>
        <span className="text-xs italic" style={{ color: "var(--text-muted)" }}>
          composing a response... please hold
        </span>
      </div>
    </div>
  );
}
