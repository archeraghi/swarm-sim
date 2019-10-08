from PIL import Image
from vispy.gloo import Program, IndexBuffer, VertexBuffer
from vispy.util.transforms import translate
from vispy.geometry import create_sphere
from abc import ABC, abstractmethod
import numpy as np


def load_obj_file(file_path):
    model_file = open(file_path, "r").readlines()
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
            tex = tex+[[float(split[1]), float(split[2])]]
        elif split[0] == "f":
            for part in split[1:]:
                vn = part.split("/")
                if len(vn) != 3:
                    print("load_obj_file:  accepting only v//n and v/t/n ")
                else:
                    vert_out = vert_out + [vertices[int(vn[0]) - 1]]
                    if vn[1].isnumeric():
                        tex_out = tex_out + [tex[int(vn[1]) - 1]]
                    norm_out = norm_out + [normals[int(vn[2]) - 1]]
        else:
            print("load_obj_file: did not understand \"", line[:-1], "\". only accepting v, vn, vt and f")
    return vert_out, norm_out, tex_out


class Model(Program, ABC):
    def __init__(self, vertex_shader_file, fragment_shader_file):
        # open and compile the given shader files.
        super().__init__(open(vertex_shader_file).read(),
                         open(fragment_shader_file).read())

    @abstractmethod
    def draw_model(self):
        pass

    def translate_model(self, new_position):
        self['model'] = translate(new_position)


tex_vertex_shader_path = "lib/visualization/shader/bodyVertexShaderWithTex.glsl"
tex_fragment_shader_path = "lib/visualization/shader/bodyFragmentShaderWithTex.glsl"


class TexturedModel(Model, ABC):
    def __init__(self, model_file, texture_file):
        super().__init__(tex_vertex_shader_path, tex_fragment_shader_path)
        self.model_file = model_file
        self.texture_file = texture_file
        self.light_angle = 0

        # initialize shader uniform variables
        self['ambient_light'] = 0.1
        self['scale'] = 1
        self['view'] = translate((0, 0, 0))
        self['model'] = np.eye(4, dtype=np.float32)
        self['projection'] = np.eye(4, dtype=np.float32)
        self['light_color'] = (1, 1, 1, 1)
        self['light_direction'] = (np.sin(self.light_angle), 0, np.cos(self.light_angle))

        # load the model
        self.vertices, self.normals, self.tex_coords = load_obj_file(self.model_file)

        # upload shader attributes to the gpu
        self['position'] = self.vertices
        self['normal'] = self.normals
        self['uv'] = self.tex_coords
        self['texture'] = Image.open(self.texture_file)


single_color_vertex_shader_path = "lib/visualization/shader/bodyVertexShader.glsl"
single_color_fragment_shader_path = "lib/visualization/shader/bodyFragmentShader.glsl"


class SingleColorModel(Model, ABC):
    def __init__(self, model_file, color):
        super().__init__(single_color_vertex_shader_path, single_color_fragment_shader_path)

        self.light_angle = 0

        # initialize shader uniform variables
        self['view'] = translate((0, 0, 0))
        self['scale'] = 1
        self['model'] = np.eye(4, dtype=np.float32)
        self['projection'] = np.eye(4, dtype=np.float32)
        self['light_color'] = (1, 1, 1, 1)
        self['light_direction'] = (np.sin(self.light_angle), 0, np.cos(self.light_angle))

        self['model_color'] = color
        self['ambient_light'] = 0.1

        # calculate the mesh data for a sphere
        self.vertices, self.normals, self.tex_coords = load_obj_file(model_file)
        # upload shader attributes to the gpu
        self['position'] = self.vertices
        self['normal'] = self.normals


class ParticleModel(SingleColorModel):

    def draw_model(self):
        self.draw()

    def rotate_light(self, angle):
        self.light_angle += angle
        self['light_direction'] = (np.sin(self.light_angle), 0, np.cos(self.light_angle))


class TileModel(TexturedModel):

    def draw_model(self):
        self.draw('triangles')

    def rotate_light(self, angle):
        self.light_angle += angle
        self['light_direction'] = (np.sin(self.light_angle), 0, np.cos(self.light_angle))


class MarkerModel(SingleColorModel):

    def draw_model(self):
        self.draw('triangles')

    def rotate_light(self, angle):
        self.light_angle += angle
        self['light_direction'] = (np.sin(self.light_angle), 0, np.cos(self.light_angle))




