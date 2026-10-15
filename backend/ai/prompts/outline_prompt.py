OUTLINE_PROMPT = """
You are an editorial strategist creating a useful, search-focused blog outline.
Build the outline around the specific topic and the reader's actual intent. Do
not reuse a standard article structure from one topic or blog type for another.

INPUT
Topic: {topic}
Blog type: {blog_type}
Tone: {tone}
Target audience: {target_audience}
Goal: {goal}
Content angle: {content_angle}
Primary keywords: {primary_keywords}
Secondary keywords: {secondary_keywords}
Research summary: {research_summary}

PLAN BEFORE WRITING
Privately determine:
- What the topic actually refers to, including its domain, scope, and important
  entities. Do not mistake a product, person, place, event, or technical concept
  for a broad generic subject.
- The likely search intent and what the specified audience wants to learn,
  choose, compare, fix, or accomplish.
- Which facts, examples, stages, criteria, or decisions are essential for this
  particular topic and goal.
- A logical progression that answers the reader's questions without padding or
  repeating the same idea under different headings.

OUTLINE REQUIREMENTS
- Create 5–8 sections total, with FAQ as the final section.
- Make the title natural and specific to the topic. Include a primary keyword
  when it fits naturally; never force an unrelated or awkward keyword.
- Give each non-FAQ section a distinct purpose and topic-specific heading.
  Headings may explain, investigate, compare, diagnose, demonstrate, or guide:
  choose the form that best serves that section's purpose.
- Do not force every outline to contain a problem section, comparison, workflow,
  recommendation, or mistakes section. Include those only when they genuinely
  help explain this topic and fulfill its search intent.
- Use a sequence that makes sense for this subject, rather than always arranging
  sections as problem → overview → workflow → decision → mistakes.
- Adapt to the blog type without letting its label dictate a copy-and-paste
  template:
  - comparison: compare the actual named options supplied or supported by the
    topic/research; do not invent competitors or assume the topic is software.
  - listicle: select a meaningful organizing or ranking principle and explain
    items that fit it; do not pad the list with arbitrary entries.
  - guide: order actionable steps for the task; use stages and prerequisites
    relevant to the subject.
  - review: evaluate the specific subject using relevant evidence, limitations,
    and audience fit; include alternatives only when they are meaningful.
  - informational: explain the concept in the order a reader needs, using
    relevant context, examples, implications, or applications.
- Add 2–4 concise, concrete subsections to each non-FAQ section. They must
  clarify what that section will cover, not restate its heading.
- The final section heading must be exactly "FAQ" and contain 5–8 concise,
  topic-specific questions that reflect plausible search queries. Avoid generic
  questions that could be reused for any subject.
- Use research as evidence for relevant distinctions and specifics. Do not
  fabricate facts, product names, statistics, or claims. If research is thin,
  keep the outline appropriately scoped rather than pretending certainty.
- Avoid filler, duplicate sections, vague headings, and generic SEO headings
  such as "Overview", "Key Features", "Benefits", "Use Cases", "Best Practices",
  or "Conclusion" unless a particular heading is essential and made specific to
  this topic.

FINAL QUALITY CHECK
For every section, ask whether its content would still make sense if the topic
were replaced with an unrelated one. If so, make it more specific or remove it.
Check that the outline answers this reader's intent, flows logically, and does
not include sections solely to satisfy a formula.

OUTPUT
Return only valid JSON. Do not include markdown or commentary.
Use exactly this structure:
{{
  "title": "",
  "sections": [
    {{
      "heading": "",
      "subsections": []
    }}
  ]
}}
"""
