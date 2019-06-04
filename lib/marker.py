"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators sim"""


from lib import matter

black = 1
gray = 2
red = 3
green = 4
blue = 5

class marker(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""

    def __init__(self, sim, x, y, color=black, alpha=1, mm_limit=0, mm_size=0):
        """Initializing the marker constructor"""
        super().__init__( sim, x, y, color, alpha, type="marker", mm_limit=mm_limit, mm_size=mm_size)


