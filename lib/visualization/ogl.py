import numpy as np
import OpenGL.GL as gl


def load_obj_file(file_path):
    """
    loads and parses an .obj file.
    Works only with vertices, normals and texture coordinates and only for triangular faces.
    Any other functions of the "Wavefront" (.obj) file format are ignored!
    :param file_path: path to the .obj file
    :return: list of tuples of vertices, list of tuples of normals, list of tuples of texture coordinates
    """
    try:
        model_file = open(file_path, "r").readlines()
    except IOError:
        raise RuntimeError("Cannot load model file: ", file_path)
    vertices = []
    normals = []
    tex = []

    vert_out = []
    norm_out = []
    tex_out = []
    for line in model_file:
        if len(line) == 0 or line[0] == "#":
            continue
        split = line.split(" ")
        if split[0] == "s":
            if split[1].find("off") == -1:
                print("load_obj_file: smoothing not supported!")
            continue
        if split[0] == "v":
            vertices = vertices + [[float(split[1]), float(split[2]), float(split[3])]]
        elif split[0] == "vn":
            normals = normals + [[float(split[1]), float(split[2]), float(split[3])]]
        elif split[0] == "vt":
            tex = tex + [[float(split[1]), float(split[2])]]
        elif split[0] == "f":
            for part in split[1:]:
                vn = part.split("/")
                if len(vn) != 3:
                    print("load_obj_file:  accepting only v//n and v/t/n ")
                else:
                    vert_out.append(tuple(vertices[int(vn[0]) - 1]))
                    if vn[1].isnumeric():
                        tex_out = tex_out + tex[int(vn[1]) - 1]
                    norm_out = norm_out + [normals[int(vn[2]) - 1]]
        else:
            print("load_obj_file: did not understand \"", line[:-1], "\". only accepting v, vn, vt and f")
    return vert_out, norm_out, tex_out


class Program:
    def __init__(self, vertex_file, fragment_file):
        """
        Superclass for Opengl Programs.
        compiles the given shader source files and gives rudimentary functions
        like updating the view and projection matrices. (assuming the matrices are defined in the shader)
        :param vertex_file: file path to the vertex shader
        :param fragment_file: file path to the fragment shader
        """
        # creating GL Program
        self.program = gl.glCreateProgram()
        # loading shader source files
        self.vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        try:
            vert_source = open(vertex_file).read()
            frag_source = open(fragment_file).read()
            self.init_shaders(vert_source, frag_source)
        except IOError:
            raise RuntimeError("Couldn't read the shader source files!")

        self.use()

    def init_shaders(self, vert, frag):
        """
        compiles and links shaders
        :param vert: vertex shader source string
        :param frag: fragment shader source string
        :return:
        """
        # set the sources
        gl.glShaderSource(self.vertex, vert)
        gl.glShaderSource(self.fragment, frag)
        # compile vertex shader
        gl.glCompileShader(self.vertex)
        if not gl.glGetShaderiv(self.vertex, gl.GL_COMPILE_STATUS):
            e = gl.glGetShaderInfoLog(self.vertex).decode()
            print(e)
            raise RuntimeError("Vertex shader compilation error")

        # compile fragment shader
        gl.glCompileShader(self.fragment)
        if not gl.glGetShaderiv(self.fragment, gl.GL_COMPILE_STATUS):
            e = gl.glGetShaderInfoLog(self.fragment).decode()
            print(e)
            raise RuntimeError("Fragment shader compilation error")

        # attach the shaders to the matter program
        gl.glAttachShader(self.program, self.vertex)
        gl.glAttachShader(self.program, self.fragment)

        # link the shaders to the matter program
        gl.glLinkProgram(self.program)
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')

        # detach the shaders from matter program
        gl.glDetachShader(self.program, self.vertex)
        gl.glDetachShader(self.program, self.fragment)

    def use(self):
        """
        shortcut for this one line.. sets this Program to the used one
        :return:
        """
        gl.glUseProgram(self.program)

    def update_projection(self, projection_matrix):
        """
        Updates the projection matrix in the vertex shader program
        :param projection_matrix: 4x4 float32 projection matrix
        :return:
        """
        self.use()
        loc = gl.glGetUniformLocation(self.program, "projection")
        gl.glUniformMatrix4fv(loc, 1, False, projection_matrix)

    def update_view(self, view_matrix):
        """
        Updates the view matrix in the vertex shader program
        :param view_matrix: 4x4 float32 view matrix
        :return:
        """
        self.use()
        loc = gl.glGetUniformLocation(self.program, "view")
        gl.glUniformMatrix4fv(loc, 1, False, view_matrix)


