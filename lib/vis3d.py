import importlib
import OpenGL.GL as gl
from PyQt5 import QtOpenGL, QtCore
from PyQt5.QtWidgets import QApplication, QSplitter
from vispy.util.transforms import translate, ortho, perspective, rotate
import numpy as np
import time
from lib.visualization.ogl import MatterProgram, GridProgram


class OpenGLWidget(QtOpenGL.QGLWidget):

    def __init__(self, world):
        super().__init__()

        self.setMouseTracking(True)
        self.aspect = 1
        self.radius = 5
        self.theta = 0
        self.phi = 0
        self.x_offset = 0
        self.y_offset = 0
        self.fov = 50
        self.drag_state = False
        self.last_position = []
        self.drag_sensitivity = 1000
        self.rotate_sensitivity = 5
        self.zoom_sensitivity = 100
        self.projection = "perspective"
        self.background = (0.5, 0.5, 0.5, 1.0)
        self.particle_model = None
        self.tile_model = None
        self.marker_model = None
        self.world = world
        self.matter_program = None
        self.grid_program = None

        # debug
        self.offsets = np.random.randint(-10, 10, (100, 3)).flatten("C")

    def set_background(self, color):
        self.background = color
        gl.glClearColor(*self.background)

    def initializeGL(self):
        # set global openGL settings
        # enabling depth test (z buffer)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # setting the clear color
        gl.glClearColor(*self.background)
        # initialize the openGL context and all models
        self.matter_program = MatterProgram(self.world.config_data)
        self.matter_program.set_positions(self.offsets)
        self.grid_program = GridProgram(self.world.grid, self.world.config_data)

    def resizeGL(self, width, height):
        # calculate the aspect ratio
        if height == 0:
            height = 1
        self.aspect = width / height
        # set the openGL viewport
        gl.glViewport(0, 0, width, height)
        # update the view and redraw the scene
        self.update_view()

    def update_view(self):
        # calculate the projection matrix
        if self.projection == "perspective":
            projection = perspective(self.fov, self.aspect, 0.1, 1000)
        elif self.projection == "ortho":
            projection = ortho(-self.radius * self.aspect,
                               self.radius * self.aspect,
                               -self.radius, self.radius, 0.01, 1000)
        else:
            print("warning: unknown projection \""+self.projection+"\"! setting projection to perspective.")
            self.projection = "perspective"
            projection = perspective(self.fov, self.aspect, 0.1, 1000)

        # upload the projection matrix to the gpu
        self.matter_program.update_projection(projection)
        self.grid_program.update_projection(projection)
        # calculate the view matrix
        view = np.dot(np.dot(rotate(self.phi, (0, 1, 0)),
                             rotate(self.theta, (1, 0, 0))),
                      translate([self.x_offset, self.y_offset, -self.radius]))
        # upload the view matrix to the gpu
        self.matter_program.update_view(view)
        self.grid_program.update_view(view)
        # redraw the scene
        self.glDraw()

    def paintGL(self):
        # clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # update particle model offsets
        particles = list(self.world.particle_map_coordinates.keys())
        self.matter_program.set_positions(particles)
        # draw particles
        self.matter_program.draw_particles(len(particles))

        # update marker model offsets
        markers = list(self.world.marker_map_coordinates.keys())
        self.matter_program.set_positions(markers)
        # draw particles
        self.matter_program.draw_markers(len(markers))

        # update tile model offsets
        tiles = list(self.world.tile_map_coordinates.keys())
        self.matter_program.set_positions(tiles)
        # draw particles
        self.matter_program.draw_tiles(len(tiles))
        # draw the grid
        self.grid_program.draw()

    def mousePressEvent(self, a0):
        # starting dragging
        if a0.buttons() & QtCore.Qt.LeftButton or a0.buttons() & QtCore.Qt.RightButton:
            self.drag_state = True
            self.last_position = [a0.x(), a0.y()]

    def mouseReleaseEvent(self, a0):
        # stopping dragging
        if not a0.buttons() & QtCore.Qt.LeftButton and not a0.buttons() & QtCore.Qt.RightButton:
            self.drag_state = False
            self.last_position = []

    def wheelEvent(self, a0):
        # update radius according to the wheel movement
        self.radius += a0.angleDelta().y()/self.zoom_sensitivity
        if self.radius < 0.1:
            self.radius = 0.1
        self.update_view()

    def mouseMoveEvent(self, a0):
        if self.drag_state:
            current_position = [a0.x(), a0.y()]
            drag_amount = [self.last_position[0] - current_position[0], self.last_position[1] - current_position[1]]

            if a0.buttons() & QtCore.Qt.LeftButton and self.world.grid.get_dimension_count() > 2:
                self.rotate_view(drag_amount)

            if a0.buttons() & QtCore.Qt.RightButton:
                self.drag_view(drag_amount)

            self.last_position = current_position

    def rotate_view(self, dragamount):
        self.theta -= dragamount[1] / self.rotate_sensitivity
        self.phi -= dragamount[0] / self.rotate_sensitivity
        if self.theta > 90:
            self.theta = 90
        if self.theta < -90:
            self.theta = -90
        self.update_view()

    def drag_view(self, dragamount):
        self.x_offset -= dragamount[0] / self.drag_sensitivity * self.radius
        self.y_offset += dragamount[1] / self.drag_sensitivity * self.radius
        self.update_view()


class Visualization:
    def __init__(self, world):
        self.world = world
        self.rounds_per_second = 10
        self.running = False
        self.app = None
        self.viewer = None
        self.gui = None
        self.splitter = None

    def init(self):
        # create the QApplication
        self.app = QApplication([])

        # create the opengl widget
        self.viewer = OpenGLWidget(self.world)

        # create the gui
        gui_module = importlib.import_module('gui.' + self.world.config_data.gui)
        self.gui = gui_module.define_gui(self.world)

        # put opengl widget and gui into a splitter window
        self.splitter = QSplitter()
        self.splitter.addWidget(self.gui)  # gui
        self.splitter.addWidget(self.viewer)
        self.splitter.closeEvent = self.close
        self.splitter.setMinimumWidth(self.world.config_data.window_size_x)
        self.splitter.setMinimumHeight(self.world.config_data.window_size_y)
        self.splitter.setWindowTitle("Simulator")
        self.splitter.setSizes([self.world.config_data.window_size_x*0.25,self.world.config_data.window_size_x*0.75])

    def start(self):
        # show the window/splitter-frame
        self.splitter.show()

    @staticmethod
    def close(event):
        exit(0)

    def wait_till_running(self):
        while not self.running:
            self.app.processEvents()
            self.viewer.glDraw()

    def run(self, round_start_timestamp):
        # waiting until simulation starts
        self.wait_till_running()
        self.app.processEvents()
        self.viewer.glDraw()
        # waiting until enough time passed to do the next simulation round.
        waiting_time = (1 / self.rounds_per_second) / 100
        time_elapsed = time.perf_counter() - round_start_timestamp
        while time_elapsed < 1 / self.rounds_per_second:
            # waiting for 1/100 of the round_time
            time.sleep(waiting_time)
            self.wait_till_running()
            self.app.processEvents()
            self.viewer.glDraw()
            time_elapsed = time.perf_counter() - round_start_timestamp
