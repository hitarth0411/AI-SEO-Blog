def calculate_seo_score(content: str, keywords: dict):

    score = 0

    primary_keyword = keywords["primary"]
    secondary_keywords = keywords["secondary"]

    # Check keyword presence
    if primary_keyword.lower() in content.lower():
        score += 30

    # Check secondary keywords
    for kw in secondary_keywords:
        if kw.lower() in content.lower():
            score += 10

    # Check blog length
    if len(content.split()) > 300:
        score += 20

    # Check headings
    if "#" in content:
        score += 20

    # Links presence
    if "http" in content:
        score += 20

    return min(score, 100)

def generate_meta_data(topic: str):

    meta_title = f"Best Guide to {topic} (2026 SEO Optimized)"

    meta_description = (
        f"Learn everything about {topic}. "
        f"This SEO optimized guide explains tools, benefits, and tips."
    )

    return {
        "meta_title": meta_title,
        "meta_description": meta_description
    }

def add_links(content: str):

    external_link = "https://openai.com"
    internal_link = "/blogs/ai-tools-guide"

    content += "\n\n## Useful Resources\n"
    content += f"- Learn more: {external_link}\n"
    content += f"- Related article: {internal_link}\n"

    return content