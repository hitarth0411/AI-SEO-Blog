from rag.chunker import chunk_text
from rag.embedder import get_embedding
from rag.vector_store import add_embeddings

def load_data():

    with open("rag/data.txt", "r") as f:
        text = f.read()

    chunks = chunk_text(text)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    add_embeddings(embeddings, chunks)

    print("Data loaded successfully")

if __name__ == "__main__":
    load_data()