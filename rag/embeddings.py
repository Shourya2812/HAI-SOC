"""
rag/embeddings.py

Generates vector embeddings for HAI-SOC RAG chunks
using the local Ollama embedding model.
"""

import requests


# --------------------------------------------------
# Configuration
# --------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/embed"

EMBEDDING_MODEL = "granite-embedding:278m"


# --------------------------------------------------
# Generate Embedding
# --------------------------------------------------

def embed_text(text: str) -> list[float]:
    """
    Generate an embedding vector for a single text.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["embeddings"][0]


# --------------------------------------------------
# Embed Multiple Texts
# --------------------------------------------------

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts.
    """

    if not texts:
        return []

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    return data["embeddings"]


# --------------------------------------------------
# Embed Chunks
# --------------------------------------------------

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Add embeddings to every RAG chunk.

    The original chunk metadata is preserved.
    """

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embed_texts(texts)

    if len(embeddings) != len(chunks):
        raise RuntimeError(
            "Number of embeddings does not match "
            "number of chunks."
        )

    embedded_chunks = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):

        embedded_chunk = {
            **chunk,
            "embedding": embedding,
        }

        embedded_chunks.append(
            embedded_chunk
        )

    return embedded_chunks


# --------------------------------------------------
# Main Test
# --------------------------------------------------

if __name__ == "__main__":

    test_text = (
        "PACS user exported patient data "
        "during an unusual hour."
    )

    embedding = embed_text(test_text)

    print(
        f"Model      : {EMBEDDING_MODEL}"
    )

    print(
        f"Dimensions : {len(embedding)}"
    )

    print(
        f"First 10   : {embedding[:10]}"
    )