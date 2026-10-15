import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []

def add_embeddings(embeddings, texts):
    global documents

    index.add(np.array(embeddings).astype("float32"))
    documents.extend(texts)

def search(query_embedding, k=3):

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"), k
    )

    results = [documents[i] for i in indices[0]]

    return results