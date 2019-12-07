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
    def is_valid_location(self, location):
        """
        checks if given location is a valid location for matter in this grid
        :param location: (float, float, float)
        :return: true = location is valid, false = location invalid
        """
        pass

    @abstractmethod
    def get_nearest_location(self, coordinates):
        """
        calculates the nearest location to given coordinates
        :param coordinates: (float, float, float)
        :return: valid location
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
        calculates locations in a box
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
        :param start: location, (float, float, float) tuple, start of path
        :param end: location, (float, float, float) tuple, end of path
        :return: integer, minimal amount of steps between start and end
        """
        pass

    @staticmethod
    def get_location_in_direction(position, direction):
        """
        calculates a new position from current position and direction
        :param position: location, (float, float, float) tuple, current position
        :param direction: location, (float, float, float) tuple, direction
        :return: location, (float, float, float) tuple, new position
        """
        new_pos = []
        for i in range(len(position)):
            new_pos.append(position[i]+direction[i])
        return tuple(new_pos)

    def get_center(self):
        """
        returns the center of the grid. usually (0,0,0)
        :return: location, (float, float, float) tuple
        """
        return 0.0, 0.0, 0.0

    def get_scaling(self):
        """
        returns the x,y,z scaling for the visualization. usually (1,1,1) = no scaling
        :return: x,y,z scaling values: float, float, float
        """
        return 1.0, 1.0, 1.0

    def get_adjacent_locations(self, location):
        """
        calculates a set of adjacent locations of the given location
        :param location: the location of which the neighboring locations should be calculated
        :return: a set of locations
        """
        n = set()
        for d in self.get_directions_list():
            n.add(self.get_location_in_direction(location, d))
        return n

    def _get_adjacent_locations_not_in_set(self, location, not_in_set):
        """
        the same as 'get_neighboring_locations', but doesn't return locations which are in the given 'not_in_set'.
        :param location: the location of which the neighboring locations should be calculated
        :param not_in_set: set of locations, which should not be included in the result
        :return: a set of locations
        """
        result = set()
        for d in self.get_directions_list():
            n = self.get_location_in_direction(location, d)
            if n not in not_in_set:
                result.add(n)
        return result

    def get_n_sphere(self, location, radius):
        """
        calculates the n-sphere of this grid
        :param location: center of the circle/sphere
        :param radius: radius of the circle/sphere
        :return: set of locations
        """
        result = set()
        ns = self.get_adjacent_locations(location)
        current_ns = ns
        result.update(ns)

        for i in range(radius):
            tmp = set()
            for n in current_ns:
                ns = self._get_adjacent_locations_not_in_set(n, result)
                tmp.update(ns)
                result.update(ns)
            current_ns = tmp

        return result

    def get_n_sphere_border(self, location, radius):
        """
        calculates the border of an n-sphere around the center with the given radius
        :param location: center of the ring
        :param radius: radius of the ring
        :return: set of locations
        """
        if radius == 0:
            r = set()
            r.add(location)
            return r

        seen = set()
        ns = self.get_adjacent_locations(location)
        current_ns = ns
        seen.update(ns)
        seen.add(location)

        for i in range(radius-1):
            tmp = set()
            for n in current_ns:
                ns = self._get_adjacent_locations_not_in_set(n, seen)
                seen.update(ns)
                tmp.update(ns)
            current_ns = tmp

        return current_ns
