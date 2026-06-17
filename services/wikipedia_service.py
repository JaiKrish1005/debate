import requests


BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"


def get_summary(title: str):
    try:
        response = requests.get(
            f"{BASE_URL}/{title}",
            timeout=10,
            headers={
                "User-Agent": "debAIte/0.1"
            }
        )

        response.raise_for_status()

        data = response.json()

        return {
            "title": data.get("title", title),
            "summary": data.get("extract", "")
        }

    except Exception as e:
        print(f"ERROR for {title}: {e}")
        return None