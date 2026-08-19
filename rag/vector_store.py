"""
rag/vector_store.py

Stores HAI-SOC knowledge-base embeddings in Qdrant.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from rag.chunking import chunk_documents
from rag.embeddings import embed_chunks
from rag.loaders import load_knowledge_base


# --------------------------------------------------
# Configuration
# --------------------------------------------------

QDRANT_URL = "http://localhost:6333"

VECTOR_SIZE = 768

DISTANCE = Distance.COSINE


COLLECTIONS = {
    "HIPAA": "hipaa_safeguards",
    "NIST": "nist_controls",
    "MITRE": "mitre_attack",
    "RUNBOOK": "incident_runbooks",
}


# --------------------------------------------------
# Qdrant Client
# --------------------------------------------------

def create_client():
    """
    Create a connection to the local Qdrant instance.
    """

    return QdrantClient(
        url=QDRANT_URL
    )


# --------------------------------------------------
# Collection Management
# --------------------------------------------------

def create_collection(
    client: QdrantClient,
    collection_name: str,
):
    """
    Create a Qdrant collection if it does not exist.
    """

    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if collection_name in existing_collections:

        print(
            f"Collection already exists: "
            f"{collection_name}"
        )

        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=DISTANCE,
        ),
    )

    print(
        f"Created collection: "
        f"{collection_name}"
    )


# --------------------------------------------------
# Insert Chunks
# --------------------------------------------------

def insert_chunks(
    client: QdrantClient,
    collection_name: str,
    chunks: list[dict],
):
    """
    Insert embedded chunks into Qdrant.
    """

    points = []

    for index, chunk in enumerate(chunks):

        point = PointStruct(
            id=index,
            vector=chunk["embedding"],
            payload={
                "text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "document_id": chunk["document_id"],
                "category": chunk["category"],
                "title": chunk["title"],
                "source": chunk["source"],
                "citation": chunk["citation"],
                "tags": chunk["tags"],
            },
        )

        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points,
    )

    print(
        f"Inserted {len(points)} chunks "
        f"into {collection_name}"
    )


# --------------------------------------------------
# Build Vector Store
# --------------------------------------------------

def build_vector_store():

    print("Loading knowledge base...")

    documents = load_knowledge_base()

    print(
        f"Loaded {len(documents)} documents"
    )

    print("\nChunking documents...")

    chunks = chunk_documents(
        documents
    )

    print(
        f"Generated {len(chunks)} chunks"
    )

    print("\nGenerating embeddings...")

    embedded_chunks = embed_chunks(
        chunks
    )

    print(
        f"Generated {len(embedded_chunks)} embeddings"
    )

    client = create_client()

    print(
        f"\nConnected to Qdrant: {QDRANT_URL}"
    )

    # ----------------------------------------------
    # Group chunks by category
    # ----------------------------------------------

    grouped_chunks = {}

    for chunk in embedded_chunks:

        category = chunk["category"]

        grouped_chunks.setdefault(
            category,
            [],
        ).append(chunk)

    # ----------------------------------------------
    # Create collections and insert vectors
    # ----------------------------------------------

    for category, collection_name in COLLECTIONS.items():

        category_chunks = grouped_chunks.get(
            category,
            [],
        )

        if not category_chunks:

            print(
                f"No chunks found for "
                f"{category}"
            )

            continue

        create_collection(
            client,
            collection_name,
        )

        insert_chunks(
            client,
            collection_name,
            category_chunks,
        )

    print("\nVector store build completed.")


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    build_vector_store()