from rag.embedder import get_embedding
from rag.vector_store import search

def retrieve_context(query: str):

    query_embedding = get_embedding(query)

    results = search(query_embedding)

    return results