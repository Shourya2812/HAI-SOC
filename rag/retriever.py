"""
rag/retriever.py

Retrieves relevant healthcare security knowledge from Qdrant.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import models

from rag.embeddings import embed_text


QDRANT_URL = "http://localhost:6333"

COLLECTIONS = [
    "hipaa_safeguards",
    "nist_controls",
    "mitre_attack",
    "incident_runbooks",
]


def create_qdrant_client():
    """
    Create a connection to the local Qdrant server.
    """

    return QdrantClient(url=QDRANT_URL)


def search_collection(
    client: QdrantClient,
    collection_name: str,
    query_vector: list[float],
    limit: int = 3,
):
    """
    Search one Qdrant collection for the most relevant chunks.
    """

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True,
    ).points

    return results


def retrieve_knowledge(
    query: str,
    results_per_collection: int = 3,
):
    """
    Retrieve relevant knowledge from all HAI-SOC
    knowledge-base collections.
    """

    client = create_qdrant_client()

    query_vector = embed_text(query)

    retrieved = []

    for collection in COLLECTIONS:

        results = search_collection(
            client=client,
            collection_name=collection,
            query_vector=query_vector,
            limit=results_per_collection,
        )

        for result in results:

            payload = result.payload or {}

            retrieved.append(
                {
                    "collection": collection,
                    "score": result.score,
                    "document_id": payload.get("document_id"),
                    "title": payload.get("title"),
                    "category": payload.get("category"),
                    "text": payload.get("text"),
                    "metadata": payload,
                }
            )

    retrieved.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return retrieved


def print_results(results):
    """
    Display retrieved knowledge in a readable format.
    """

    print(f"\nRetrieved {len(results)} results\n")

    for index, result in enumerate(results, start=1):

        print("=" * 80)

        print(f"Result       : {index}")
        print(f"Collection   : {result['collection']}")
        print(f"Score        : {result['score']:.4f}")
        print(f"Category     : {result['category']}")
        print(f"Document     : {result['document_id']}")
        print(f"Title        : {result['title']}")

        print("\nText:")
        print(result["text"][:1000])

    print("=" * 80)


if __name__ == "__main__":

    query = (
        "A PACS user exported patient data during an unusual hour "
        "after multiple failed attempts. Investigate possible "
        "unauthorized PHI exfiltration."
    )

    print("Connecting to Qdrant...")
    print(f"Query: {query}")

    results = retrieve_knowledge(query)

    print_results(results)