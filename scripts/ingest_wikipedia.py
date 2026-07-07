from pathlib import Path
import sys
import uuid

import requests

# Make project root importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from services.chroma import index_documents

TOPICS_FILE = PROJECT_ROOT / "data" / "wikipedia_topics.txt"

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "debAIte/1.0 (Local AI Claim Verification Project)"
}

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_topics() -> list[str]:
    """
    Load Wikipedia article titles from data/wikipedia_topics.txt.
    """
    with open(TOPICS_FILE, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def fetch_article(topic: str) -> str:
    """
    Fetch the full plain-text extract of a Wikipedia article.
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": topic,
        "explaintext": True,
        "redirects": 1,
    }

    response = requests.get(
        WIKIPEDIA_API,
        params=params,
        headers=HEADERS,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    return page.get("extract", "")


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Split text into overlapping character chunks.
    """
    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def ingest_topic(topic: str) -> int:
    """
    Fetch, chunk and index one Wikipedia article.
    """
    print(f"Indexing: {topic}")

    article = fetch_article(topic)

    if not article:
        print("  No content found.")
        return 0

    chunks = chunk_text(article)

    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        metadatas.append(
            {
                "topic": topic,
                "chunk": index,
                "source": "Wikipedia",
            }
        )

    index_documents(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    print(f"  Indexed {len(chunks)} chunks.")

    return len(chunks)


def main():
    topics = load_topics()

    total_chunks = 0

    print("=" * 50)
    print(f"Found {len(topics)} topics")
    print("=" * 50)

    for topic in topics:
        try:
            total_chunks += ingest_topic(topic)
        except Exception as exc:
            print(f"Failed to index '{topic}'")
            print(exc)
            print()

    print("\n" + "=" * 50)
    print("Ingestion Complete")
    print("=" * 50)
    print(f"Topics Indexed : {len(topics)}")
    print(f"Chunks Indexed : {total_chunks}")


if __name__ == "__main__":
    main()