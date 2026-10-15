import json
from ai.config.llm_config import get_llm
from ai.prompts.keyword_prompt import KEYWORD_PROMPT


def parse_json(text):
    text = text.strip()
    if "```" in text:
        text = text.split("```")[1].lstrip("json").strip()
    start = text.find("{")
    end   = text.rfind("}") + 1
    return json.loads(text[start:end])


def keyword_agent(state):
    topic    = state["topic"]
    blog_type = state.get("plan", {}).get("blog_type", "informational")

    llm    = get_llm(fast=True)
    prompt = KEYWORD_PROMPT.format(topic=topic, blog_type=blog_type)
    raw    = llm.invoke(prompt).content

    try:
        keywords = parse_json(raw)
    except Exception as e:
        print(f"⚠️ Keyword parse failed: {e}")
        keywords = {
            "primary_keywords":   [topic],
            "secondary_keywords": [],
            "long_tail_keywords": [f"best {topic}"],
            "lsi_keywords":       []
        }

    print("\n================ KEYWORD OUTPUT ================\n")
    print(keywords)
    return {"keywords": keywords}
