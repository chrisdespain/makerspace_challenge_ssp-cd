"use client";

const ISSUES = [
  "My motivation has stopped responding",
  "Unexpected feelings in production",
  "Memory leak in my personal life",
  "My work-life balance threw a 500 error",
  "Critical: imposter syndrome detected",
  "Requesting a hotfix for my anxiety",
];

interface SuggestedIssuesProps {
  onSelect: (text: string) => void;
}

export default function SuggestedIssues({ onSelect }: SuggestedIssuesProps) {
  return (
    <div className="px-6 pb-4">
      <p className="text-xs mb-2.5" style={{ color: "var(--text-xmuted)" }}>
        Common issues — select one to file immediately:
      </p>
      <div className="flex flex-wrap gap-2">
        {ISSUES.map((issue) => (
          <button
            key={issue}
            onClick={() => onSelect(issue)}
            className="px-3 py-1.5 rounded-full text-xs border transition-colors"
            style={{
              color: "var(--text-secondary)",
              borderColor: "var(--border)",
              background: "var(--surface)",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "var(--accent)";
              e.currentTarget.style.color = "var(--accent)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "var(--border)";
              e.currentTarget.style.color = "var(--text-secondary)";
            }}
          >
            {issue}
          </button>
        ))}
      </div>
    </div>
  );
}
