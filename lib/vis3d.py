import importlib
import time
from pprint import pprint

from PyQt5 import QtCore
from PyQt5.QtCore import QRect

import gui
import vispy
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout, QSpacerItem
from vispy import app, gloo
from lib.visualization.grid_models import CubicGrid
from lib.visualization.models import ParticleModel, TileModel, MarkerModel
from vispy.util.transforms import perspective, ortho, rotate, translate
from PyQt5.QtWidgets import QSizePolicy
import numpy as np

# important: because of the implementation and the gui module, vispy has to run on pyqt5 backend
app.use_app("pyqt5")
# gl+ = newest openGL version on the system.
vispy.config['gl_backend'] = "gl+"


window_width = 600
window_height = 800
scaling = 1


class Gui(QWidget):
    def __init__(self, visualization):
        super().__init__()
        self.visualization = visualization

        gui_interface = importlib.import_module('gui.' + self.visualization.world.config_data.gui)

        gui_widget = gui_interface.define_gui(self.visualization, self.visualization.world)

        gui_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(gui_widget)
        wrapper_layout.addStretch(0)

        self.visualization.native.setLayout(wrapper_layout)

    def start(self):
        print("starting")
        self.visualization.running = not self.visualization.running


class Controller:
    def __init__(self, visualization):
        self.visualization = visualization
        self.theta = 0
        self.phi = 0
        self.xoffset = 0
        self.yoffset = 0
        self.radius = 10
        self.fov = 50
        self.drag_sensitivity = 1000
        self.rotate_sensitivity = 5
        # orth = orthographic projection, else = perspective
        self.projection_type = 'pers'
        # vispy somehow doesn't catch the closeEvent of PyQt5,
        # so it has to be done over the native interface
        self.visualization.native.closeEvent = self.on_close
        # the rest of the events work fine
        self.visualization.on_mouse_drag = self.on_mouse_drag
        self.visualization.on_mouse_move = self.on_mouse_move
        self.visualization.on_mouse_wheel = self.on_mouse_wheel
        self.visualization.on_resize = self.on_resize
        self.update_window()

    def start(self):
        self.visualization.show()

    def on_mouse_drag(self, delta, buttons):
        if 1 in buttons:
            self.theta -= delta[1] / self.rotate_sensitivity
            self.phi -= delta[0] / self.rotate_sensitivity
            if self.theta > 90:
                self.theta = 90
            if self.theta < -90:
                self.theta = -90
        if 2 in buttons:
            self.xoffset -= delta[0] / self.drag_sensitivity * self.radius
            self.yoffset += delta[1] / self.drag_sensitivity * self.radius
        self.update_window()

    def on_mouse_move(self, event):
        if event.is_dragging and event.last_event.is_dragging:
            self.on_mouse_drag(event.last_event.pos - event.pos, event.buttons)
        self.update_window()

    def on_mouse_wheel(self, event):
        self.radius -= event.delta[1] / 3
        if self.radius < 1:
            self.radius = 1
        self.update_window()

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)
        self.update_window()

    def update_window(self):
        ratio = self.visualization.physical_size[0] / self.visualization.physical_size[1]
        if self.projection_type == 'orth':
            proj = ortho(-self.radius * ratio, self.radius * ratio, -self.radius, self.radius, 0.01, 1000)
        else:
            proj = perspective(self.fov, ratio, 0.01, 1000.0)
        view = np.dot(np.dot(rotate(self.phi, (0, 1, 0)),
                             rotate(self.theta, (1, 0, 0))),
                      translate([self.xoffset, self.yoffset, -self.radius]))
        self.visualization.update_view(proj, view, proj, view)

    def on_close(self, event):
        exit(0)


class Visualization(app.Canvas):
    def __init__(self, world):
        app.Canvas.__init__(self, size=(window_width*scaling, window_height*scaling), title='Simulator', vsync=False)

        gloo.set_state(clear_color=(0.35, 0.35, 0.35, 1.00), depth_test=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'), blend=True, depth_mask=True,
                       cull_face=True)

        self.rounds_per_second = 10
        self.world = world
        self.particle_model = ParticleModel("lib/visualization/models/particle.obj", (1, 0, 0, 1))
        self.tile_model = TileModel("lib/visualization/models/tile.obj",
                                    "lib/visualization/textures/cubic_tile_tex.jpg")
        self.marker_model = MarkerModel("lib/visualization/models/marker.obj", (0, 1, 0, 1))

        self.grid = self.world.grid

        self.running = False
        self.controller = Controller(self)
        self.gui = Gui(self)
        self.controller.start()

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        self.grid.draw_model()

        for p in self.world.particles:
            self.particle_model.translate_model(p.coordinates)
            self.particle_model.draw_model()

        for m in self.world.markers:
            self.marker_model.translate_model(m.coordinates)
            self.marker_model.draw_model()

        for t in self.world.tiles:
            if t.get_tile_status() == True:
                self.tile_model.translate_model((t.coordinates[0]+0.2,
                                                t.coordinates[1]+0.2,
                                                t.coordinates[2]+0.2))
                self.tile_model['scale'] = 0.5
                self.tile_model['model_color'] = (0, 0, 0.3, 1)
                self.tile_model.draw_model()
                self.tile_model['model_color'] = (0, 0, 1, 1)
                self.tile_model['scale'] = 1
            else:
                self.tile_model.translate_model(t.coordinates)
                self.tile_model.draw_model()



        self.particle_model.rotate_light(0.01)
        self.tile_model.rotate_light(0.01)
        self.marker_model.rotate_light(0.01)

    def update_view(self, proj, view, gridproj, gridview):
        self.particle_model['projection'] = proj
        self.particle_model['view'] = view
        self.tile_model['projection'] = proj
        self.tile_model['view'] = view
        self.marker_model['projection'] = proj
        self.marker_model['view'] = view
        self.grid['projection'] = gridproj
        self.grid['view'] = gridview
        self.update()


    def wait_till_running(self):
        while not self.running:
            app.process_events()
            self.update()


    def run(self, round_start_timestamp):

        # waiting until simulation starts
        self.wait_till_running()

        # waiting until enough time passed to do the next simulation round.
        waiting_time = (1 / self.rounds_per_second) / 100
        time_elapsed = time.perf_counter() - round_start_timestamp
        while time_elapsed < 1 / self.rounds_per_second:
            # waiting for 1/100 of the round_time
            time.sleep(waiting_time)
            self.wait_till_running()
            app.process_events()
            self.update()
            time_elapsed = time.perf_counter() - round_start_timestamp

