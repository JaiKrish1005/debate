from services.chroma import retrieve


def main():
    test_queries = [
        "Vitamin C prevents colds",
        "The Earth is flat",
        "Climate change is caused by humans",
        "Coffee is healthy",
        "Artificial intelligence",
    ]

    for query in test_queries:
        print("=" * 80)
        print(f"Query: {query}")
        print("=" * 80)

        results = retrieve(query)

        if not results:
            print("No results found.\n")
            continue

        for i, result in enumerate(results, start=1):
            print(f"\nResult {i}")
            print("-" * 80)
            print(f"Topic : {result['metadata']['topic']}")
            print(f"Chunk : {result['metadata']['chunk']}")
            print()
            print(result["document"])

        print("\n")


if __name__ == "__main__":
    main()