import inspect

import OpenGL.GL as GL
from PIL import Image
from PyQt5 import QtOpenGL, QtGui, QtCore

from lib.swarm_sim_header import eprint
from lib.visualization.programs.offset_color_carry_program import OffsetColorCarryProgram
from lib.visualization.programs.offset_color_program import OffsetColorProgram
from lib.visualization.programs.grid_program import GridProgram
import numpy as np
import time


class OGLWidget(QtOpenGL.QGLWidget):

    def __init__(self, world, camera):
        """
        Main Class for managing the Visualization / OpenGL Programs / Visualization data
        :param world: the world class
        :param camera: a camera for the visualization
        """
        super(OGLWidget, self).__init__()

        self.debug = False
        self.world = world
        self.setMouseTracking(True)
        self.drag_state = False
        self.show_center = world.config_data.show_center
        self.show_focus = world.config_data.show_focus
        self.keyPressEventHandler = None
        self.ctrl = False
        self.last_position = []
        self.mouse_pos = [0, 0]
        self.drag_sensitivity = 1000
        self.rotation_sensitivity = 5
        self.zoom_sensitivity = 100
        self.cursor_zoom_sensitivity = 200
        self.cursor_type = 'tile'

        self.camera = camera

        # on init the background will be set from this variable, later on only by the setter
        self.background = world.config_data.background_color

        # programs, program flags and dynamic data
        self.programs = {}
        self.particle_offset_data = {}
        self.particle_update_flag = False
        self.tile_offset_data = {}
        self.tile_update_flag = False
        self.location_offset_data = {}
        self.location_update_flag = False

    def update_scene(self):
        """
        updates the projection, view and world matrices for the scene, and the position of the cursor, because
        the it depends heavily on the matrices.
        :return:
        """

        self.update_programs_projection_matrix()
        self.update_programs_view_matrix()
        self.update_programs_world_matrix()
        if self.ctrl:
            self.update_cursor_data()
        self.glDraw()

    def update_data(self):
        """
        updates the offset, color and carry data for particles, tiles and locations.
        is called mainly by the run method in Visualization once per round.
        :return:
        """
        if self.particle_update_flag:
            self.particle_update_flag = False
            tmp = np.array(list(self.particle_offset_data.values())).transpose()
            if len(tmp) == 0:
                self.programs["particle"].update_offsets([])
                self.programs["particle"].update_colors([])
                self.programs["particle"].update_carried([])
            else:
                self.programs["particle"].update_offsets(tmp[0].tolist())
                self.programs["particle"].update_colors(tmp[1].tolist())
                self.programs["particle"].update_carried(tmp[2].tolist())

        if self.tile_update_flag:
            self.tile_update_flag = False
            tmp = np.array(list(self.tile_offset_data.values())).transpose()
            if len(tmp) == 0:
                self.programs["tile"].update_offsets([])
                self.programs["tile"].update_colors([])
                self.programs["tile"].update_carried([])
            else:

                self.programs["tile"].update_offsets(tmp[0].tolist())
                self.programs["tile"].update_colors(tmp[1].tolist())
                self.programs["tile"].update_carried(tmp[2].tolist())

        if self.location_update_flag:
            self.location_update_flag = False

            tmp = np.array(list(self.location_offset_data.values())).transpose()
            if len(tmp) == 0:
                self.programs["location"].update_offsets([])
                self.programs["location"].update_colors([])
            else:
                self.programs["location"].update_offsets(tmp[0].tolist())
                self.programs["location"].update_colors(tmp[1].tolist())

    def initializeGL(self):
        """
        This method is called when the OpenGL context was successfully created by the PyQt5 library.
        This is the first function which can use OpenGL calls. Before that, a OpenGL code will result in an error.
        All OpenGL Programs are created and initialized here.
        :return:
        """
        # set global openGL settings
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glClearColor(*self.background, 1.0)

        # initialize the openGL programs
        self.programs["particle"] = OffsetColorCarryProgram(self.world.config_data.particle_model_file)
        self.programs["particle"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["particle"].set_model_scaling(self.world.config_data.particle_scaling)

        self.programs["tile"] = OffsetColorCarryProgram(self.world.config_data.tile_model_file)
        self.programs["tile"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["tile"].set_model_scaling(self.world.config_data.tile_scaling)

        self.programs["location"] = OffsetColorProgram(self.world.config_data.location_model_file)
        self.programs["location"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["location"].set_model_scaling(self.world.config_data.location_scaling)

        self.programs["grid"] = GridProgram(self.world.grid, self.world.config_data.line_color,
                                            self.world.config_data.coordinates_color,
                                            self.world.config_data.tile_model_file)
        self.programs["grid"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["grid"].set_line_scaling(self.world.config_data.line_scaling)
        self.programs["grid"].show_lines = self.world.config_data.show_lines
        self.programs["grid"].set_model_scaling(self.world.config_data.coordinates_scaling)
        self.programs["grid"].show_coordinates = self.world.config_data.show_coordinates
        self.programs["grid"].update_offsets(self.world.grid.get_box(self.world.grid.size))

        # showing coordinates in 2D is not really necessary, since all coordinates are easy to spot on the grid
        # and there's no depth
        if self.world.grid.get_dimension_count() == 2:
            self.programs["grid"].show_coordinates = False

        self.programs["center"] = OffsetColorProgram(self.world.config_data.particle_model_file)
        self.programs["center"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["center"].set_model_scaling((0.3, 0.3, 0.3))
        self.programs["center"].update_offsets([self.world.grid.get_center()])
        self.programs["center"].update_colors(self.world.config_data.center_color)

        self.programs["focus"] = OffsetColorProgram(self.world.config_data.particle_model_file)
        self.programs["focus"].set_model_scaling((0.3, 0.3, 0.3))
        self.programs["focus"].update_offsets(self.camera.get_look_at())
        self.programs["focus"].update_colors(self.world.config_data.focus_color)

        # cursor programs.. loading in the init, so on change it doesnt has to be loaded again
        self.programs["cursor_tile"] = OffsetColorProgram(self.world.config_data.tile_model_file)
        self.programs["cursor_tile"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["cursor_tile"].set_model_scaling((1.1, 1.1, 1.1))
        self.programs["cursor_tile"].update_offsets([0.0, 0.0, 0.0])
        self.programs["cursor_tile"].update_colors(self.world.config_data.cursor_color)

        self.programs["cursor_particle"] = OffsetColorProgram(self.world.config_data.particle_model_file)
        self.programs["cursor_particle"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["cursor_particle"].set_model_scaling((1.1, 1.1, 1.1))
        self.programs["cursor_particle"].update_offsets([0.0, 0.0, 0.0])
        self.programs["cursor_particle"].update_colors(self.world.config_data.cursor_color)

        self.programs["cursor_location"] = OffsetColorProgram(self.world.config_data.location_model_file)
        self.programs["cursor_location"].set_world_scaling(self.world.grid.get_scaling())
        self.programs["cursor_location"].set_model_scaling((1.1, 1.1, 1.1))
        self.programs["cursor_location"].update_offsets([0.0, 0.0, 0.0])
        self.programs["cursor_location"].update_colors(self.world.config_data.cursor_color)

    def resizeGL(self, width, height):
        """
        Is called by PyQt5 library when the OpenGLWidget is resized.
        :param width: width of screen in pixels
        :param height: height of screen in pixels
        :return:
        """
        if height == 0:
            height = 1
        if width == 0:
            width = 1
        self.camera.set_viewport(width, height)

        # set the openGL viewport
        GL.glViewport(0, 0, width, height)

        # update matrices
        self.update_scene()

    def update_programs_projection_matrix(self):
        """
        updates the projection matrix of all OpenGL programs
        :return:
        """
        # upload the projection matrix to the gpu
        for p in self.programs.values():
            p.set_projection_matrix(self.camera.projection_matrix)

    def update_programs_world_matrix(self):
        """
        updates the world matrix of all OpenGL programs
        :return:
        """
        # upload the model matrix to the gpu
        for p in self.programs.values():
            p.set_world_matrix(self.camera.world_matrix)

    def update_programs_view_matrix(self):
        """
        updates the view matrix of all OpenGL programs
        :return:
        """
        # upload the view matrix to the gpu
        for p in self.programs.values():
            p.set_view_matrix(self.camera.view_matrix)

    def update_cursor_data(self):
        """
        updates the position of the cursor
        :return:
        """
        # updating only the current cursor program
        self.programs["cursor_"+self.cursor_type].update_offsets(
            self.world.grid.get_nearest_valid_coordinates(self.camera.cursor_position))

    def rotate_light(self, angle):
        """
        rotates the light direction in all programs
        :param angle:
        :return:
        """
        for p in self.programs.values():
            p.rotate_light(angle)

    def paintGL(self):
        """
        The main Draw Method.
        All drawing calls originate here.
        It will be called only when a new frame is needed. No change -> no new frame
        :return:
        """
        # clear the screen
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # draw
        self.programs["particle"].draw()
        self.programs["location"].draw()
        self.programs["tile"].draw()
        self.programs["grid"].draw()

        # center
        if self.show_center:
            self.programs["center"].draw()

        # cursor
        if self.ctrl:
            self.programs["cursor_"+self.cursor_type].draw()

        if self.show_focus:
            self.programs["focus"].draw()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        """
        Is called by PyQt5 library, when a mouse button is pressed.
        Is used to set a tile or remove one on current cursers position and to detect dragging
        :param a0: all mouse press event data
        :return:
        """
        # starting dragging
        if self.ctrl and int(a0.buttons()) & QtCore.Qt.LeftButton:
            nl = self.world.grid.get_nearest_valid_coordinates(self.camera.cursor_position)
            if self.cursor_type == 'tile':
                if nl in self.world.tile_map_coordinates:
                    self.world.remove_tile_on(nl)
                else:
                    self.world.add_tile(nl)
            if self.cursor_type == 'particle':
                if nl in self.world.particle_map_coordinates:
                    self.world.remove_particle_on(nl)
                else:
                    self.world.add_particle(nl)
            if self.cursor_type == 'location':
                if nl in self.world.location_map_coordinates:
                    self.world.remove_location_on(nl)
                else:
                    self.world.add_location(nl)
            self.update_data()
            self.glDraw()
        else:
            if a0.button() & QtCore.Qt.LeftButton or a0.button() & QtCore.Qt.RightButton:
                self.drag_state = True
                self.last_position = [a0.x(), a0.y()]

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        """
        Is called by PyQt5 library, when a mouse button is released.
        Used for detecting the end of dragging.
        :param a0: all mouse release data
        :return:
        """
        # stopping dragging
        if not a0.button() & QtCore.Qt.LeftButton and not a0.button() & QtCore.Qt.RightButton:
            self.drag_state = False
            self.last_position = []

    def wheelEvent(self, a0: QtGui.QWheelEvent):
        """
        Is called by PyQt5 library, when the mouse Wheel is beeing scrolled.
        Used to zoom in and out, and move the cursor in z-direction (relative to the camera)
        :param a0: all mouse wheel event data
        :return:
        """
        if self.ctrl:
            if self.world.grid.get_dimension_count() < 3:
                self.camera.update_radius(a0.angleDelta().y() / self.zoom_sensitivity)
                self.camera.set_cursor_radius(-self.camera.get_radius())
            else:
                self.camera.update_cursor_radius(-a0.angleDelta().y() / self.cursor_zoom_sensitivity)
        else:
            self.camera.update_radius(a0.angleDelta().y() / self.zoom_sensitivity)

        self.update_scene()
        self.glDraw()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        """
        Is called by PyQt5 library, when the mouse has moved over the OpenGLWidget.
        Used to update mouse position for the cursor and calling the drag functions.
        :param a0: mouse move event data
        :return:
        """
        self.setFocus()
        self.mouse_pos = [a0.x(), a0.y()]
        if self.ctrl:
            self.camera.update_mouse_position(self.mouse_pos)
            self.update_cursor_data()
            self.glDraw()
        else:
            if self.drag_state:
                drag_amount = [self.last_position[0] - self.mouse_pos[0], self.last_position[1] - self.mouse_pos[1]]

                if int(a0.buttons()) & QtCore.Qt.LeftButton and self.world.grid.get_dimension_count() > 2:
                    self.rotate_view(drag_amount)

                if int(a0.buttons()) & QtCore.Qt.RightButton:
                    self.drag_view(drag_amount)

                self.last_position = self.mouse_pos

    def rotate_view(self, drag_amount):
        """
        is called by mouseMoveEvent when the left mouse button is being pressed.
        rotates the camera around the current look_at point
        :param drag_amount: amount of pixels dragged
        :return:
        """
        self.camera.rotate(- drag_amount[0] / self.rotation_sensitivity, drag_amount[1] / self.rotation_sensitivity)

        self.update_programs_world_matrix()
        self.update_programs_view_matrix()
        self.glDraw()

    def drag_view(self, drag_amount):
        """
        is called by mouseMoveEvent when the right mouse button is being pressed.
        drags the camera up/down, left/right (relative to the camera) - changes the look_at point.
        :param drag_amount:
        :return:
        """
        self.camera.move(- drag_amount[0] / self.drag_sensitivity * self.camera.get_radius(),
                         drag_amount[1] / self.drag_sensitivity * self.camera.get_radius(), 0)

        self.update_programs_world_matrix()
        self.update_programs_view_matrix()
        self.programs["focus"].update_offsets(-self.camera.get_look_at())
        self.glDraw()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        """
        Is called by PyQt5 library when a key is pressed.
        used for detecting the Control button being pressed (showing the cursor) and calling the
        key handler of the gui_module
        :param a0: all key press event data
        :return:
        """
        if a0.key() == QtCore.Qt.Key_Control:
            self.ctrl = True
            self.camera.update_mouse_position(self.mouse_pos)
            self.update_cursor_data()
            self.glDraw()
        if self.keyPressEventHandler is not None:
            self.keyPressEventHandler(a0)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        """
        Is called by PyQt5 library when a key is released.
        used for detecting the Control button being released (hiding the cursor)
        :param a0: all key release event data
        :return:
        """
        if a0.key() == QtCore.Qt.Key_Control:
            self.ctrl = False
            self.update_cursor_data()
            self.glDraw()

    def take_screenshot(self):
        """
        takes a screenshot of the OpenGLWidget. saves it with a random name in the screenshots folder.
        :return:
        """
        GL.glReadBuffer(GL.GL_FRONT)
        pixels = GL.glReadPixels(0, 0, self.width(), self.height(), GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        i = Image.frombytes('RGB', (self.width(), self.height()), pixels, 'raw')
        import os
        if os.path.exists("screenshots") and os.path.isdir("screenshots"):
            i.save("screenshots/screenshot%s.jpg" % str(time.perf_counter_ns()), "JPEG")
        else:
            eprint("\"screenshots\" folder doesn't exist. "
                   "Please create it in the running directory before taking screenshots.")

    def set_background_color(self, color):
        GL.glClearColor(*color, 1.0)
        self.glDraw()
