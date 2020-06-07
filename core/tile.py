"""The tile module provides the interface for the tiles. A tile is a hexogon that can be taken or dropped
 and be connected to each other to buld up islands"""
from core import matter


class Tile(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, coordinates, color):
        """Initializing the marker constructor"""
        super().__init__(world, coordinates, color, matter_type="tile", mm_size=world.config_data.tile_mm_size)
        self.__isCarried = False

    def get_tile_status(self):
        """
        Get the tile status if it taken or not

        :return: Tiles status
        """
        return self.__isCarried

    def set_tile_status(self, status):
        """
        Sets the tiles status

        :param status: True: Has been taken; False: Is not taken
        :return:
        """
        self.__isCarried = status

    def take(self):
        """
        Takes the tile on the given coordinate if it is not taken

        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.__isCarried:
            if self.coordinates in self.world.tile_map_coordinates:
                del self.world.tile_map_coordinates[self.coordinates]
            self.__isCarried = True
            if self.world.vis is not None:
                self.world.vis.tile_changed(self)
            return True
        else:
            return False

    def drop_me(self, coordinates):
        """
        Drops the tile

        :param coordinates: the given position
        :return: None
        """
        self.coordinates = coordinates
        self.world.tile_map_coordinates[self.coordinates] = self
        self.__isCarried = False
        if self.world.vis is not None:
            self.world.vis.tile_changed(self)

    def set_color(self, color):
        super().set_color(color)
        if self.world.vis is not None:
            self.world.vis.tile_changed(self)
