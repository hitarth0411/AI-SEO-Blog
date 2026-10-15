import { NextRequest, NextResponse } from "next/server";
import { BLOG_SYSTEM_PROMPT, ANTHROPIC_MODEL, ANTHROPIC_MAX_TOKENS } from "@/lib/constants";

// ─── POST /api/generate ───────────────────────────────────────────────────────
// Receives { topic } from the frontend, calls Anthropic on the server side
// (keeps the API key safe), returns parsed BlogResult JSON.

export async function POST(req: NextRequest) {
  try {
    const { topic } = await req.json();

    if (!topic || typeof topic !== "string" || !topic.trim()) {
      return NextResponse.json({ error: "Blog topic is required." }, { status: 400 });
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return NextResponse.json({ error: "Server configuration error: missing API key." }, { status: 500 });
    }

    // ── Call Anthropic ────────────────────────────────────────────────────────
    const anthropicRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type":         "application/json",
        "x-api-key":            apiKey,
        "anthropic-version":    "2023-06-01",
      },
      body: JSON.stringify({
        model:      ANTHROPIC_MODEL,
        max_tokens: ANTHROPIC_MAX_TOKENS,
        system:     BLOG_SYSTEM_PROMPT,
        messages:   [{ role: "user", content: `Blog Topic: ${topic.trim()}` }],
      }),
    });

    if (!anthropicRes.ok) {
      const err = await anthropicRes.json().catch(() => ({}));
      console.error("Anthropic API error:", err);
      return NextResponse.json({ error: "AI generation failed. Please try again." }, { status: 502 });
    }

    const data = await anthropicRes.json();
    const raw  = (data.content as { type: string; text: string }[])
      ?.map(b => (b.type === "text" ? b.text : ""))
      .join("") ?? "";

    // ── Parse JSON response ───────────────────────────────────────────────────
    const clean  = raw.replace(/```json|```/g, "").trim();
    const parsed = JSON.parse(clean);

    return NextResponse.json(parsed, { status: 200 });

  } catch (err) {
    console.error("Generate route error:", err);
    return NextResponse.json({ error: "Internal server error." }, { status: 500 });
  }
}
