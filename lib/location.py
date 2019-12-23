"""The location module provides the interface to the locations. A location is any point on
 the coordinate system of the simulators world"""
from lib import matter


class Location(matter.Matter):
    """In the class matter all the methods for the characterstic of a location is included"""
    def __init__(self, world, coordinates, color):
        """Initializing the location constructor"""
        super().__init__(world, coordinates, color, type="location", mm_size=world.config_data.location_mm_size)

    def set_color(self, color):
        super().set_color(color)
        if self.world.vis is not None:
            self.world.vis.location_changed(self)
