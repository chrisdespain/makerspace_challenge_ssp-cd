"use client";

import { useRef, useEffect } from "react";
import { Send, X, Loader2 } from "lucide-react";

interface InputBarProps {
  input: string;
  loading: boolean;
  error: string | null;
  hasMessages: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
  onDismissError: () => void;
}

export default function InputBar({
  input,
  loading,
  error,
  hasMessages,
  onChange,
  onSubmit,
  onDismissError,
}: InputBarProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) onSubmit();
    }
  };

  const charCount = input.length;
  const showCounter = charCount > 200;

  return (
    <div
      className="flex-shrink-0 border-t px-4 py-4"
      style={{
        background: "var(--surface)",
        borderColor: "var(--border)",
      }}
    >
      {/* Error banner */}
      {error && (
        <div
          className="flex items-center justify-between gap-3 px-3 py-2 rounded-md mb-3 text-xs border"
          style={{
            background: "var(--error-bg)",
            color: "var(--error-text)",
            borderColor: "var(--error-border)",
          }}
        >
          <span>⚠ {error}</span>
          <button onClick={onDismissError} title="Dismiss">
            <X size={12} />
          </button>
        </div>
      )}

      <div
        className="flex items-end gap-3 rounded-xl border px-3 py-2.5 transition-colors"
        style={{
          borderColor: "var(--border-strong)",
          background: "var(--bg)",
        }}
      >
        <textarea
          ref={textareaRef}
          rows={1}
          value={input}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          placeholder="Describe your issue in detail. Attach feelings if applicable."
          className="flex-1 resize-none bg-transparent text-sm outline-none leading-relaxed"
          style={{
            color: "var(--text-primary)",
            caretColor: "var(--accent)",
            minHeight: "24px",
            maxHeight: "120px",
          }}
        />

        <div className="flex items-center gap-2 flex-shrink-0">
          {showCounter && (
            <span className="text-xs" style={{ color: "var(--text-xmuted)" }}>
              {charCount}
            </span>
          )}
          <button
            onClick={onSubmit}
            disabled={loading || !input.trim()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
            style={{
              background:
                loading || !input.trim() ? "var(--border)" : "var(--accent)",
              color:
                loading || !input.trim() ? "var(--text-xmuted)" : "white",
              cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            }}
          >
            {loading ? (
              <Loader2 size={12} className="animate-spin" />
            ) : (
              <Send size={12} />
            )}
            {hasMessages ? "Add Comment" : "Submit Ticket"}
          </button>
        </div>
      </div>

      <p className="text-xs mt-1.5 px-1" style={{ color: "var(--text-xmuted)" }}>
        Enter to submit · Shift+Enter for newline · Response time: unspecified
      </p>
    </div>
  );
}
