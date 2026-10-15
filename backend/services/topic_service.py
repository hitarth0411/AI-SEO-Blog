def expand_topics(topic: str):

    related_topics = [
        f"benefits of {topic}",
        f"popular {topic}",
        f"how to choose {topic}",
        f"future of {topic}"
    ]

    return {
        "related_topics": related_topics
    }