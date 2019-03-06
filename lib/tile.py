"""The tile module provides the interface for the tiles. A tile is a hexogon that can be taken or dropped
 and be connected to each other to buld up islands"""
import logging
from lib import matter


black = 1
gray = 2
red = 3
green = 4
blue = 5

read=0
write=1


class Tile(matter.matter):
    """In the classe location all the methods for the characterstic of a location is included"""

    def __init__(self, sim, x, y, color=gray, alpha=1, mm_limit=0, mm_size=0):
        """Initializing the location constructor"""
        super().__init__( sim, x, y, color, alpha=1,  type="tile", mm_limit=mm_limit, mm_size=mm_size)
        self.__isCarried = False
        self.created = False


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


    def take(self, coords=0):
        """
        Takes the tile on the given coordinate if it is not taken

        :param coords: Coordination of tile that should be taken
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """
        if coords==0:
            if self.__isCarried == False:
                if self.coords in self.sim.tile_map:
                    del self.sim.tile_map_coords[self.coords]
                self.__isCarried = True
                self.touch()
                return True
            else:
                return False
        else:
            if self.__isCarried == False:
                if self.coords in self.sim.tile_map_coords:
                    del self.sim.tile_map_coords[self.coords]
                self.__isCarried = True
                self.coords = coords
                self.touch()
                return True
            else:
                return False



    def drop_me(self, coords):
        """
        Drops the tile

        :param coords: the given position
        :return: None
        """
        self.sim.tile_map_coords[coords] = self
        self.coords = coords
        self.__isCarried = False
        self.touch()

    def update_tile_coords(self, tile, new_coords):
        """
        Upadtes the tiles new coordinates

        :param tile:
        :param new_coords: new coorindation points
        :return: None
        """
        tile.coords = new_coords
        self.tile_map_coords[tile.coords] = tile

    def touch(self):
        """Tells the visualization that something has been modified and that it shoud changed it"""
        self.modified = True

