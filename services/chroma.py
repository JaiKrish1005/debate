from pathlib import Path
import os

import chromadb
from chromadb.api.models.Collection import Collection
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "wikipedia"
TOP_K = 5

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

if not EMBEDDING_MODEL:
    raise ValueError("EMBEDDING_MODEL is not set in the .env file.")

# -----------------------------------------------------------------------------
# Clients
# -----------------------------------------------------------------------------

chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

ollama_client = Client()

# -----------------------------------------------------------------------------
# Collection
# -----------------------------------------------------------------------------


def create_collection() -> Collection:
    """
    Create the Chroma collection if it doesn't exist,
    otherwise return the existing collection.
    """
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Wikipedia knowledge base"},
    )


# -----------------------------------------------------------------------------
# Embeddings
# -----------------------------------------------------------------------------


def _embed(text: str) -> list[float]:
    """
    Generate an embedding for a single piece of text using Ollama.
    """
    response = ollama_client.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.embeddings[0]


# -----------------------------------------------------------------------------
# Indexing
# -----------------------------------------------------------------------------


def index_documents(
    ids: list[str],
    documents: list[str],
    metadatas: list[dict] | None = None,
) -> None:
    """
    Index documents into ChromaDB.

    Args:
        ids:
            Unique document IDs.

        documents:
            Document text.

        metadatas:
            Optional metadata for each document.
    """
    if len(ids) != len(documents):
        raise ValueError("ids and documents must have the same length.")

    if metadatas is not None and len(metadatas) != len(documents):
        raise ValueError("metadatas must match documents length.")

    collection = create_collection()

    embeddings = []

    for document in documents:
        embeddings.append(_embed(document))

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


# -----------------------------------------------------------------------------
# Retrieval
# -----------------------------------------------------------------------------


def retrieve(
    query: str,
    top_k: int = TOP_K,
) -> list[str]:
    """
    Retrieve the most relevant document chunks.

    Returns:
        A list of retrieved document strings.
    """
    collection = create_collection()

    query_embedding = _embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [])

    if not documents:
        return []

    return documents[0]
