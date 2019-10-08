"""The tile module provides the interface for the tiles. A tile is a hexogon that can be taken or dropped
 and be connected to each other to buld up islands"""
from lib import matter
from lib.swarm_sim_header import *


class Tile(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, coordinates, color=gray, transparency=1):
        """Initializing the marker constructor"""
        super().__init__( world, coordinates, color, transparency,  type="tile", mm_size=world.config_data.tile_mm_size)
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

    def take(self, coordinates=0):
        """
        Takes the tile on the given coordinate if it is not taken

        :param coordinates: Coordination of tile that should be taken
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """
        if coordinates==0:
            if self.__isCarried == False:
                if self.coordinates in self.world.tile_map:
                    del self.world.tile_map_coordinates[self.coordinates]
                self.__isCarried = True
                self.set_transparency(0.5)
                self.touch()
                return True
            else:
                return False
        else:
            if self.__isCarried == False:
                if self.coordinates in self.world.tile_map_coordinates:
                    del self.world.tile_map_coordinates[self.coordinates]
                self.__isCarried = True
                self.coordinates = coordinates
                self.set_transparency(0.5)
                self.touch()
                return True
            else:
                return False

    def drop_me(self, coordinates):
        """
        Drops the tile

        :param coordinates: the given position
        :return: None
        """
        self.world.tile_map_coordinates[coordinates] = self
        self.coordinates = coordinates
        self.__isCarried = False
        self.set_transparency(1)
        self.touch()

    def touch(self):
        """Tells the visualization that something has been modified and that it shoud changed it"""
        self.modified = True

