"use client";

import { BlogResult } from "@/types/blog";

interface SEOPanelProps {
  result: BlogResult;
}

export default function SEOPanel({ result }: SEOPanelProps) {

  // Ensure keywords is always an array
  const keywords = Array.isArray(result.keywords)
    ? result.keywords
    : typeof result.keywords === "string"
    ? result.keywords.split(",").map((k: string) => k.trim())
    : [];

  return (
    <div className="ocard fu fu2">
      <div className="sec-label">SEO Metadata</div>

      <div style={{ display: "flex", flexDirection: "column", gap: 15 }}>

        {/* Meta Title */}
        <div>
          <div
            style={{
              fontSize: 11,
              color: "var(--text-tertiary)",
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "0.07em",
              marginBottom: 6,
            }}
          >
            Meta Title
          </div>

          <div
            style={{
              fontSize: 14,
              color: "var(--text-primary)",
              lineHeight: 1.55,
              padding: "10px 13px",
              background: "#FAFAF8",
              borderRadius: "var(--r-sm)",
              border: "1px solid var(--border-light)",
            }}
          >
            {result.meta_title || "No meta title available"}
          </div>
        </div>

        {/* Meta Description */}
        <div>
          <div
            style={{
              fontSize: 11,
              color: "var(--text-tertiary)",
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "0.07em",
              marginBottom: 6,
            }}
          >
            Meta Description
          </div>

          <div
            style={{
              fontSize: 14,
              color: "var(--text-secondary)",
              lineHeight: 1.6,
              padding: "10px 13px",
              background: "#FAFAF8",
              borderRadius: "var(--r-sm)",
              border: "1px solid var(--border-light)",
            }}
          >
            {result.meta_description || "No meta description available"}
          </div>
        </div>

        {/* Keywords */}
        <div>
          <div
            style={{
              fontSize: 11,
              color: "var(--text-tertiary)",
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "0.07em",
              marginBottom: 8,
            }}
          >
            Focus Keywords
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {keywords.length > 0 ? (
              keywords.map((kw: string, i: number) => (
                <span key={i} className="tag">
                  {kw}
                </span>
              ))
            ) : (
              <span
                style={{
                  fontSize: 13,
                  color: "var(--text-tertiary)",
                }}
              >
                No keywords available
              </span>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
