from src.distance.haversine import Haversine


class DistanceEngine:

    def calculate(
        self,
        coord1: tuple[float, float],
        coord2: tuple[float, float],
    ) -> float:
        """Calculate haversine distance between two (lat, lon) tuples."""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        return Haversine.calculate(lat1, lon1, lat2, lon2)