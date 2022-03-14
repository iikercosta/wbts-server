from typing import List

from app.models import Location


def get_locations() -> List[str]:
    locations = Location.query.all()

    return [location.alias for location in locations]
