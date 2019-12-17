import OpenGL.GL as gl

from lib.swarm_sim_header import eprint
from lib.visualization.programs.program import Program
import numpy as np
import ctypes


class OffsetColorProgram(Program):
    """
    OpenGL Program for Models which are loaded from a model file (Wavefront / .obj format) and are drawn multiple times
    at different positions with different colors
    """

    vertex_shader_file = "lib/visualization/shader/offset_color_vertex.glsl"
    fragment_shader_file = "lib/visualization/shader/frag.glsl"

    def __init__(self, model_file: str):
        self.vbos = list()
        self.amount = 0
        super().__init__(self.vertex_shader_file, self.fragment_shader_file, model_file)

    def _init_buffers(self, vertices, normals, _):
        # prepare data for the gpu
        gpu_data = np.array(vertices + normals, dtype=np.float32)

        # create VBOs
        self.vbos = list(gl.glGenBuffers(3))

        # init VBO 0 - static mesh data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[0])
        loc = self.get_attribute_location("position")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        loc = self.get_attribute_location("normal")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(self.size*12))
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

        # init VBO 2 - dynamic color data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[2])
        loc = self.get_attribute_location("color")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glVertexAttribDivisor(loc, 1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 0, np.array([], dtype=np.float32), gl.GL_DYNAMIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def draw(self):
        """
        sets the vao and draws the scene
        :return:
        """
        self.use()
        gl.glBindVertexArray(self._vao)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, self.size, self.amount)

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
        self.amount = len(gpu_data)/3.0
        if len(gpu_data) % 3.0 != 0.0:
            eprint("WARNING: invalid offset data! "
                   "Amount of coordinate components not dividable by 3 (not in xyz format?)!")
        self.amount = int(self.amount)

    def update_colors(self, data):
        """
        updates the color data (VBO2)
        :param data: list/array of rgba values. (dimensions are irrelevant)
        :return:
        """
        self.use()
        gpu_data = np.array(data, dtype=np.float32).flatten()
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbos[2])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, gpu_data.nbytes, gpu_data, gl.GL_DYNAMIC_DRAW)
        if len(gpu_data) % 4.0 != 0.0:
            eprint("WARNING: invalid color data! "
                   "Amount of color components not dividable by 4 (not in rgba format?)!")
