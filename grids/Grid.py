from abc import ABC, abstractmethod


class Grid(ABC):

    @property
    @abstractmethod
    def size(self):
        pass

    @property
    @abstractmethod
    def directions(self):
        pass

    @abstractmethod
    def are_valid_coordinates(self, coordinates):
        """
        checks if given coordinates are valid for this grid
        :param coordinates: (float, float, float)
        :return: true = coordinates are valid, false = coordinates invalid
        """
        pass

    @abstractmethod
    def get_nearest_valid_coordinates(self, coordinates):
        """
        calculates the nearest valid coordinates to given coordinates
        :param coordinates: (float, float, float)
        :return: valid coordinates
        """
        pass

    def get_directions_dictionary(self):
        """
        returns a dictionary of the directions, with direction names (string) as keys
        and the direction vectors (3d tuple) as values
        :return: dictionary with  - 'string: (float, float,float)'
        """
        return self.directions

    def get_directions_list(self):
        """
        returns a list of the direction vectors
        :return: list of 3d tuples - '(float, float, float)'
        """
        return list(self.directions.values())

    def get_directions_names(self):
        """
        returns a list of direction names
        :return: list of strings
        """
        return list(self.directions.keys())

    def get_lines(self):
        """
        FOR VISUALIZATION!
        calculates line data in this grids directions for the visualization.
        output is a list of start and end points. the start point is always the center of this grid and the end points
        are the directions but only half in length
        :return: list of vectors, [(sx,sy,sz), (ex,ey,ez), (sx,sy,sz), (ea,eb,ec), ...]
        """
        lines = []
        for d in self.get_directions_list():
            lines.append(self.get_center())
            hd = (d[0] * 0.5, d[1] * 0.5, d[2] * 0.5)
            lines.append(hd)
        return lines

    @abstractmethod
    def get_box(self, width):
        """
        calculates all valid coordinates in a box
        :return: list of 3d coordinates: [(x_start_l0, y_start_l0), (x_end_l0, y_end_l0), (x_start_l1, y_start_l1), ...)
        """
        pass

    @abstractmethod
    def get_dimension_count(self):
        """
        returns the amount of dimensions
        :return: integer, amount of dimensions (3 or 2 presumably)
        """
        pass

    @abstractmethod
    def get_distance(self, start, end):
        """
        the metric or distance function for this grid
        :param start: coordinates, (float, float, float) tuple, start of path
        :param end: coordinates, (float, float, float) tuple, end of path
        :return: integer, minimal amount of steps between start and end
        """
        pass

    @staticmethod
    def get_coordinates_in_direction(position, direction):
        """
        calculates a new position from current position and direction
        :param position: coordinates, (float, float, float) tuple, current position
        :param direction: coordinates, (float, float, float) tuple, direction
        :return: coordinates, (float, float, float) tuple, new position
        """
        new_pos = []
        for i in range(len(position)):
            new_pos.append(position[i]+direction[i])
        return tuple(new_pos)

    def get_center(self):
        """
        returns the center of the grid. usually (0,0,0)
        :return: coordinates, (float, float, float) tuple
        """
        return 0.0, 0.0, 0.0

    def get_scaling(self):
        """
        returns the x,y,z scaling for the visualization. usually (1,1,1) = no scaling
        :return: x,y,z scaling values: float, float, float
        """
        return 1.0, 1.0, 1.0

    def get_adjacent_coordinates(self, coordinates):
        """
        calculates a set of adjacent coordinates of the given coordinates
        :param coordinates: the coordinates of which the neighboring coordinates should be calculated
        :return: a set of coordinates
        """
        n = set()
        for d in self.get_directions_list():
            n.add(self.get_coordinates_in_direction(coordinates, d))
        return n

    def _get_adjacent_coordinates_not_in_set(self, coordinates, not_in_set):
        """
        the same as 'get_neighboring_coordinates', but doesn't return coordinates which are in the given 'not_in_set'.
        :param coordinates: the coordinates of which the neighboring coordinates should be calculated
        :param not_in_set: set of coordinates, which should not be included in the result
        :return: a set of coordinates
        """
        result = set()
        for d in self.get_directions_list():
            n = self.get_coordinates_in_direction(coordinates, d)
            if n not in not_in_set:
                result.add(n)
        return result

    def get_n_sphere(self, coordinates, radius):
        """
        calculates the n-sphere of this grid
        :param coordinates: center of the circle/sphere
        :param radius: radius of the circle/sphere
        :return: set of coordinates
        """
        result = set()
        ns = self.get_adjacent_coordinates(coordinates)
        current_ns = ns
        result.update(ns)

        for i in range(radius):
            tmp = set()
            for n in current_ns:
                ns = self._get_adjacent_coordinates_not_in_set(n, result)
                tmp.update(ns)
                result.update(ns)
            current_ns = tmp

        return result

    def get_n_sphere_border(self, coordinates, radius):
        """
        calculates the border of an n-sphere around the center with the given radius
        :param coordinates: center of the ring
        :param radius: radius of the ring
        :return: set of coordinates
        """
        if radius == 0:
            r = set()
            r.add(coordinates)
            return r

        seen = set()
        ns = self.get_adjacent_coordinates(coordinates)
        current_ns = ns
        seen.update(ns)
        seen.add(coordinates)

        for i in range(radius-1):
            tmp = set()
            for n in current_ns:
                ns = self._get_adjacent_coordinates_not_in_set(n, seen)
                seen.update(ns)
                tmp.update(ns)
            current_ns = tmp

        return current_ns
