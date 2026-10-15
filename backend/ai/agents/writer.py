import json
import time
from ai.config.llm_config import get_llm
from ai.prompts.writer_prompt import FULL_BLOG_PROMPT, SECTION_WRITER_PROMPT


def call_llm(llm, prompt, retries=2, wait=12):
    """Call LLM with retry on rate limit."""
    for attempt in range(1, retries + 1):
        try:
            return llm.invoke(prompt).content.strip()
        except Exception as e:
            msg = str(e)
            if ("429" in msg or "rate_limit" in msg.lower()) and attempt < retries:
                print(f"⚠️ Rate limit — waiting {wait}s (attempt {attempt}/{retries})...")
                time.sleep(wait)
            else:
                raise


def clean_section_content(text, heading):
    """Strip stray headings and duplicate lines from a section."""
    for fmt in (f"## {heading}", f"# {heading}", f"**{heading}**"):
        text = text.replace(fmt, "")

    lines = [l for l in text.split("\n") if l.strip() not in ("#", "##", "###")]
    seen, result = set(), []
    for line in lines:
        key = line.strip()
        if key not in seen:
            result.append(line)
            seen.add(key)

    return "\n".join(result).strip()


def clean_full_blog(text, title):
    content = text.strip()

    if content.startswith("```"):
        content = content.replace("```markdown", "").replace("```md", "").replace("```", "").strip()

    lines = content.splitlines()
    filtered_lines = []
    seen_title = False
    normalized_title = str(title).strip().lower()

    for index, line in enumerate(lines):
        stripped = line.strip()
        normalized_line = stripped.lstrip("#").strip().lower()

        if normalized_title and normalized_line == normalized_title:
            if seen_title or index > 0:
                continue
            seen_title = True

        filtered_lines.append(line)

    content = "\n".join(filtered_lines).strip()
    content = content.replace("\n#### ", "\n### ")
    content = content.replace("\n##### ", "\n### ")

    if not content.startswith("# "):
        content = f"# {title}\n\n{content}"

    return content.strip()


def build_research_text(research):
    compact_research = []
    for item in research[:5]:
        if not isinstance(item, dict):
            continue
        compact_research.append({
            "title": item.get("title", ""),
            "summary": item.get("summary", ""),
            "key_points": item.get("key_points", [])[:3],
            "source": item.get("source", ""),
        })

    return json.dumps(compact_research, ensure_ascii=False, indent=2)


def build_outline_text(title, sections):
    lines = [f"Title: {title}"]
    for index, section in enumerate(sections, start=1):
        heading = section.get("heading", "")
        subsections = section.get("subsections", [])
        lines.append(f"{index}. {heading}")
        for sub in subsections:
            lines.append(f"   - {sub}")
    return "\n".join(lines)


def has_expected_headings(content, title, sections):
    if not content.strip().startswith("# "):
        return False

    title_line = content.splitlines()[0].strip()
    if title and title.lower() not in title_line.lower():
        return False

    return all(f"## {section.get('heading', '')}" in content for section in sections if section.get("heading"))


def write_full_blog(llm, state, plan, keywords, outline, research):
    sections = outline.get("sections", [])
    title = outline.get("title", state["topic"])
    prompt = FULL_BLOG_PROMPT.format(
        topic=state["topic"],
        blog_type=plan.get("blog_type", "informational"),
        tone=plan.get("tone", "professional"),
        target_audience=plan.get("target_audience", "general readers"),
        goal=plan.get("goal", "help the reader make a confident decision"),
        content_angle=plan.get("content_angle", "practical and specific"),
        estimated_word_count=plan.get("estimated_word_count", "1200-1600"),
        reading_level=plan.get("reading_level", "intermediate"),
        primary_keywords=json.dumps(keywords.get("primary_keywords", [])[:3]),
        secondary_keywords=json.dumps(keywords.get("secondary_keywords", [])[:5]),
        lsi_keywords=json.dumps(keywords.get("lsi_keywords", [])[:5]),
        research=build_research_text(research),
        outline=build_outline_text(title, sections),
    )

    content = clean_full_blog(call_llm(llm, prompt), title)
    if not has_expected_headings(content, title, sections):
        raise ValueError("Full blog output did not follow the outline headings.")
    return content


def write_by_section(llm, state, plan, keywords, outline, research):
    sections = outline.get("sections", [])
    title = outline.get("title", state["topic"])
    total_sections = len(sections)
    research_text = build_research_text(research)
    full_blog = f"# {title}\n\n"

    for i, section in enumerate(sections):
        heading = section.get("heading", "")
        subsections = section.get("subsections", [])
        pos = i + 1
        is_intro = pos == 1
        is_conc = pos == total_sections
        is_table = any(w in heading.lower() for w in ("comparison", "table", "compare", "vs"))

        print(f"\n🔹 Writing fallback section {pos}/{total_sections}: {heading}")

        prompt = SECTION_WRITER_PROMPT.format(
            topic=state["topic"],
            blog_type=plan.get("blog_type", "informational"),
            tone=plan.get("tone", "professional"),
            heading=heading,
            subsections=json.dumps(subsections),
            is_intro=is_intro,
            is_conclusion=is_conc,
            is_table=is_table,
            primary_keywords=json.dumps(keywords.get("primary_keywords", [])[:3]),
            secondary_keywords=json.dumps(keywords.get("secondary_keywords", [])[:4]),
            research=research_text,
        )

        content = clean_section_content(call_llm(llm, prompt), heading)
        full_blog += f"## {heading}\n\n{content}\n\n"

    return full_blog.strip()


def writer_agent(state):
    llm = get_llm(fast=False, temperature=0.35)
    plan = state.get("plan", {})
    keywords = state.get("keywords", {})
    outline = state.get("outline", {})
    research = state.get("research", [])

    print("\n================ WRITING STARTED ================\n")

    try:
        full_blog = write_full_blog(llm, state, plan, keywords, outline, research)
    except Exception as e:
        print(f"⚠️ Full blog generation failed, using section fallback: {e}")
        full_blog = write_by_section(llm, state, plan, keywords, outline, research)

    state["final_blog"] = full_blog
    print("\n================ FINAL BLOG GENERATED ================\n")
    return state
