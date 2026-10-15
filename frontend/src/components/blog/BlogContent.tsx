"use client";

import { useState } from "react";
import { Icons } from "@/components/ui/Icons";
import { renderBlogHtml } from "@/lib/renderBlogHtml";
import { useTypewriter } from "@/hooks/useTypewriter";

interface BlogContentProps {
  content:  string;
  onCopy:   (text: string, id: string) => void;
  copiedId: string;
}

export default function BlogContent({ content, onCopy, copiedId }: BlogContentProps) {
  const { out, done } = useTypewriter(content);
  const [editing,      setEditing]      = useState(false);
  const [editedContent, setEditedContent] = useState(content);
  const [saved,         setSaved]         = useState(false);

  // once typewriter finishes, keep the full content in the editor
  const displayContent = done ? editedContent : out;

  function handleSave() {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
    setEditing(false);
  }

  return (
    <div className="ocard fu fu4">
      {/* Header row */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        marginBottom: 20,
      }}>
        <div className="sec-label" style={{ marginBottom: 0 }}>Blog Content</div>
        <div style={{ display: "flex", gap: 8 }}>
          {done && (
            <button
              className="btn-ghost"
              style={{ padding: "5px 11px", fontSize: 12 }}
              onClick={() => setEditing(v => !v)}
            >
              {editing ? "Preview" : "✏ Edit"}
            </button>
          )}
          {editing && (
            <button
              className="btn-ghost"
              style={{ padding: "5px 11px", fontSize: 12, background: saved ? "#F0FDF4" : undefined }}
              onClick={handleSave}
            >
              <span style={{ display: "flex" }}>{saved ? Icons.check : null}</span>
              {saved ? "Saved!" : "Save"}
            </button>
          )}
          <button
            className="btn-ghost"
            style={{ padding: "5px 11px", fontSize: 12 }}
            onClick={() => onCopy(editedContent, "c")}
          >
            <span style={{ display: "flex" }}>
              {copiedId === "c" ? Icons.check : Icons.copy}
            </span>
            {copiedId === "c" ? "Copied" : "Copy"}
          </button>
        </div>
      </div>

      {/* Edit mode */}
      {editing ? (
        <textarea
          value={editedContent}
          onChange={e => setEditedContent(e.target.value)}
          style={{
            width: "100%", minHeight: 520,
            border: "1px solid var(--border)", borderRadius: "var(--r-md)",
            padding: "16px", fontSize: 14, lineHeight: 1.75,
            color: "var(--text-primary)", background: "#FAFAF8",
            fontFamily: "var(--sans)", resize: "vertical",
          }}
        />
      ) : (
        <>
          <div
            className="blog-body"
            dangerouslySetInnerHTML={{ __html: renderBlogHtml(displayContent) }}
          />
          {!done && <span className="cursor" />}
        </>
      )}
    </div>
  );
}
