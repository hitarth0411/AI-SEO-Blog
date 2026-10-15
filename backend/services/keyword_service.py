def generate_keywords(topic: str):

    primary_keyword = topic

    secondary_keywords = [
        f"best {topic}",
        f"{topic} tools",
        f"{topic} guide",
        f"{topic} tips",
        f"{topic} for beginners"
    ]

    return {
        "primary": primary_keyword,
        "secondary": secondary_keywords
    }