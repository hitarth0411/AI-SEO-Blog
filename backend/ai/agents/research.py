import os
import json
import logging

from tavily import TavilyClient
from ai.config.llm_config import get_llm
from ai.prompts.research_prompt import RESEARCH_PROMPT
from ai.utils.json_utils import parse_json as parse_llm_json

logger = logging.getLogger(__name__)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def debug_preview(label: str, value, limit: int = 1200):
    print(f"\n[{label}]\n")
    if isinstance(value, str):
        print(value[:limit])
    else:
        try:
            print(json.dumps(value, indent=2)[:limit])
        except Exception:
            print(str(value)[:limit])


# =========================
# SEARCH
# =========================
def get_research_data(topic: str):
    queries = [
        f"{topic} tools",
        f"{topic} comparison",
        f"{topic} features use cases"
    ]

    all_results = []
    failed_queries = 0

    for q in queries:
        try:
            res = tavily.search(
                query=q,
                search_depth="basic",
                max_results=2
            )
        except Exception as exc:
            failed_queries += 1
            logger.warning("Research search failed; continuing with remaining queries: %s", exc)
            continue

        for r in res.get("results", []):
            all_results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": (r.get("content") or "")[:400]
            })

    # Deduplicate
    seen = set()
    unique = []
    for item in all_results:
        if item["url"] and item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    if failed_queries == len(queries):
        logger.error("All research searches failed; outline generation will continue without research.")

    return unique


# =========================
# FORMAT
# =========================
def format_research_data(data):
    if not data:
        return ""

    formatted = ""
    for i, item in enumerate(data, 1):
        formatted += f"""
[{i}]
Title: {item['title']}
URL: {item['url']}
Content: {item['content']}
"""
    return formatted.strip()


# =========================
# MAIN FUNCTION (IMPORTANT NAME)
# =========================
def research_agent(state: dict):
    try:
        topic = state.get("topic")
        print("\n================ RESEARCH STARTED ================\n")
        print(f"Topic: {topic}")

        raw_data = get_research_data(topic)
        print(f"Raw result count: {len(raw_data)}")
        debug_preview(
            "RAW RESEARCH RESULTS",
            [{"title": item.get("title", ""), "url": item.get("url", "")} for item in raw_data[:3]],
        )

        if not raw_data:
            research = [
                {
                    "title": "No data available",
                    "summary": "No relevant research data was found for this topic.",
                    "key_points": [],
                    "source": ""
                }
            ]
            print("\n[RESEARCH FALLBACK] No raw data found.\n")
            return {"research": research}

        formatted_data = format_research_data(raw_data)
        debug_preview("FORMATTED RESEARCH INPUT", formatted_data)

        prompt = RESEARCH_PROMPT.format(
            topic=topic,
            research_data=formatted_data
        )

        llm = get_llm(temperature=0.2)

        response = llm.invoke(prompt)
        content = response.content.strip()
        debug_preview("RAW RESEARCH AGENT OUTPUT", content)

        research = parse_llm_json(content)
        if not isinstance(research, list):
            raise ValueError("Research model output must be a JSON array.")
        research = [item for item in research if isinstance(item, dict)]
        print("\n================ RESEARCH OUTPUT ================\n")
        print(f"Parsed research entries: {len(research)}")
        debug_preview("RESEARCH OUTPUT PREVIEW", research[:3])
        return {"research": research}

    except Exception as exc:
        logger.exception("Research failed; outline generation will continue without research: %s", exc)
        return {"research": []}
