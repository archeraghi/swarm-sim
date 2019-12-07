import sys

import numpy as np
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5 import QtCore


def normalize(v):
    length = np.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    if length != 0:
        return np.array([v[0]/length, v[1]/length, v[2]/length])
    else:
        return np.array([v[0], v[1], v[2]])


def cross(a, b):
    cx = a[1]*b[2] - a[2]*b[1]
    cy = a[2]*b[0] - a[0]*b[2]
    cz = a[0]*b[1] - a[1]*b[0]
    return np.array([cx, cy, cz])


def get_look_at_matrix(eye, at, up):
    npeye = np.array(eye)
    npat = np.array(at)
    npup = np.array(up)

    zaxis = normalize(npeye - npat)
    xaxis = normalize(cross(zaxis, npup))
    yaxis = cross(xaxis, zaxis)

    zaxis *= -1

    look_at_matrix = np.array([
        [xaxis[0], xaxis[1], xaxis[2], 0],
        [yaxis[0], yaxis[1], yaxis[2], 0],
        [zaxis[0], zaxis[1], zaxis[2], 0],
        [0, 0, 0, 1],
    ], dtype=np.float32).transpose()

    return look_at_matrix


def get_translation_matrix(offset):
    x = offset[0]
    y = offset[1]
    z = offset[2]
    translation_matrix = np.array([[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [x, y, z, 1.0]], dtype=np.float32)
    return translation_matrix


def get_orthographic_projection_matrix(left, right, bottom, top, znear, zfar):

    ortho_matrix = np.zeros((4, 4), dtype=np.float32)
    ortho_matrix[0, 0] = 2.0 / (right - left)
    ortho_matrix[3, 0] = -(right + left) / float(right - left)
    ortho_matrix[1, 1] = 2.0 / (top - bottom)
    ortho_matrix[3, 1] = -(top + bottom) / float(top - bottom)
    ortho_matrix[2, 2] = -2.0 / (zfar - znear)
    ortho_matrix[3, 2] = -(zfar + znear) / float(zfar - znear)
    ortho_matrix[3, 3] = 1.0

    return ortho_matrix


def get_perspetive_projection_matrix(fov, aspect, znear, zfar):
    h = np.tan(np.radians(fov/2.0)) * znear
    w = h * aspect

    pers_matrix = np.zeros((4, 4), dtype=np.float32)
    pers_matrix[0, 0] = 2.0 * znear / float(2 * w)
    pers_matrix[1, 1] = 2.0 * znear / float(2 * h)
    pers_matrix[2, 2] = -(zfar + znear) / float(zfar - znear)
    pers_matrix[3, 2] = -2.0 * znear * zfar / float(zfar - znear)
    pers_matrix[2, 3] = -1.0

    return pers_matrix


def eeprint(*args, sep=' ', end='\n'):
    print(*args, sep, end, file=sys.stderr)
    exit(-1)


def eprint(*args, sep=' ', end='\n'):
    print(*args, sep, end, file=sys.stderr)


def load_obj_file(file_path: str):
    """
    loads and parses an .obj file.
    Works only with vertices, normals and texture coordinates and only for triangular faces.
    Any other functions of the "Wavefront" (.obj) file format are ignored!
    :param file_path: path to the .obj file
    :return: list of tuples of vertices, list of tuples of normals, list of tuples of texture coordinates
    """
    model_file = ""
    try:
        model_file = open(file_path, "r").readlines()
    except IOError as e:
        eeprint("ERROR: Cannot open the model file (%s):\n%s" % (file_path, str(e)))

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
            # ignoring smoothing option
            continue
        if split[0] == "v":
            vertices.append((float(split[1]), float(split[2]), float(split[3])))
        elif split[0] == "vn":
            normals.append((float(split[1]), float(split[2]), float(split[3])))
        elif split[0] == "vt":
            tex.append((float(split[1]), float(split[2])))
        elif split[0] == "f":
            for part in split[1:]:
                vn = part.split("/")
                if len(vn) != 3:
                    print("load_obj_file:  accepting only v//n and v/t/n ")
                else:
                    vert_out.append(tuple(vertices[int(vn[0]) - 1]))
                    if vn[1].isnumeric():
                        tex_out.append(tex.__getitem__(int(vn[1]) - 1))
                    norm_out.append(normals.__getitem__(int(vn[2]) - 1))
        else:
            print("load_obj_file: did not understand \"%s\". only accepting v, vn, vt and f." % line[:-1])
    return vert_out, norm_out, tex_out


class LoadingWindow(QMainWindow):
    def __init__(self, message, title):
        """
        simple window for displaying a loading message with a progress bar.
        used for loading the scenario.
        """
        super(LoadingWindow, self).__init__()

        main_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message, self), alignment=QtCore.Qt.AlignBaseline)
        progress = QProgressBar(self)
        progress.setMinimum(0)
        progress.setMaximum(0)
        layout.addWidget(progress, alignment=QtCore.Qt.AlignBaseline)
        main_widget.setLayout(layout)
        main_widget.setFocus()
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle(title)
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)
        self.setCentralWidget(main_widget)
        self.show()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
