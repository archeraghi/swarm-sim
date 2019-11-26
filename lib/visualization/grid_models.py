from abc import ABC, abstractmethod

vertex_shader_path = "lib/visualization/shader/gridVertexShader.glsl"
fragment_shader_path = "lib/visualization/shader/gridFragmentShader.glsl"


class Grid(ABC):

    @abstractmethod
    def is_valid_location(self, location):
        """
        checks if given location is a valid location for matter in this grid
        :param location: (float, float, float)
        :return: true = location is valid, false = location invalid
        """
        pass

    @abstractmethod
    def get_directions_dictionary(self):
        """
        returns a python dictonary with all directions this grid has
        :return: dictionary: "direction name" : (float, float, float) ...
        """
        pass

    @abstractmethod
    def get_lines(self):
        """
        calculates or loads line data for visualization, as a list of 3d coordinates
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
    def get_position_in_direction(position, direction):
        """
        calculates a new position from current position and direction
        :param position: location, (float, float, float) tuple, current position
        :param direction: location, (float, float, float) tuple, direction
        :return: location, (float, float, float) tuple, new position
        """
        return position[0]+direction[0], position[1]+direction[1], position[2]+direction[2]

    @abstractmethod
    def get_center(self):
        """
        returns the mathematical center of the grid. usually (0,0,0)
        :return: location, (float, float, float) tuple
        """
        pass

    def get_centered_ring(self, hops_radius):
        return self.get_centered_ring_recursive(self.get_center(), hops_radius)

    def get_centered_circle(self, hops_radius):
        return self.get_centered_circle_recursive(self.get_center(), hops_radius)

    def get_centered_ring_recursive(self, current, hops_radius=1):
        dirs = self.get_directions_dictionary().values()
        mydist = self.get_distance(current, self.get_center())
        if mydist == hops_radius:
            return [current]
        o = []
        for d in dirs:
            p = self.get_position_in_direction(current, d)
            if hops_radius >= self.get_distance(self.get_center(), p) > mydist:
                r = self.get_centered_ring_recursive(p, hops_radius)
                for i in r:
                    if i not in o:
                        o += [i]
        return o

    def get_centered_circle_recursive(self, current, hops_radius=1):
        dirs = self.get_directions_dictionary().values()
        mydist = self.get_distance(current, self.get_center())
        o = []
        if mydist <= hops_radius:
            o += [current]
        else:
            return []
        for d in dirs:
            p = self.get_position_in_direction(current, d)
            if hops_radius >= self.get_distance(self.get_center(), p) > mydist:
                r = self.get_centered_circle_recursive(p, hops_radius)
                for i in r:
                    if i not in o:
                        o += [i]
        return o

    def get_ring(self, center, hops_radius):
        cr = self.get_centered_ring(hops_radius)
        if center != self.get_center():
            for i in range(len(cr)):
                cr[i] = self.get_position_in_direction(cr[i], center)
        return cr

    def scan_circle_in_list(self, matter_list, center, hops_radius):
        output = []
        for m in matter_list:
            if self.get_distance(center, m.coordinates) <= hops_radius:
                output += [m]
        return output

    def get_circle(self, center, hops_radius):
        cc = self.get_centered_circle(hops_radius)
        if center != self.get_center():
            for i in range(len(cc)):
                cc[i] = self.get_position_in_direction(cc[i], center)
        return cc


class CubicGrid(Grid):

    directions = {
        "LEFT":     (-1, 0, 0),
        "RIGHT":    (1, 0, 0),
        "UP":       (0, 1, 0),
        "DOWN":     (0, -1, 0),
        "FORWARD":  (0, 0, 1),
        "BACK":     (0, 0, -1),
    }

    def __init__(self, size):
        super().__init__()
        self.size = size

    def get_lines(self):
        vertices = []

        for x in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                vertices.append(tuple([float(x), float(y), float(-self.size)]))
                vertices.append(tuple([float(x), float(y), float(self.size)]))

        for x in range(-self.size, self.size+1):
            for z in range(-self.size, self.size+1):
                vertices.append(tuple([float(x), float(-self.size), float(z)]))
                vertices.append(tuple([float(x),  float(self.size), float(z)]))

        for z in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                vertices.append(tuple([float(-self.size), float(y), float(z)]))
                vertices.append(tuple([float(self.size),  float(y), float(z)]))

        return vertices

    def is_valid_location(self, location):
        if location[0] % 1 == 0 and location[1] % 1 == 0 and location[2] % 1 == 0:
            return True
        else:
            return False

    def get_directions_dictionary(self):
        return self.directions

    def get_dimension_count(self):
        return 3

    def get_distance(self, start, end):
        return abs(start[0]-end[0])+abs(start[1]-end[1])+abs(start[2]-end[2])

    def get_center(self):
        return 0, 0, 0


class HexagonalGrid(Grid):

    directions = {
        "NE":  (0.5,   1, 0),
        "E":   (1,     0, 0),
        "SE":  (0.5,  -1, 0),
        "SW":  (-0.5, -1, 0),
        "W":   (-1,    0, 0),
        "NW":  (-0.5,  1, 0),
    }

    def __init__(self, size):
        super().__init__()
        self.size = size

    def get_lines(self):
        vertices = []

        # horizontal lines
        for y in range(-self.size, self.size+1):
            vertices.append(tuple([float(-self.size), float(y), 0.0]))
            vertices.append(tuple([float(self.size),  float(y), 0.0]))

        # diagonal lines from bottom-left to top-right
        for x in range(-self.size, self.size):
            vertices.append(tuple([float(x), float(-self.size), 0.0]))
            if x > 0:
                vertices.append(tuple([float(x)+self.size-x, float(self.size)-x*2,  0.0]))
            else:
                vertices.append(tuple([float(x)+self.size, float(self.size),  0.0]))
        for y in range(-self.size, self.size, 2):
            vertices.append(tuple([float(-self.size), y, 0.0]))
            vertices.append(tuple([-float(y+self.size)/2.0, float(self.size), 0.0]))

        # diagonal lines from bottom-right to top-left
        for x in range(-self.size, self.size + 1):
            vertices.append(tuple([float(x), float(-self.size), 0.0]))
            if x > 0:
                vertices.append(tuple([float(x)-self.size, float(self.size), 0.0]))
            else:
                vertices.append(tuple([float(x)-self.size-x, float(self.size)+2*x, 0.0]))
        for y in range(-self.size, self.size, 2):
            vertices.append(tuple([float(self.size), y, 0.0]))
            vertices.append(tuple([float(y+self.size)/2.0, float(self.size), 0.0]))

        return vertices

    def is_valid_location(self, location):
        if not location[2] == 0.0:
            print(3)
            return False
        if location[1] % 2.0 == 0.0:
            if location[0] % 1.0 == 0.0:
                return True
            else:
                print(1)
                return False
        else:
            if location[0] % 1.0 == 0.5:
                return True
            else:
                print(2)
                return False

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