class MatterProgram(Program):
    vertex_shader_file = "lib/visualization/shader/vert.glsl"
    fragment_shader_file = "lib/visualization/shader/frag.glsl"

    def __init__(self, config_data):
        """
        initializes/loads/creates all necessary data/buffers/shaders for drawing Matter (Patricles, Tiles, Markers)
        :param config_data: configuration data for initial state and model filenames
        """
        super().__init__(self.vertex_shader_file, self.fragment_shader_file)
        # set init state from config
        self.particle_color = config_data.particle_color
        self.tile_color = config_data.tile_color
        self.marker_color = config_data.marker_color

        # load data
        p_vert, p_norm, _ = load_obj_file("lib/visualization/models/" + config_data.particle_model_file)
        self.particle_model_offset = 0
        self.particle_model_length = len(p_vert)

        t_vert, t_norm, _ = load_obj_file("lib/visualization/models/" + config_data.tile_model_file)
        self.tile_model_offset = self.particle_model_length
        self.tile_model_length = len(t_vert)

        m_vert, m_norm, _ = load_obj_file("lib/visualization/models/" + config_data.marker_model_file)
        self.marker_model_offset = self.tile_model_offset + self.tile_model_length
        self.marker_model_length = len(m_vert)

        # prepare data array
        data = self.prepare_data(p_vert + t_vert + m_vert, p_norm + t_norm + m_norm)
        # upload data to gpu
        self.create_gpu_buffer(data)

        # init the shader uniforms
        self.light_angle = 0
        self.init_uniforms()

    def prepare_data(self, vert, norm):
        """
        prepares the vertex attribute data for upload to the gpu
        :param vert: vertices / positions, format: X * 3 floats
        :param norm: face-normals, format: X * 3 floats
        :return: array of tuples, format: [(x0, y0, z0), (nx0, ny0, nz0), (x1, y1, y1), (nx1, ny1, nz1), ... ]
        """
        # prepare data for gpu
        data_length = self.particle_model_length + self.tile_model_length + self.marker_model_length

        data = np.zeros(data_length, [("position", np.float32, 3),
                                      ("normal", np.float32, 3)])
        # set the position data
        data['position'] = vert
        # set the normal data
        data['normal'] = norm
        return data


    def create_gpu_buffer(self, data):
        """
        Initializes and creates the VBOs in the GPU.
        Uploads the given data to the created buffers.
        :param data: data for the gpu
        :return:
        """
        # generate positions and normals VBO
        buffer = gl.glGenBuffers(1)
        # calculate the stride
        stride = data.strides[0]
        # get the location of positions array in the shader
        loc = gl.glGetAttribLocation(self.program, "position")
        # enable the positions attribute array in the VBO
        gl.glEnableVertexAttribArray(loc)
        # bind the positions array in VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        # define the positions array pointer in the VBO
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, gl.ctypes.c_void_p(0))

        # calculate the offset from "position" variable in data for the normal array
        offset = gl.ctypes.c_void_p(data.dtype["position"].itemsize)
        # get the location of normals array in the shader
        loc = gl.glGetAttribLocation(self.program, "normal")
        # enable the normals attribute array in the VBO
        gl.glEnableVertexAttribArray(loc)
        # bind the normals array in VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        # define the normals array pointer in the VBO
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

        # upload the positions & normals data to the GPU
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

        # create collor/offset buffer
        co_buffer = gl.glGenBuffers(1)
        # get the location
        loc = gl.glGetAttribLocation(self.program, "offset")
        # enable the offsets array
        gl.glEnableVertexAttribArray(loc)
        # bind the offsets array
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, co_buffer)
        # define the offsets array pointer
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, gl.ctypes.c_void_p(0))
        # set the vertex attribute divisor to change with new instance and not with new attribute
        gl.glVertexAttribDivisor(loc, 1)


    def init_uniforms(self):
        """
        initializes the shader uniforms to defaults from config.ini
        :return:
        """
        eye = np.eye(4, 4)
        loc = gl.glGetUniformLocation(self.program, "projection")
        gl.glUniformMatrix4fv(loc, 1, False, eye)

        loc = gl.glGetUniformLocation(self.program, "view")
        gl.glUniformMatrix4fv(loc, 1, False, eye)

        loc = gl.glGetUniformLocation(self.program, "scale")
        gl.glUniform1f(loc, 1.0)

        loc = gl.glGetUniformLocation(self.program, "ambient_light")
        gl.glUniform1f(loc, 0.2)

        loc = gl.glGetUniformLocation(self.program, "light_direction")
        gl.glUniform3f(loc, np.sin(self.light_angle), 0.0, np.cos(self.light_angle))

        loc = gl.glGetUniformLocation(self.program, "light_color")
        gl.glUniform4f(loc, 1.0, 1.0, 1.0, 1.0)

        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, 0.0, 0.0, 0.0, 0.0)

    def draw_particles(self, count):
        """
        draws the given amount of particles
        :param count: amount of particles to draw (presumably equal to the amount of offsets/positions)
        :return:
        """
        self.use()
        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, *self.particle_color)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, self.particle_model_offset, self.particle_model_length, count)

    def draw_tiles(self, count):
        """
        draws the given amount of tiles
        :param count: amount of tiles to draw (presumably equal to the amount of offsets/positions)
        :return:
        """
        self.use()
        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, *self.tile_color)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, self.tile_model_offset, self.tile_model_length, count)

    def draw_markers(self, count):
        """
        draws the given amount of markers
        :param count: amount of markers to draw (presumably equal to the amount of offsets/positions)
        :return:
        """
        self.use()
        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, *self.marker_color)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, self.marker_model_offset, self.marker_model_length, count)

    def set_positions(self, data):
        """
        uploads the model positions to the GPU
        :param data: offsets/positions of models, format: [(x0, y0, z0), (x1, y1, z1), ...]
        :return:
        """
        self.use()
        gpu_data = np.array(data, dtype=np.float32)
        loc = gl.glGetAttribLocation(self.program, "offset")
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, loc)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, gpu_data.nbytes, gpu_data, gl.GL_DYNAMIC_DRAW)

    def rotate_light(self, angle):
        self.use()
        self.light_angle += angle
        loc = gl.glGetUniformLocation(self.program, "light_direction")
        gl.glUniform3f(loc, np.sin(np.radians(self.light_angle)), 0.0, np.cos(np.radians(self.light_angle)))


