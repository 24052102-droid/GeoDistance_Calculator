from __future__ import annotations
from typing import Optional


class CoordinateExtractor:

    def extract(self, data: dict) -> Optional[tuple[float, float]]:
        """
        Extract (latitude, longitude) from a Wikipedia API response.

        Returns None if coordinates are absent or the response is malformed.
        """
        try:
            pages = data["query"]["pages"]

            if not pages:
                return None

            page = pages[0]

            coords = page.get("coordinates")
            if not coords:
                return None

            return float(coords[0]["lat"]), float(coords[0]["lon"])

        except (KeyError, IndexError, TypeError, ValueError):
            return None