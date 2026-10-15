"use client";

interface TableOfContentsProps {
  items: string[];
}

export default function TableOfContents({ items }: TableOfContentsProps) {
  return (
    <div className="ocard fu fu3">
      <div className="sec-label">Table of Contents</div>
      {items.map((item, i) => (
        <div key={i} className="toc-row">
          <span className="toc-n">{String(i + 1).padStart(2, "0")}</span>
          <span style={{ color: "var(--text-primary)", fontSize: 14 }}>{item}</span>
        </div>
      ))}
    </div>
  );
}
