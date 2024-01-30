"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators sim"""


from lib import matter

black = 1
gray = 2
red = 3
green = 4
blue = 5

class Marker(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""

    def __init__(self, sim, x, y, color=black, alpha=1):
        """Initializing the marker constructor"""
        super().__init__( sim, (x, y), color, alpha, type="marker", mm_size=sim.config_data.marker_mm_size)