class GridProgram(Program):
    vertex_shader_file = "lib/visualization/shader/gridvert.glsl"
    fragment_shader_file = "lib/visualization/shader/frag.glsl"

    def __init__(self, grid, config_data):
        """
        initializes/loads/creates all necessary data/buffers/shaders for drawing the Grid
        :param grid: the grid object to be visualized
        """
        super().__init__(self.vertex_shader_file, self.fragment_shader_file)

        # get lines data
        self.grid = grid
        lines = self.grid.get_lines()

        # prepare data
        self.length = len(lines)
        data = np.zeros(self.length, [("position", np.float32, 3)])
        data['position'] = lines

        # upload data to gpu
        self.create_gpu_buffer(data)

        # init the shader uniforms
        self.color = config_data.grid_color
        self.init_uniforms()

    def create_gpu_buffer(self, data):
        """
        Initializes and creates the VBOs in the GPU.
        Uploads the given data to the created buffers.
        :param data: data for the gpu
        :return:
        """
        # generate positions and normals VBO
        buffer = gl.glGenBuffers(1)
        # get the location of positions array in the shader
        loc = gl.glGetAttribLocation(self.program, "position")
        # enable the positions attribute array in the VBO
        gl.glEnableVertexAttribArray(loc)
        # bind the positions array in VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        # define the positions array pointer in the VBO
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, data.strides[0], gl.ctypes.c_void_p(0))
        # upload the positions & normals data to the GPU
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    def init_uniforms(self):
        """
        initializes the shader uniforms to defaults from config.ini
        :return:
        """
        eye = np.eye(4, 4)
        loc = gl.glGetUniformLocation(self.program, "projection")
        gl.glUniformMatrix4fv(loc, 1, False, eye)

        loc = gl.glGetUniformLocation(self.program, "view")
        gl.glUniformMatrix4fv(loc, 1, False, eye)

        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, *self.color)

    def draw(self):
        """
        draws the grid
        :return:
        """
        self.use()
        gl.glDrawArrays(gl.GL_LINES, 0, self.length)

    def set_color(self, color):
        self.use()
        self.color = color
        print(color)
        loc = gl.glGetUniformLocation(self.program, "model_color")
        gl.glUniform4f(loc, *self.color)
