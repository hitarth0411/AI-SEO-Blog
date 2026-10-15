"use client";

import { useEffect, useMemo, useState } from "react";

const STEPS = [
  "Planning agent is working...",
  "Planning is done. Moving to writing agent...",
  "Writing agent is working...",
  "Writing is done. Moving to SEO agent...",
  "SEO optimization agent is working...",
] as const;

export default function AIWorking() {
  const [idx, setIdx] = useState(0);

  useEffect(() => {
    const t = window.setInterval(() => {
      setIdx(v => Math.min(v + 1, STEPS.length - 1));
    }, 1500);
    return () => window.clearInterval(t);
  }, []);

  const active = useMemo(() => STEPS[idx], [idx]);

  return (
    <div style={{
      marginTop: 22,
      borderRadius: 18,
      border: "1px solid var(--border)",
      background: "rgba(255,255,255,0.7)",
      backdropFilter: "blur(10px)",
      boxShadow: "0 10px 30px rgba(0,0,0,0.06)",
      padding: "16px 16px 14px",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <div className="ai-orb" aria-hidden="true" />
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 13.5, fontWeight: 700, color: "var(--text-primary)" }}>
            AI is working
          </div>
          <div style={{ fontSize: 12.5, color: "var(--text-secondary)" }}>
            {active} <span className="typing-dots" aria-hidden="true" />
          </div>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {STEPS.map((s, i) => {
          const done = i < idx;
          const current = i === idx;
          return (
            <div key={s} style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div style={{
                width: 18,
                height: 18,
                borderRadius: 999,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 12,
                background: done ? "rgba(34,197,94,0.14)" : "rgba(79,70,229,0.10)",
                color: done ? "var(--accent)" : "var(--primary)",
                border: `1px solid ${done ? "rgba(34,197,94,0.25)" : "rgba(79,70,229,0.20)"}`,
              }}>
                {done ? "✓" : current ? "•" : ""}
              </div>
              <div style={{
                fontSize: 13,
                color: done ? "var(--text-secondary)" : "var(--text-primary)",
                fontWeight: current ? 600 : 500,
              }}>
                {s}
              </div>
              {current && <div className="ai-cursor" aria-hidden="true" />}
            </div>
          );
        })}
      </div>
    </div>
  );
}

