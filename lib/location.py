"""The location module provides the interface to the locations. A location is any point on
 the coordinate system of the simulators sim"""

from lib import matter

black = 1
gray = 2
red = 3
green = 4
blue = 5


class Location(matter.Matter):
    """In the classe location all the methods for the characterstic of a location is included"""

    def __init__(self, sim, x, y, color=black, alpha=1, mm_limit=0, mm_size=0):
        """Initializing the location constructor"""
        super().__init__(sim, x, y, color, alpha, type="location", mm_limit=mm_limit, mm_size=mm_size)
