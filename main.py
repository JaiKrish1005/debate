from graph.workflow import run_debate


def main():
    claim = "Earth is a s sphere"

    result = run_debate(claim)

    print("\n=== CLAIM ===")
    print(result["claim"])

    print("\n=== EVIDENCE ===")
    for source in result["evidence"].sources:
        print(f"\nTitle: {source.title}")
        print(source.summary[:300])

    print("\n=== DEFENDER ===")
    print(result["defender_argument"])

    print("\n=== SKEPTIC ===")
    print(result["skeptic_argument"])

    print("\n=== VERDICT ===")
    print(result["verdict"])


if __name__ == "__main__":
    main()
