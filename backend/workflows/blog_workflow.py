from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph

from services.keyword_service import generate_keywords
from services.topic_service import expand_topics
from services.planner_service import create_outline
from services.writer_service import write_blog
from services.seo_service import calculate_seo_score
from rag.retriever import retrieve_context


class BlogState(TypedDict, total=False):
    topic: str
    keywords: Dict
    related_topics: Dict
    outline: Dict
    content: str
    seo_score: int
    meta_title: str
    meta_description: str
    context: List[str] 


# Keyword Agent
def keyword_node(state: BlogState) -> BlogState:

    topic = state["topic"]
    keywords = generate_keywords(topic)

    return {
        **state,
        "keywords": keywords
    }


# RAG Retrieval Agent
def retrieval_node(state: BlogState) -> BlogState:

    topic = state["topic"]

    try:
        context = retrieve_context(topic)
    except Exception:
        context = []

    return {
        **state,
        "context": context
    }


#  Topic Expansion Agent
def topic_node(state: BlogState) -> BlogState:

    topic = state["topic"]
    related_topics = expand_topics(topic)

    return {
        **state,
        "related_topics": related_topics
    }


# Content Planner Agent
def planner_node(state: BlogState) -> BlogState:

    topic = state["topic"]

    outline = create_outline(topic)

    return {
        **state,
        "outline": outline
    }


# Blog Writing Agent (WITH RAG)
def writer_node(state: BlogState) -> BlogState:

    topic = state["topic"]
    outline = state["outline"]
    context = state.get("context", [])

    content = write_blog(topic, outline, context)

    return {
        **state,
        "content": content
    }


# SEO Optimization Agent
def seo_node(state: BlogState) -> BlogState:

    content = state["content"]
    keywords = state.get("keywords", {})
    topic = state["topic"]

    from services.seo_service import (
        calculate_seo_score,
        generate_meta_data,
        add_links
    )

    # Add links
    content = add_links(content)

    # Meta data
    meta = generate_meta_data(topic)

    # SEO score
    seo_score = calculate_seo_score(content, keywords)

    return {
        **state,
        "content": content,
        "seo_score": seo_score,
        "meta_title": meta["meta_title"],
        "meta_description": meta["meta_description"]
    }


# LangGraph Workflow
def run_blog_workflow(topic: str):

    graph = StateGraph(BlogState)

    # Nodes
    graph.add_node("keyword_agent", keyword_node)
    graph.add_node("retrieval_agent", retrieval_node)
    graph.add_node("topic_agent", topic_node)
    graph.add_node("planner_agent", planner_node)
    graph.add_node("writer_agent", writer_node)
    graph.add_node("seo_agent", seo_node)

    # Flow
    graph.set_entry_point("keyword_agent")

    graph.add_edge("keyword_agent", "retrieval_agent")
    graph.add_edge("retrieval_agent", "topic_agent")
    graph.add_edge("topic_agent", "planner_agent")
    graph.add_edge("planner_agent", "writer_agent")
    graph.add_edge("writer_agent", "seo_agent")

    graph.set_finish_point("seo_agent")

    app = graph.compile()

    result = app.invoke({
        "topic": topic
    })

    return result