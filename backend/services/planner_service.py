def create_outline(topic: str):

    title = f"Best Guide to {topic}"

    sections = [
        {
            "heading": "Introduction",
            "subtopics": []
        },
        {
            "heading": f"Benefits of {topic}",
            "subtopics": [
                "Improved productivity",
                "Better learning experience"
            ]
        },
        {
            "heading": f"Popular {topic}",
            "subtopics": [
                "Top tools",
                "Key features"
            ]
        },
        {
            "heading": f"How to choose the right {topic}",
            "subtopics": [
                "Important factors",
                "Ease of use"
            ]
        },
        {
            "heading": "Conclusion",
            "subtopics": []
        }
    ]

    return {
        "title": title,
        "sections": sections
    }