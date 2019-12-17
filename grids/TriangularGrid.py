import math

from grids.Grid import Grid


class TriangularGrid(Grid):

    def __init__(self, size):
        super().__init__()
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def directions(self):
        return {"NE":  (0.5,   1, 0),
                "E":   (1,     0, 0),
                "SE":  (0.5,  -1, 0),
                "SW":  (-0.5, -1, 0),
                "W":   (-1,    0, 0),
                "NW":  (-0.5,  1, 0)}

    def get_box(self, width):
        locs = []
        for y in range(-int(width/2),int(width/2)):
            for x in range(-int(width / 2), int(width / 2)):
                if y % 2 == 0:
                    locs.append((x, y, 0.0))
                else:
                    locs.append((x+0.5, y, 0.0))

        return locs

    def are_valid_coordinates(self, coordinates):
        if not coordinates[2] == 0.0:
            return False
        if coordinates[1] % 2.0 == 0.0:
            if coordinates[0] % 1.0 == 0.0:
                return True
        else:
            if coordinates[0] % 1.0 == 0.5:
                return True
        return False

    def get_nearest_valid_coordinates(self, coordinates):
        nearest_y = round(coordinates[1])
        if nearest_y % 2 == 0:
            nearest_x = round(coordinates[0])
        else:
            if coordinates[0] < 0:
                nearest_x = int(coordinates[0]) - 0.5
            else:
                nearest_x = int(coordinates[0]) + 0.5

        return nearest_x, nearest_y, 0

    def get_directions_dictionary(self):
        return self.directions

    def get_dimension_count(self):
        return 2

    def get_distance(self, start, end):
        dx = abs(start[0]-end[0])
        dy = abs(start[1]-end[1])
        if dx*2 >= dy:
            return (dx*2+dy)/2
        else:
            return dy

    def get_center(self):
        return 0, 0, 0

    def get_scaling(self):
        return 1.0, math.sqrt(3/4), 1.0
