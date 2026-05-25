class Validator:

    @staticmethod
    def validate(lat: float, lon: float) -> bool:
        """Return True only when lat/lon are within legal geographic bounds."""
        return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0