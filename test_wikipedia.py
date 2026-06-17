# test_wikipedia.py

from services.wikipedia_service import search_claim

results = search_claim("Coffee causes dehydration")

for item in results:
    print("\n")
    print(item["title"])
    print("-" * 40)
    print(item["summary"])