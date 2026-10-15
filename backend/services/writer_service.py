def write_blog(topic: str, outline: dict, context=None):

    title = outline["title"]
    sections = outline["sections"]

    content = f"# {title}\n\n"

    # Introduction
    content += "## Introduction\n"
    content += (
        f"{topic} is an important topic in today's digital world. "
        f"In this blog, we will explore various aspects of {topic}, "
        f"including its benefits, tools, and practical applications.\n\n"
    )

    # RAG Context (Background Knowledge)
    if context:
        content += "## Background Knowledge\n"
        for c in context:
            content += f"{c}\n\n"

    # Main Sections
    for section in sections:

        heading = section["heading"]
        subtopics = section["subtopics"]

        content += f"## {heading}\n"
        content += (
            f"{heading} plays a key role in understanding {topic}. "
            f"This section provides useful insights and explanations.\n\n"
        )

        # H3 subsections
        for sub in subtopics:
            content += f"### {sub}\n"
            content += (
                f"{sub} is an important aspect of {topic}. "
                f"It helps users understand real-world applications "
                f"and practical usage.\n\n"
            )

    # Conclusion
    content += "## Conclusion\n"
    content += (
        f"In conclusion, {topic} continues to grow and impact different fields. "
        f"By understanding its concepts, tools, and applications, "
        f"you can make better use of {topic} in real-life scenarios.\n"
    )

    return content