import importlib
from threading import Thread

from PyQt5.QtWidgets import QApplication, QSplitter, QWidget

from lib.swarm_sim_header import eprint
from lib.visualization.OGLWidget import OGLWidget
import time
from lib.visualization.camera import Camera
from lib.visualization.utils import LoadingWindow


def close(_):
    exit(0)


class Visualization:
    def __init__(self, world):
        """
        Main Interface between the OpenGL stuff and the simulator.
        Initializes the camera, and the opengl-widget.
        controlls the speed of the simulation.
        :param world: the world class
        """
        self._world = world
        self._last_light_rotation = 0
        self._rounds_per_second = 10
        self._running = False
        self._app = None
        self._viewer = None
        self._gui = None
        self._splitter = None
        self.light_rotation = True

        # create the QApplication
        self._app = QApplication([])

        # create camera for the visualization
        # if grid is 2D, set to ortho (ortho is better for 2D)
        if self._world.grid.get_dimension_count() == 2:
            self._camera = Camera(self._world.config_data.window_size_x, self._world.config_data.window_size_y,
                                  self._world.config_data.look_at, self._world.config_data.phi,
                                  self._world.config_data.theta, self._world.config_data.radius,
                                  self._world.config_data.fov, self._world.config_data.cursor_offset,
                                  self._world.config_data.render_distance, "ortho", self._world.grid.get_scaling())
        else:
            self._camera = Camera(self._world.config_data.window_size_x, self._world.config_data.window_size_y,
                                  self._world.config_data.look_at, self._world.config_data.phi,
                                  self._world.config_data.theta, self._world.config_data.radius,
                                  self._world.config_data.fov, self._world.config_data.cursor_offset,
                                  self._world.config_data.render_distance,
                                  "perspective", self._world.grid.get_scaling())

        # create the opengl widget
        self._viewer = OGLWidget(self._world, self._camera)
        self._viewer.glInit()

        # create and show the main Window
        self._splitter = QSplitter()
        self._splitter.closeEvent = close
        self._splitter.setMinimumWidth(self._world.config_data.window_size_x)
        self._splitter.setMinimumHeight(self._world.config_data.window_size_y)
        self._splitter.setWindowTitle("Simulator")

        self._splitter.show()

        # create gui
        # creating the gui has to happen after showing the window, so the gui can access
        # opengl variables and programs during creation
        gui_module = importlib.import_module('gui.' + self._world.config_data.gui)

        # the key press handler
        def key_press_event(event):
            gui_module.key_handler(event.key(), self._world, self)

        # loading key handler from gui module
        if "key_handler" in dir(gui_module):
            self._viewer.keyPressEventHandler = key_press_event
            self._splitter.keyPressEvent = key_press_event
        else:
            eprint("Warning: no key_handler in gui module => no key handler added.")

        # loading gui from gui module
        if "create_gui" in dir(gui_module):
            self._gui = gui_module.create_gui(self._world, self)
            if self._gui is not None and issubclass(self._gui.__class__, QWidget):
                self._splitter.addWidget(self._gui)
                self._splitter.keyPressEvent = self._viewer.keyPressEvent
                self._splitter.keyReleaseEvent = self._viewer.keyReleaseEvent
                self._splitter.addWidget(self._viewer)
                self._splitter.setSizes(
                    [self._world.config_data.window_size_x * 0.25, self._world.config_data.window_size_x * 0.75])
            else:
                eprint("warning: create_gui in gui module didn't return a QWidget. expected subclass of QWidget, "
                       "but got %s => no gui added." % self._gui.__class__.__name__)
                self._splitter.addWidget(self._viewer)

        else:
            eprint("warning: no create_gui in gui module => no gui added.")
            self._splitter.addWidget(self._viewer)

    def reset(self):
        """
        stops the simulation.
        deletes all data in the visualization.
        resets the camera
        :return:
        """
        self._running = False
        self._viewer.particle_offset_data = {}
        self._viewer.particle_update_flag = True
        self._viewer.tile_offset_data = {}
        self._viewer.tile_update_flag = True
        self._viewer.location_offset_data = {}
        self._viewer.location_update_flag = True
        self._viewer.update_data()
        self._camera.reset()
        self._viewer.update_scene()

    def wait_for_thread(self, thread: Thread, window_message, window_title):
        """
        executes a thread and shows a loading window till the thread stops.
        blocks the gui, while thread runs.
        :param thread: the thread
        :param window_message: the displayed message
        :param window_title: the title of the loading window
        :return:
        """

        loading_window = LoadingWindow(window_message, window_title)
        if self._gui is not None and issubclass(self._gui.__class__, QWidget):
            self._gui.setDisabled(True)
        thread.start()
        while thread.is_alive():
            self._app.processEvents()
        thread.join()
        loading_window.close()
        self._gui.setDisabled(False)

    def rotate_light(self):
        """
        rotates the light direction at a steady degrees/second velocity independent of the CPU-clock or framerate.
        :return:
        """
        # rotation of light only in 3d
        if self._world.grid.get_dimension_count() > 2:
            # 20° per second rotation
            if self._last_light_rotation == 0:
                self._last_light_rotation = time.perf_counter()
            else:
                angle = (time.perf_counter() - self._last_light_rotation) * 20
                self._last_light_rotation = time.perf_counter()
                self._viewer.rotate_light(angle)
                self._viewer.glDraw()

    def start_stop(self):
        """
        starts and pauses the simulation
        :return:
        """
        self._running = not self._running

    def _wait_while_not_running(self):
        """
        helper function.
        waits until the running flag is set.
        :return:
        """
        sleep_time = 1.0 / 120.0
        self._app.processEvents()
        if self.light_rotation:
            self.rotate_light()
        while not self._running:
            # sleeping for 1/120 secs, for responsive GUI
            time.sleep(sleep_time)
            if self.light_rotation:
                self.rotate_light()
            self._app.processEvents()

    def run(self, round_start_timestamp):
        """
        main function for running the simulation with the visualization.
        Controlls the waiting time, so the rounds_per_second value is being kept.
        :param round_start_timestamp: timestamp of the start of the round.
        :return:
        """
        # draw scene
        self._viewer.update_data()
        self._viewer.glDraw()
        # waiting until simulation starts
        self._wait_while_not_running()
        # waiting until enough time passed to do the next simulation round.
        time_elapsed = time.perf_counter() - round_start_timestamp
        # sleeping time - max 1/120 for a responsive GUI
        sleep_time = min(1.0 / 120, (1.0 / self._rounds_per_second) / 10.0)
        while time_elapsed < 1 / self._rounds_per_second:
            # waiting for 1/100 of the round_time
            time.sleep(sleep_time)
            # check if still running... if not wait (important for low rounds_per_second values)
            self._wait_while_not_running()
            time_elapsed = time.perf_counter() - round_start_timestamp

    def remove_particle(self, particle):
        """
        removes a particle from the visualization.
        it wont be deleted immediately! not until the next round.
        if you want an immediate deletion of the particle, then call this function, then, update_data and after that
        glDraw of the OpenGLWidget.

        :param particle: the particle (not the id, the instance) to be deleted
        :return:
        """
        self._viewer.particle_update_flag = True
        if particle in self._viewer.particle_offset_data:
            del self._viewer.particle_offset_data[particle]

    def particle_changed(self, particle):
        """
        updates the offset, color and carry data of the particle in the visualization.
        it wont be an immediate update. it will update in the beginning of the next "run" call / after current round.
        :param particle: the particle that has changed (the instance)
        :return:
        """
        self._viewer.particle_update_flag = True
        self._viewer.particle_offset_data[particle] = (particle.coordinates, particle.color,
                                                       1.0 if particle.get_carried_status() else 0.0)

    def remove_tile(self, tile):
        """
        removes a tile from the visualization.
        :param tile: the tile (not the id, the instance) to be deleted
        :return:
        """
        self._viewer.tile_update_flag = True
        if tile in self._viewer.tile_offset_data:
            del self._viewer.tile_offset_data[tile]

    def tile_changed(self, tile):
        """
        updates the offset, color and carry data of the tile in the visualization.
        :param tile: the tile ( not the id, the instance) to be deleted
        :return:
        """
        self._viewer.tile_update_flag = True
        self._viewer.tile_offset_data[tile] = (tile.coordinates, tile.color, 1.0 if tile.get_tile_status() else 0.0)

    def remove_location(self, location):
        """
        removes a location from the visualization.
        :param location: the location (not the id, the instance) to be deleted
        :return:
        """
        self._viewer.location_update_flag = True
        if location in self._viewer.location_offset_data:
            del self._viewer.location_offset_data[location]

    def location_changed(self, location):
        """
        updates the offset and color data of the location in the visualization.
        :param location: the location ( not the id, the instance) to be deleted
        :return:
        """
        self._viewer.location_update_flag = True
        self._viewer.location_offset_data[location] = (location.coordinates, location.color)

    def update_visualization_data(self):
        self._viewer.update_data()

    # setters and getters for various variables in the visualization

    def set_rounds_per_second(self, rounds_per_second):
        self._rounds_per_second = rounds_per_second

    def get_rounds_per_second(self):
        return self._rounds_per_second

    def reset_camera_position(self):
        self._camera.reset()
        self._viewer.update_scene()

    def set_field_of_view(self, fov: float):
        self._camera.set_fov(fov)
        self._viewer.update_programs_projection_matrix()
        self._viewer.update_cursor_data()
        self._viewer.glDraw()

    def get_field_of_view(self):
        return self._camera.get_fov()

    def set_drag_sensitivity(self, s: float):
        self._viewer.drag_sensitivity = s

    def get_drag_sensitivity(self):
        return self._viewer.drag_sensitivity

    def set_zoom_sensitivity(self, s: float):
        self._viewer.zoom_sensitivity = s

    def get_zoom_sensitivity(self):
        return self._viewer.zoom_sensitivity

    def set_rotation_sensitivity(self, s: float):
        self._viewer.rotation_sensitivity = s

    def get_rotation_sensitivity(self):
        return self._viewer.rotation_sensitivity

    def get_projection_type(self):
        return self._camera.get_projection_type()

    def set_projection_type(self, projection_type):
        self._camera.set_projection_type(projection_type)
        self._viewer.update_programs_projection_matrix()
        self._viewer.glDraw()

    def get_background_color(self):
        return self._viewer.background

    def set_background_color(self, color):
        self._viewer.set_background_color(color)

    def get_grid_line_color(self):
        return self._viewer.programs["grid"].get_line_color()

    def set_grid_line_color(self, color):
        self._viewer.programs["grid"].set_line_color(color)

    def get_grid_line_width(self):
        return self._viewer.programs["grid"].width

    def set_grid_line_width(self, width):
        self._viewer.programs["grid"].set_width(width)
        self._viewer.glDraw()

    def get_grid_line_scaling(self):
        return self._viewer.programs["grid"].get_line_scaling()

    def set_grid_line_scaling(self, scaling):
        self._viewer.programs["grid"].set_line_scaling(scaling)
        self._viewer.glDraw()

    def get_grid_coordinates_color(self):
        return self._viewer.programs["grid"].get_model_color()

    def set_grid_coordinates_color(self, color):
        self._viewer.programs["grid"].set_model_color(color)
        self._viewer.glDraw()

    def get_grid_coordinates_scaling(self):
        return self._viewer.programs["grid"].get_model_scaling()

    def set_grid_coordinates_scaling(self, scaling):
        print(2)
        self._viewer.programs["grid"].set_model_scaling(scaling)
        print(2)
        self._viewer.glDraw()

    def get_render_distance(self):
        return self._camera.get_render_distance()

    def set_render_distance(self, render_distance):
        self._camera.set_render_distance(render_distance)
        self._viewer.update_programs_projection_matrix()
        self._viewer.glDraw()

    def get_show_lines(self):
        return self._viewer.programs["grid"].show_lines

    def set_show_lines(self, show_lines: bool):
        self._viewer.programs["grid"].show_lines = show_lines
        self._viewer.glDraw()

    def get_show_coordinates(self):
        return self._viewer.programs["grid"].show_coordinates

    def set_show_coordinates(self, show_coordinates: bool):
        self._viewer.programs["grid"].show_coordinates = show_coordinates
        self._viewer.glDraw()

    def get_show_center(self):
        return self._viewer.show_center

    def set_show_center(self, show_center: bool):
        self._viewer.show_center = show_center

    def get_show_focus(self):
        return self._viewer.show_focus

    def set_show_focus(self, show_focus: bool):
        self._viewer.show_focus = show_focus

    def take_screenshot(self):
        self._viewer.take_screenshot()

    def recalculate_grid(self, size):
        self._viewer.programs["grid"].update_offsets(self._world.grid.get_box(size))
        self._viewer.glDraw()

    def get_particle_scaling(self):
        return self._viewer.programs["particle"].get_model_scaling()

    def set_particle_scaling(self, scaling):
        self._viewer.programs["particle"].set_model_scaling(scaling)

    def get_tile_scaling(self):
        return self._viewer.programs["tile"].get_model_scaling()

    def set_tile_scaling(self, scaling):
        self._viewer.programs["tile"].set_model_scaling(scaling)

    def get_location_scaling(self):
        return self._viewer.programs["location"].get_model_scaling()

    def set_location_scaling(self, scaling):
        self._viewer.programs["location"].set_model_scaling(scaling)