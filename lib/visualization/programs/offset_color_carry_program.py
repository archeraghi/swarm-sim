import OpenGL.GL as GL
from lib.visualization.programs.offset_color_program import OffsetColorProgram
import ctypes
import numpy as np


class OffsetColorCarryProgram(OffsetColorProgram):
    """
    extended version of OffsetColorProgram.
    Has a carry flag and changes the position and alpha when flag is 1.0
    """

    vertex_shader_file = "lib/visualization/shader/offset_color_carry_vertex.glsl"
    fragment_shader_file = "lib/visualization/shader/frag.glsl"

    def _init_buffers(self, v, n, _):
        """
        extends the init_buffer of OffsetColorProgram class by creating the additional carry flag VBO
        :param v: the vertex model data (position vectors)
        :param n: the normal vector model data
        :return:
        """
        super()._init_buffers(v, n, _)

        self.vbos.append(GL.glGenBuffers(1))

        # init VBO 2 - dynamic color data
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbos[3])
        loc = self.get_attribute_location("carried")
        GL.glEnableVertexAttribArray(loc)
        GL.glVertexAttribPointer(loc, 1, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))
        GL.glVertexAttribDivisor(loc, 1)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 0, np.array([], dtype=np.float32), GL.GL_DYNAMIC_DRAW)

    def update_carried(self, data):
        """
        updates the carry flag data (VBO3)
        :param data: list/array of floats (1.0 = True, 0.0 = False).
        :return:
        """
        self.use()
        gpu_data = np.array(data, dtype=np.float32)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbos[3])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, gpu_data.nbytes, gpu_data, GL.GL_DYNAMIC_DRAW)
