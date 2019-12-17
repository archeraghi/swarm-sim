from lib.swarm_sim_header import eprint
from lib.visualization.programs.program import Program
import OpenGL.GL as gl
import numpy as np
import ctypes


class GridProgram(Program):
    """
    OpenGL Program for the visualization of the grid and the included coordinates
    """
    vertex_shader_file = "lib/visualization/shader/grid_vertex.glsl"
    fragment_shader_file = "lib/visualization/shader/frag.glsl"

    def __init__(self, grid, line_color, model_color, coordinate_model_file):
        """
        initializes/loads/creates all necessary data/buffers/shaders for drawing the Grid
        :param grid: the grid object to be visualized
        :param line_color: color of the grid lines
        :param model_color: color of the grid coordinate model
        :param coordinate_model_file: model file of the coordinates
        """
        self.grid = grid
        self.width = 1
        self.line_offset = 0
        self.line_length = 0
        self.amount = 0
        self.show_coordinates = True
        self.show_lines = True
        self.vbos = list()
        super().__init__(self.vertex_shader_file, self.fragment_shader_file, coordinate_model_file)
        self.set_line_color(line_color)
        self.set_model_color(model_color)

    def _init_buffers(self, verts, normals, _):

        # get lines data
        lines = self.grid.get_lines()

        self.line_offset = len(verts)
        self.line_length = len(lines)
        # prepare data for the gpu
        gpu_data = np.array(verts + lines + normals, dtype=np.float32)

        # create VBO
        self.vbos = list(gl.glGenBuffers(2))
        # init VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[0])
        loc = self.get_attribute_location("position")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))

        loc = self.get_attribute_location("normal")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p((len(verts) + len(lines)) * 12))
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 12 * len(gpu_data), gpu_data, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        # init VBO 1 - dynamic offset data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[1])
        loc = self.get_attribute_location("offset")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glVertexAttribDivisor(loc, 1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 0, np.array([], dtype=np.float32), gl.GL_DYNAMIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def _init_uniforms(self):
        """
        initializes the shader uniforms
        :return:
        """
        super()._init_uniforms()
        self.set_line_color((0.0, 0.0, 0.0, 0.0))
        self.set_model_color((0.0, 0.0, 0.0, 0.0))
        self.set_line_scaling((1.0, 1.0, 1.0))

    def draw(self):
        """
        draws the grid lines
        :return:
        """
        self.use()
        if self.show_lines:
            self._drawing_lines(True)
            gl.glDrawArraysInstanced(gl.GL_LINES, self.line_offset, self.line_length, self.amount)
        if self.show_coordinates:
            self._drawing_lines(False)
            gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, self.size, self.amount)

    def set_width(self, width):
        """
        sets the width of the grid lines (updates the glLineWidth globally!!!)
        :param width: the width (int)
        :return:
        """
        self.width = width
        gl.glLineWidth(self.width)

    def set_line_color(self, color):
        """
        sets the line_color uniform in the grid vertex shader
        :param color: the color (rgba)
        :return:
        """
        self.use()

        gpu_data = np.array(color, dtype=np.float32).flatten()
        if len(gpu_data) != 4:
            eprint("ERROR: length of set_line_color parameter not correct, expected 4 got %d " % len(gpu_data))
        else:
            loc = self.get_uniform_location("line_color")
            gl.glUniform4f(loc, *gpu_data)

    def get_line_color(self):
        """
        reads the line color from the vertex shader
        :return:
        """
        return self.get_uniform("line_color", 4)

    def set_model_color(self, color):
        """
        sets the model_color uniform in the grid vertex shader
        :param color: the color (rgba)
        :return:
        """
        self.use()
        gpu_data = np.array(color, dtype=np.float32).flatten()
        if len(gpu_data) != 4:
            eprint("ERROR: length of set_model_color parameter not correct, expected 4 got %d " % len(gpu_data))
        else:
            loc = self.get_uniform_location("model_color")
            gl.glUniform4f(loc, *gpu_data)

    def get_model_color(self):
        """
        reads the model color from the vertex shader
        :return:
        """
        return self.get_uniform("model_color", 4)

    def _drawing_lines(self, line_flag: bool):
        loc = self.get_uniform_location("drawing_lines")
        gl.glUniform1i(loc, gl.GL_TRUE if line_flag else gl.GL_FALSE)

    def update_offsets(self, data):
        """
        updates the offsets/positions data (VBO 1)
        :param data: array of 3d positions
        :return:
        """
        self.use()
        gpu_data = np.array(data, dtype=np.float32).flatten()
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[1])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, gpu_data.nbytes, gpu_data, gl.GL_DYNAMIC_DRAW)
        self.amount = len(gpu_data) / 3.0
        if len(gpu_data) % 3.0 != 0.0:
            eprint("WARNING: invalid offset data! "
                   "Amount of coordinate components not dividable by 3 (not in xyz format?)!")
        self.amount = int(self.amount)

    def set_line_scaling(self, scaling):
        """
        sets the line_scaling uniform in the vertex shader
        :param scaling: the scaling vector
        :return:
        """
        self.use()
        gpu_data = np.array(scaling, dtype=np.float32).flatten()
        if len(gpu_data) != 3:
            eprint("ERROR: length of set_line_scaling parameter not correct, expected 3 got %d " % len(gpu_data))
        else:
            loc = self.get_uniform_location("line_scaling")
            gl.glUniform3f(loc, *gpu_data)

    def get_line_scaling(self):
        """
        reads the line scaling vector from the vertex shader
        :return:
        """
        return self.get_uniform("line_scaling", 3)
