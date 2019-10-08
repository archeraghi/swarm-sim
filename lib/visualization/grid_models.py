from vispy.gloo import VertexBuffer, IndexBuffer
from lib.visualization.models import Model
from abc import ABC, abstractmethod
import numpy as np

vertex_shader_path = "lib/visualization/shader/gridVertexShader.glsl"
fragment_shader_path = "lib/visualization/shader/gridFragmentShader.glsl"


class Grid(Model, ABC):

    def __init__(self, size):
        super().__init__(vertex_shader_path, fragment_shader_path)
        self.size = size
        self['view'] = np.eye(4, dtype=np.float32)
        self['model'] = np.eye(4, dtype=np.float32)
        self['projection'] = np.eye(4, dtype=np.float32)
        self['color'] = (1, 1, 1, 0.5)

    @abstractmethod
    def is_valid_location(self, location):
        pass

    @abstractmethod
    def get_directions_dictionary(self):
        pass

    @abstractmethod
    def get_dimension_count(self):
        pass


class CubicGrid(Grid):

    directions = {
        "LEFT":     (-1, 0, 0),
        "EAST":     (-1, 0, 0),
        "RIGHT":    (1, 0, 0),
        "UP":       (0, 1, 0),
        "DOWN":     (0, -1, 0),
        "FORWARD":  (0, 0, 1),
        "BACK":     (0, 0, -1),
    }

    def __init__(self, size):
        super().__init__(size)
        verts, lines = self.calculate_lines()
        self['position'] = VertexBuffer(verts)
        self.line_indices = IndexBuffer(lines)

    def calculate_lines(self):
        vertices = []
        lines = []

        for x in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                vertices = vertices + [[x, y, -self.size]]
                vertices = vertices + [[x, y, self.size]]
                lines = lines + [[len(vertices) - 2, len(vertices) - 1]]

        for x in range(-self.size, self.size+1):
            for z in range(-self.size, self.size+1):
                vertices = vertices+[[x, -self.size, z]]
                vertices = vertices+[[x,  self.size, z]]
                lines = lines+[[len(vertices)-2, len(vertices)-1]]

        for z in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                vertices = vertices+[[-self.size, y, z]]
                vertices = vertices+[[self.size,  y, z]]
                lines = lines+[[len(vertices)-2, len(vertices)-1]]

        return vertices, lines

    def draw_model(self):
        self.draw('lines', self.line_indices)

    def is_valid_location(self, location):
        if location[0] % 1 == 0 and location[1] % 1 == 0 and location[2] % 1 == 0:
            return True
        else:
            return False

    def get_directions_dictionary(self):
        return self.directions

    def get_dimension_count(self):
        return 3
