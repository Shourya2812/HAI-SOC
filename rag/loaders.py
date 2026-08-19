"""
backend/rag/loaders.py

Loads HAI-SOC knowledge-base Markdown documents
and extracts YAML frontmatter + Markdown content.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"


# --------------------------------------------------
# RAG Document Model
# --------------------------------------------------

class RAGDocument(BaseModel):
    """
    Represents one knowledge-base document.

    Frontmatter metadata is preserved so that it can
    later be attached to every vector stored in Qdrant.
    """

    document_id: str

    category: str

    title: str

    source: str

    citation: str

    tags: list[str] = Field(default_factory=list)

    content: str

    source_path: str

    metadata: dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------
# Frontmatter Parsing
# --------------------------------------------------

def parse_markdown_file(path: Path) -> RAGDocument:
    """
    Parse one Markdown file.

    Expected structure:

    ---
    document_id: ...
    category: ...
    title: ...
    ---
    
    Markdown content...
    """

    text = path.read_text(
        encoding="utf-8"
    )

    if not text.startswith("---"):
        raise ValueError(
            f"Missing YAML frontmatter: {path}"
        )

    parts = text.split(
        "---",
        2
    )

    if len(parts) != 3:
        raise ValueError(
            f"Invalid frontmatter format: {path}"
        )

    frontmatter_text = parts[1].strip()

    content = parts[2].strip()

    metadata = yaml.safe_load(
        frontmatter_text
    )

    if not isinstance(metadata, dict):
        raise ValueError(
            f"Invalid YAML frontmatter: {path}"
        )

    # Required metadata validation

    required_fields = [
        "document_id",
        "category",
        "title",
        "source",
        "citation",
    ]

    for field in required_fields:

        if not metadata.get(field):

            raise ValueError(
                f"Missing '{field}' in {path}"
            )

    if not content:
        raise ValueError(
            f"Empty document content: {path}"
        )

    # Preserve complete frontmatter

    document_metadata = dict(
        metadata
    )

    return RAGDocument(
        document_id=metadata["document_id"],
        category=metadata["category"],
        title=metadata["title"],
        source=metadata["source"],
        citation=metadata["citation"],
        tags=metadata.get("tags", []),
        content=content,
        source_path=str(path),
        metadata=document_metadata,
    )


# --------------------------------------------------
# Knowledge Base Loader
# --------------------------------------------------

def load_knowledge_base() -> list[RAGDocument]:
    """
    Recursively load all Markdown documents
    from knowledge_base/.
    """

    if not KNOWLEDGE_BASE_DIR.exists():

        raise FileNotFoundError(
            f"Knowledge base not found: "
            f"{KNOWLEDGE_BASE_DIR}"
        )

    files = sorted(
        KNOWLEDGE_BASE_DIR.rglob("*.md")
    )

    documents: list[RAGDocument] = []

    document_ids: set[str] = set()

    for path in files:

        document = parse_markdown_file(
            path
        )

        # Prevent duplicate document IDs

        if document.document_id in document_ids:

            raise ValueError(
                "Duplicate document_id found: "
                f"{document.document_id}"
            )

        document_ids.add(
            document.document_id
        )

        documents.append(
            document
        )

    return documents


# --------------------------------------------------
# Manual Test
# --------------------------------------------------

if __name__ == "__main__":

    documents = load_knowledge_base()

    print(
        f"Loaded {len(documents)} "
        f"knowledge documents\n"
    )

    for document in documents:

        print(
            f"{document.category:8} | "
            f"{document.document_id:40} | "
            f"{document.title} | "
            f"{len(document.content)} chars"
        )