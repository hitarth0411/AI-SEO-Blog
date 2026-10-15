"use client";

import { useState } from "react";
import { BlogResult, ExportFormat } from "@/types/blog";
import { exportBlog } from "@/lib/exportUtils";
import { Icons } from "@/components/ui/Icons";

interface ExportPanelProps {
  result:   BlogResult;
  onCopy:   (text: string, id: string) => void;
  copiedId: string;
  onRegen:  () => void;
}

export default function ExportPanel({ result, onCopy, copiedId, onRegen }: ExportPanelProps) {
  const [showFormats, setShowFormats] = useState(false);

  const formats: { label: string; fmt: ExportFormat; ext: string }[] = [
    { label: "Plain Text (.txt)",   fmt: "txt",      ext: ".txt"  },
    { label: "Markdown (.md)",      fmt: "markdown",  ext: ".md"   },
    { label: "HTML (.html)",        fmt: "html",      ext: ".html" },
  ];

  return (
    <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, paddingBottom: 56, position: "relative" }}>

      {/* Copy All */}
      <button
        className="btn-ghost"
        onClick={() => onCopy(`# ${result.title}\n\n${result.content}`, "a")}
      >
        <span style={{ display: "flex" }}>
          {copiedId === "a" ? Icons.check : Icons.copy}
        </span>
        {copiedId === "a" ? "Copied!" : "Copy All"}
      </button>

      {/* Download dropdown */}
      <div style={{ position: "relative" }}>
        <button
          className="btn-ghost"
          onClick={() => setShowFormats(v => !v)}
        >
          <span style={{ display: "flex" }}>{Icons.download}</span>
          Download ▾
        </button>

        {showFormats && (
          <div style={{
            position: "absolute", bottom: "calc(100% + 6px)", right: 0,
            background: "var(--card-bg)", border: "1px solid var(--border)",
            borderRadius: "var(--r-md)", boxShadow: "var(--sh-md)",
            overflow: "hidden", minWidth: 180, zIndex: 20,
          }}>
            {formats.map(({ label, fmt }) => (
              <button
                key={fmt}
                onClick={() => { exportBlog(result, fmt); setShowFormats(false); }}
                style={{
                  display: "block", width: "100%", textAlign: "left",
                  padding: "10px 14px", background: "transparent", border: "none",
                  fontFamily: "var(--sans)", fontSize: 13, color: "var(--text-secondary)",
                  cursor: "pointer", transition: "background 0.1s",
                }}
                onMouseEnter={e => (e.currentTarget.style.background = "var(--hover-bg)")}
                onMouseLeave={e => (e.currentTarget.style.background = "transparent")}
              >
                {label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Regenerate */}
      <button className="btn-primary" onClick={onRegen}>
        <span style={{ display: "flex" }}>{Icons.refresh}</span>
        Regenerate
      </button>
    </div>
  );
}
