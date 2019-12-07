"""The marker module provides the interface to the markers. A marker is any point on
 the coordinate system of the simulators world"""
from lib import matter


class Marker(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, coordinates, color):
        """Initializing the marker constructor"""
        super().__init__(world, coordinates, color, type="marker", mm_size=world.config_data.marker_mm_size)

    def set_color(self, color):
        super().set_color(color)
        self.world.vis.marker_changed(self)
