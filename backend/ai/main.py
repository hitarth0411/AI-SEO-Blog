import asyncio

from ai.graph.blog_graph import blog_graph


async def generate_blog(topic: str):

    initial_state = {
        "topic": topic,
        "plan": {},
        "research": [],
        "outline": {},
        "keywords": {},
        "draft": "",
        "final_blog": "",
        "seo": {},
    }

    try:
        result = await blog_graph.ainvoke(initial_state)

        # =========================
        # CRITICAL SAFETY CHECK
        # =========================
        if not isinstance(result, dict):
            raise ValueError(f"Graph returned invalid type: {type(result)}")

        print("\n================ FINAL STATE =================\n")
        print(type(result))
        print("\n=============================================\n")

        return {
            "content": result.get("final_blog", ""),
            "plan": result.get("plan", {}),
            "research": result.get("research", []),
            "outline": result.get("outline", {}),
            "keywords": result.get("keywords", {}),
            "seo": result.get("seo", {}),
        }

    except asyncio.CancelledError:
        raise
    except Exception as e:
        print("\n GENERATE BLOG ERROR:", str(e), "\n")

        return {
            "content": "",
            "plan": {},
            "research": [],
            "outline": {},
            "keywords": {},
            "seo": {},
            "error": str(e)
        }
