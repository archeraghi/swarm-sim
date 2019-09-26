"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators world"""
from lib import matter
from lib.swarm_sim_header import *


class Marker(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, x, y, color=black, transparency=1):
        """Initializing the marker constructor"""
        super().__init__( world, (x, y), color, transparency, type="marker", mm_size=world.config_data.marker_mm_size)


