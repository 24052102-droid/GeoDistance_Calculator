from __future__ import annotations
import os
import sys
import webbrowser

from src.extraction.wiki_fetcher import WikiFetcher
from src.extraction.coordinate_extractor import CoordinateExtractor
from src.preprocessing.validation import Validator
from src.distance.distance_engine import DistanceEngine
from src.visualization.map_plotter import MapPlotter
from src.utils.cache_manager import CacheManager

# Shared instances — created once and reused for both lookups.
_cache = CacheManager()
_fetcher = WikiFetcher()
_extractor = CoordinateExtractor()


def get_coordinates(place: str) -> tuple[float, float]:
    """
    Return (latitude, longitude) for *place*.

    Hits the local cache first; falls back to the Wikipedia API.
    Raises RuntimeError with a descriptive message on any failure.
    """
    cached = _cache.get(place)
    if cached:
        print(f"  [cache] {place}")
        return cached

    print(f"  [wiki]  {place}")
    data = _fetcher.get_page(place)
    coords = _extractor.extract(data)

    if coords is None:
        raise RuntimeError(
            f"No coordinates found for '{place}'. "
            "Check the spelling or try the full Wikipedia article title."
        )

    lat, lon = coords
    if not Validator.validate(lat, lon):
        raise RuntimeError(
            f"Coordinates for '{place}' are out of valid range: ({lat}, {lon})"
        )

    _cache.set(place, coords)
    return coords


def main() -> None:
    print("=== Geographic Distance Calculator ===\n")

    place1 = input("Enter first place:  ").strip()
    place2 = input("Enter second place: ").strip()

    if not place1 or not place2:
        print("\nERROR: Place names cannot be empty.")
        sys.exit(1)

    print("\nFetching coordinates…")

    try:
        coord1 = get_coordinates(place1)
        coord2 = get_coordinates(place2)
    except RuntimeError as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)

    distance = DistanceEngine().calculate(coord1, coord2)

    print("\n" + "─" * 40)
    print("RESULTS")
    print("─" * 40)
    print(f"  {place1:<25} {coord1[0]:.5f}, {coord1[1]:.5f}")
    print(f"  {place2:<25} {coord2[0]:.5f}, {coord2[1]:.5f}")
    print(f"\n  Distance: {distance:,.2f} km")
    print("─" * 40)

    abs_path = MapPlotter.generate_map(place1, place2, coord1, coord2, distance)
    print(f"\nMap saved → {abs_path}")

    try:
        webbrowser.open(f"file://{abs_path}")
    except Exception:
        pass  # Non-critical — silently skip if no browser available.


if __name__ == "__main__":
    main()