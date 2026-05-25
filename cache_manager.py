from __future__ import annotations
import json
import os
import tempfile
from typing import Optional

CACHE_PATH = "data/cache/location_cache.json"


class CacheManager:
    """
    Persistent JSON cache for place → (lat, lon) lookups.

    Keys are lower-cased and stripped so "Paris " and "paris" hit the same entry.
    Writes are atomic (write-to-temp → rename) to avoid cache corruption on crash.
    """

    def __init__(self, cache_path: str = CACHE_PATH) -> None:
        self.cache_path = cache_path
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        if not os.path.exists(cache_path):
            self._write({})

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, place: str) -> Optional[tuple[float, float]]:
        """Return cached coordinates or None if not cached."""
        entry = self._read().get(self._key(place))
        if entry is None:
            return None
        # Stored as a list in JSON; convert back to tuple.
        return tuple(entry)  # type: ignore[return-value]

    def set(self, place: str, coordinates: tuple[float, float]) -> None:
        """Persist coordinates for *place*."""
        cache = self._read()
        cache[self._key(place)] = list(coordinates)
        self._write(cache)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _key(place: str) -> str:
        return place.strip().lower()

    def _read(self) -> dict:
        try:
            with open(self.cache_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            # Corrupt or missing file — start fresh.
            return {}

    def _write(self, data: dict) -> None:
        dir_ = os.path.dirname(self.cache_path)
        # Atomic write: write to a temp file then rename.
        with tempfile.NamedTemporaryFile(
            "w", dir=dir_, delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(data, tmp, indent=4)
            tmp_path = tmp.name
        os.replace(tmp_path, self.cache_path)