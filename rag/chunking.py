"""
rag/chunking.py

Splits loaded HAI-SOC knowledge-base documents into
retrieval-friendly chunks while preserving metadata.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loaders import load_knowledge_base


# --------------------------------------------------
# Chunking Configuration
# --------------------------------------------------

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# --------------------------------------------------
# Text Splitter
# --------------------------------------------------

def create_text_splitter():
    """
    Create a recursive text splitter.

    The splitter tries to preserve natural boundaries
    such as headings, paragraphs, and sentences.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
        ],
    )


# --------------------------------------------------
# Chunk Knowledge Base
# --------------------------------------------------

def chunk_documents(documents):
    """
    Convert loaded knowledge documents into smaller
    retrieval-friendly chunks.

    Each chunk preserves the original document metadata.
    """

    splitter = create_text_splitter()

    chunks = []

    for document in documents:

        split_texts = splitter.split_text(
            document.content
        )

        for index, text in enumerate(split_texts):

            chunk = {
                "text": text,
                "chunk_index": index,
                "document_id": document.document_id,
                "category": document.category,
                "title": document.title,
                "source": document.source,
                "citation": document.citation,
                "tags": document.tags,
            }

            chunks.append(chunk)

    return chunks


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    documents = load_knowledge_base()

    chunks = chunk_documents(documents)

    print(
        f"\nLoaded documents : {len(documents)}"
    )

    print(
        f"Generated chunks : {len(chunks)}"
    )

    print("\nChunk distribution:")

    distribution = {}

    for chunk in chunks:

        category = chunk["category"]

        distribution[category] = (
            distribution.get(category, 0) + 1
        )

    for category, count in sorted(
        distribution.items()
    ):
        print(
            f"  {category:<10} | {count}"
        )

    print("\nSample chunks:\n")

    for chunk in chunks[:5]:

        print("-" * 70)

        print(
            f"Category : {chunk['category']}"
        )

        print(
            f"Document : {chunk['document_id']}"
        )

        print(
            f"Chunk    : {chunk['chunk_index']}"
        )

        print(
            f"Length   : {len(chunk['text'])} chars"
        )

        print(
            f"Text     : {chunk['text'][:300]}..."
        )