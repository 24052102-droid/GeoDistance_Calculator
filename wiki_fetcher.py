from __future__ import annotations
import json
import time
import requests

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "WikiGeoDistanceEngine/1.0 (Python)"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


class WikiFetcher:

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def get_page(self, place: str) -> dict:
        """
        Fetch Wikipedia coordinates for *place*.

        Raises RuntimeError if all retries are exhausted.
        """
        params = {
            "action": "query",
            "prop": "coordinates",
            "titles": place,
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        }

        last_error: Exception = RuntimeError("Unknown error")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.get(
                    WIKI_API_URL, params=params, timeout=10
                )
                response.raise_for_status()

                text = response.text.strip()
                if not text:
                    raise ValueError("Empty response from Wikipedia API")

                return json.loads(text)

            except (json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                print(f"[WikiFetcher] Invalid response (attempt {attempt}/{MAX_RETRIES}): {exc}")

            except requests.RequestException as exc:
                last_error = exc
                print(f"[WikiFetcher] Network error (attempt {attempt}/{MAX_RETRIES}): {exc}")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        raise RuntimeError(
            f"Could not fetch data for '{place}' after {MAX_RETRIES} attempts: {last_error}"
        )

    def __del__(self) -> None:
        # Close the underlying TCP connection pool gracefully.
        try:
            self.session.close()
        except Exception:
            pass