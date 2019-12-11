from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QColorDialog, QRadioButton, QLabel, QTabWidget,
                             QSlider, QHBoxLayout, QCheckBox, QTabBar, QTextEdit, QLineEdit, QStyle)
from PyQt5.QtCore import Qt
from OpenGL.GL import glGetFloatv, GL_LINE_WIDTH_RANGE
from lib.vis3d import Visualization
from lib.visualization.utils import eprint


def create_slider(tick_interval: int, tick_position: int, max_position: int, min_position: int,
                  slider_position: int, callback, orientation=Qt.Horizontal):
    """
    helper function for creating a slider
    """
    slider = QSlider(orientation)
    slider.setTickInterval(tick_interval)
    slider.setTickPosition(tick_position)
    slider.setMaximum(max_position)
    slider.setMinimum(min_position)
    slider.setSliderPosition(slider_position)
    slider.valueChanged.connect(callback)
    return slider


def create_gui(world, vis: Visualization):

    tabbar = QTabWidget()
    tabbar.setMinimumWidth(200)
    tabbar.addTab(sim_tab(vis, world), "Simulation")
    tabbar.addTab(vis_tab(vis), "Visualization")
    tabbar.addTab(grid_tab(vis), "Grid")
    tabbar.addTab(matter_tab(vis), "Matter")

    return tabbar


def key_handler(key, world, vis):
    if key == Qt.Key_Space:
        vis.start_stop()


def sim_tab(vis, world):
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_rps_slider(vis))

    # start stop button
    start_stop_button = QPushButton("start/stop Simulation")

    def start_stop_sim():
        vis.start_stop()
    start_stop_button.clicked.connect(start_stop_sim)

    # screenshots button
    screenshot_button = QPushButton("take Screenshot")

    def take_screenshot():
        vis.take_screenshot()
    screenshot_button.clicked.connect(take_screenshot)

    # reset button
    reset_button = QPushButton("reset Simulation")

    def reset_sim():
        world.reset()
    reset_button.clicked.connect(reset_sim)

    layout.addWidget(screenshot_button, alignment=Qt.AlignBaseline)
    layout.addWidget(reset_button, alignment=Qt.AlignBaseline)
    layout.addStretch(0)
    layout.addWidget(start_stop_button, alignment=Qt.AlignBaseline)
    tab.setLayout(layout)

    return tab


def get_rps_slider(vis):
    hbox = QVBoxLayout()
    desc = QLabel("rounds per second (%d) : " % vis.get_rounds_per_second())
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_rps(value):
        vis.set_rounds_per_second(value)
        desc.setText("rounds per second (%d) : " % vis.get_rounds_per_second())

    hbox.addWidget(create_slider(10, 2, 60, 1, vis.get_rounds_per_second(), set_rps), alignment=Qt.AlignBaseline)
    return hbox


def vis_tab(vis: Visualization):
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_projection_switch(vis))
    layout.addLayout(get_fov_slider(vis))
    layout.addLayout(get_render_distance_slider(vis))
    layout.addLayout(get_drag_sens_slider(vis))
    layout.addLayout(get_zoom_sens_slider(vis))
    layout.addLayout(get_rota_sens_slider(vis))
    reset_position_button = QPushButton("reset position")
    reset_position_button.clicked.connect(vis.reset_camera_position)
    layout.addWidget(reset_position_button, alignment=Qt.AlignBaseline)
    layout.addStretch(0)
    tab.setLayout(layout)
    return tab


def grid_tab(vis: Visualization):
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_grid_width_slider(vis))
    layout.addLayout(get_grid_lines_scale_slider(vis))
    layout.addLayout(get_grid_locations_scale_slider(vis))
    layout.addLayout(get_show_checkboxes(vis))
    layout.addLayout(recalculate_grid(vis))
    layout.addLayout(get_color_picker(vis))
    layout.addStretch(0)
    tab.setLayout(layout)
    return tab


def matter_tab(vis):
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_particle_scaler(vis))
    layout.addLayout(get_marker_scaler(vis))
    layout.addLayout(get_tile_scaler(vis))
    layout.addStretch(0)
    tab.setLayout(layout)
    return tab


def get_particle_scaler(vis):
    def x_scaler_change(value):
        current_scaling = vis.get_particle_scaling()
        print(current_scaling)
        new_scaling = (value/10.0, current_scaling[1], current_scaling[2])
        print(new_scaling)
        vis.set_particle_scaling(new_scaling)

    def y_scaler_change(value):
        current_scaling = vis.get_particle_scaling()
        new_scaling = (current_scaling[0], value/10.0, current_scaling[2])
        vis.set_particle_scaling(new_scaling)

    def z_scaler_change(value):
        current_scaling = vis.get_particle_scaling()
        new_scaling = (current_scaling[0], current_scaling[1], value/10.0)
        vis.set_particle_scaling(new_scaling)

    x_desc = QLabel("x scale:")
    y_desc = QLabel("y scale:")
    z_desc = QLabel("z scale:")
    x_scaler = create_slider(2, 2, 20, 1, 10, x_scaler_change)
    y_scaler = create_slider(2, 2, 20, 1, 10, y_scaler_change)
    z_scaler = create_slider(2, 2, 20, 1, 10, z_scaler_change)

    hbox1 = QHBoxLayout()
    hbox1.addWidget(x_desc, alignment=Qt.AlignBaseline)
    hbox1.addWidget(x_scaler, alignment=Qt.AlignBaseline)

    hbox2 = QHBoxLayout()
    hbox2.addWidget(y_desc, alignment=Qt.AlignBaseline)
    hbox2.addWidget(y_scaler, alignment=Qt.AlignBaseline)

    hbox3 = QHBoxLayout()
    hbox3.addWidget(z_desc, alignment=Qt.AlignBaseline)
    hbox3.addWidget(z_scaler, alignment=Qt.AlignBaseline)

    vbox = QVBoxLayout()
    vbox.addWidget(QLabel("particle scaling:"), alignment=Qt.AlignBaseline)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox3)

    return vbox


def get_tile_scaler(vis):
    def x_scaler_change(value):
        current_scaling = vis.get_tile_scaling()
        print(current_scaling)
        new_scaling = (value/10.0, current_scaling[1], current_scaling[2])
        print(new_scaling)
        vis.set_tile_scaling(new_scaling)

    def y_scaler_change(value):
        current_scaling = vis.get_tile_scaling()
        new_scaling = (current_scaling[0], value/10.0, current_scaling[2])
        vis.set_tile_scaling(new_scaling)

    def z_scaler_change(value):
        current_scaling = vis.get_tile_scaling()
        new_scaling = (current_scaling[0], current_scaling[1], value/10.0)
        vis.set_tile_scaling(new_scaling)

    x_desc = QLabel("x scale:")
    y_desc = QLabel("y scale:")
    z_desc = QLabel("z scale:")
    x_scaler = create_slider(2, 2, 20, 1, 10, x_scaler_change)
    y_scaler = create_slider(2, 2, 20, 1, 10, y_scaler_change)
    z_scaler = create_slider(2, 2, 20, 1, 10, z_scaler_change)

    hbox1 = QHBoxLayout()
    hbox1.addWidget(x_desc, alignment=Qt.AlignBaseline)
    hbox1.addWidget(x_scaler, alignment=Qt.AlignBaseline)

    hbox2 = QHBoxLayout()
    hbox2.addWidget(y_desc, alignment=Qt.AlignBaseline)
    hbox2.addWidget(y_scaler, alignment=Qt.AlignBaseline)

    hbox3 = QHBoxLayout()
    hbox3.addWidget(z_desc, alignment=Qt.AlignBaseline)
    hbox3.addWidget(z_scaler, alignment=Qt.AlignBaseline)

    vbox = QVBoxLayout()
    vbox.addWidget(QLabel("tile scaling:"), alignment=Qt.AlignBaseline)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox3)

    return vbox


def get_marker_scaler(vis):
    def x_scaler_change(value):
        current_scaling = vis.get_marker_scaling()
        print(current_scaling)
        new_scaling = (value/10.0, current_scaling[1], current_scaling[2])
        print(new_scaling)
        vis.set_marker_scaling(new_scaling)

    def y_scaler_change(value):
        current_scaling = vis.get_marker_scaling()
        new_scaling = (current_scaling[0], value/10.0, current_scaling[2])
        vis.set_marker_scaling(new_scaling)

    def z_scaler_change(value):
        current_scaling = vis.get_marker_scaling()
        new_scaling = (current_scaling[0], current_scaling[1], value/10.0)
        vis.set_marker_scaling(new_scaling)

    x_desc = QLabel("x scale:")
    y_desc = QLabel("y scale:")
    z_desc = QLabel("z scale:")
    x_scaler = create_slider(2, 2, 20, 1, 10, x_scaler_change)
    y_scaler = create_slider(2, 2, 20, 1, 10, y_scaler_change)
    z_scaler = create_slider(2, 2, 20, 1, 10, z_scaler_change)

    hbox1 = QHBoxLayout()
    hbox1.addWidget(x_desc, alignment=Qt.AlignBaseline)
    hbox1.addWidget(x_scaler, alignment=Qt.AlignBaseline)

    hbox2 = QHBoxLayout()
    hbox2.addWidget(y_desc, alignment=Qt.AlignBaseline)
    hbox2.addWidget(y_scaler, alignment=Qt.AlignBaseline)

    hbox3 = QHBoxLayout()
    hbox3.addWidget(z_desc, alignment=Qt.AlignBaseline)
    hbox3.addWidget(z_scaler, alignment=Qt.AlignBaseline)

    vbox = QVBoxLayout()
    vbox.addWidget(QLabel("marker scaling:"), alignment=Qt.AlignBaseline)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox3)

    return vbox

def get_fov_slider(vis: Visualization):
    hbox = QVBoxLayout()
    desc = QLabel("(only for perspective projection)\nfield of view (%d°) : " % vis.get_field_of_view())
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_fov(value):
        vis.set_field_of_view(value)
        desc.setText("(only for perspective projection)\nfield of view (%d°) : " % vis.get_field_of_view())

    hbox.addWidget(create_slider(10, 2, 120, 10, vis.get_field_of_view(), set_fov), alignment=Qt.AlignBaseline)
    return hbox


def get_drag_sens_slider(vis):
    hbox = QVBoxLayout()
    desc = QLabel("drag sensitivity:")
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_ds(value):
        vis.set_drag_sensitivity(5100-value)

    hbox.addWidget(create_slider(500, 2, 5000, 100, 5100-vis.get_drag_sensitivity(), set_ds),
                   alignment=Qt.AlignBaseline)
    return hbox


def get_zoom_sens_slider(vis):
    hbox = QVBoxLayout()
    desc = QLabel("zoom sensitivity:")
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_zs(value):
        vis.set_zoom_sensitivity(1001-value)

    hbox.addWidget(create_slider(100, 2, 1000, 1, 1001-vis.get_zoom_sensitivity(), set_zs), alignment=Qt.AlignBaseline)
    return hbox


def get_rota_sens_slider(vis):
    hbox = QVBoxLayout()
    desc = QLabel("(only for 3D)\nrotation sensitivity:")
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_rs(value):
        vis.set_rotation_sensitivity(11-value)

    hbox.addWidget(create_slider(1, 2, 10, 1, 11-vis.get_rotation_sensitivity(), set_rs), alignment=Qt.AlignBaseline)
    return hbox


def get_projection_switch(vis):
    vbox = QVBoxLayout()
    desc = QLabel("projection type:")
    vbox.addWidget(desc, alignment=Qt.AlignBaseline)

    o = QRadioButton("orthographic")

    def orth_toggle():
        if o.isChecked():
            vis.set_projection_type("ortho")
    o.toggled.connect(orth_toggle)

    p = QRadioButton("perspective")

    if vis.get_projection_type() == "ortho":
        o.setChecked(True)
    else:
        p.setChecked(True)

    def pers_toggle():
        if p.isChecked():
            vis.set_projection_type("perspective")
    p.toggled.connect(pers_toggle)

    hbox = QHBoxLayout()
    hbox.addWidget(o, alignment=Qt.AlignBaseline)
    hbox.addWidget(p, alignment=Qt.AlignBaseline)
    vbox.addLayout(hbox)
    return vbox


def get_color_picker(vis):

    bg_button = QPushButton("background")

    def bg():
        qcd = QColorDialog()
        qcd.setCurrentColor(QColor.fromRgbF(*vis.get_background_color()))
        qcd.exec()
        if qcd.result() == 1:
            vis.set_background_color((qcd.selectedColor().getRgbF()[:3]))

    bg_button.clicked.connect(bg)

    lines_button = QPushButton("grid lines")

    def lines():
        qcd = QColorDialog()
        qcd.setOption(QColorDialog.ShowAlphaChannel)
        qcd.setCurrentColor(QColor.fromRgbF(*vis.get_grid_line_color()))
        qcd.exec()
        if qcd.result() == 1:
            vis.set_grid_line_color((qcd.selectedColor().getRgbF()))

    lines_button.clicked.connect(lines)

    locs_button = QPushButton("grid locations")

    def locs():
        qcd = QColorDialog()
        qcd.setOption(QColorDialog.ShowAlphaChannel)
        qcd.setCurrentColor(QColor.fromRgbF(*vis.get_grid_location_color()))
        qcd.exec()
        if qcd.result() == 1:
            vis.set_grid_location_color((qcd.selectedColor().getRgbF()))

    locs_button.clicked.connect(locs)

    vbox = QVBoxLayout()
    desc = QLabel("change color of:")
    vbox.addWidget(desc, alignment=Qt.AlignBaseline)
    hbox = QHBoxLayout()
    hbox.addWidget(lines_button, alignment=Qt.AlignBaseline)
    hbox.addWidget(locs_button, alignment=Qt.AlignBaseline)
    hbox.addWidget(bg_button, alignment=Qt.AlignBaseline)
    vbox.addLayout(hbox)
    return vbox


def get_grid_width_slider(vis):
    hbox = QVBoxLayout()
    desc = QLabel("grid width (%d):" % vis.get_grid_line_width())
    hbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_gw(value):
        vis.set_grid_line_width(value)
        desc.setText("grid width (%d):" % value)

    hbox.addWidget(create_slider(1, 2, glGetFloatv(GL_LINE_WIDTH_RANGE)[1], 1, vis.get_grid_line_width(), set_gw),
                   alignment=Qt.AlignBaseline)
    return hbox


def get_render_distance_slider(vis):
    vbox = QVBoxLayout()
    desc = QLabel("render distance (%d):" % vis.get_render_distance())
    vbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_mrd(value):
        vis.set_render_distance(value)
        desc.setText("render distance (%d):" % vis.get_render_distance())

    vbox.addWidget(create_slider(10, 2, 5000, 5, vis.get_render_distance(), set_mrd), alignment=Qt.AlignBaseline)
    return vbox


def get_show_checkboxes(vis):

    lines_cb = QCheckBox()
    lines_cb.setText("show lines")
    lines_cb.setChecked(vis.get_show_lines())

    def lines_clicked():
        vis.set_show_lines(lines_cb.isChecked())
    lines_cb.clicked.connect(lines_clicked)

    locs_cb = QCheckBox()
    locs_cb.setText("show locations")
    locs_cb.setChecked(vis.get_show_locations())

    def locs_clicked():
        vis.set_show_locations(locs_cb.isChecked())

    locs_cb.clicked.connect(locs_clicked)

    center_cb = QCheckBox()
    center_cb.setText("show center")
    center_cb.setChecked(vis.get_show_center())

    def center_clicked():
        vis.set_show_center(center_cb.isChecked())

    center_cb.clicked.connect(center_clicked)

    focus_cb = QCheckBox()
    focus_cb.setText("show focus")
    focus_cb.setChecked(vis.get_show_focus())

    def focus_clicked():
        vis.set_show_focus(focus_cb.isChecked())

    focus_cb.clicked.connect(focus_clicked)

    rl_cb = QCheckBox()
    rl_cb.setText("rotate light")
    rl_cb.setChecked(vis.light_rotation)

    def rl_clicked():
        vis.light_rotation = rl_cb.isChecked()

    rl_cb.clicked.connect(rl_clicked)

    hbox1 = QHBoxLayout()
    hbox1.addWidget(lines_cb)
    hbox1.addWidget(locs_cb)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(center_cb)
    hbox2.addWidget(focus_cb)
    hbox3 = QHBoxLayout()
    hbox3.addWidget(rl_cb)

    vbox = QVBoxLayout()
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox3)
    return vbox


def get_grid_lines_scale_slider(vis):
    vbox = QVBoxLayout()
    desc = QLabel("grid lines scale (%d%%):" % int(vis.get_grid_line_scaling()[0]*100))
    vbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_scale(value):
        vis.set_grid_line_scaling([value/50.0, value/50.0, value/50.0])
        desc.setText("grid lines scale (%d%%):" % (int(value*2.0)))

    vbox.addWidget(create_slider(10, 2, 50, 10, int(vis.get_grid_line_scaling()[0]*50), set_scale),
                   alignment=Qt.AlignBaseline)
    return vbox


def get_grid_locations_scale_slider(vis):
    vbox = QVBoxLayout()
    desc = QLabel("grid locations model scale (%d%%):" % int(vis.get_grid_location_scaling()[0]*500))
    vbox.addWidget(desc, alignment=Qt.AlignBaseline)

    def set_scale(value):
        vis.set_grid_location_scaling([value/1000.0, value/1000.0, value/1000.0])
        desc.setText("grid locations model scale (%d%%):" % (int(value/2.0)))

    vbox.addWidget(create_slider(10, 2, 200, 10, int(vis.get_grid_location_scaling()[0]*1000.0), set_scale),
                   alignment=Qt.AlignBaseline)
    return vbox


def recalculate_grid(vis):
    hbox = QHBoxLayout()
    rec_button = QPushButton("update grid with size:")

    size_edit = QLineEdit()
    size_edit.setValidator(QIntValidator())
    size_edit.setText(str(vis._world.grid.size))

    def on_click():
        if size_edit.text().isnumeric():
            vis.recalculate_grid(int(size_edit.text()))
        else:
            eprint("warning: grid size has to be a number")

    rec_button.clicked.connect(on_click)

    hbox.addWidget(rec_button, alignment=Qt.AlignBaseline)
    hbox.addWidget(size_edit, alignment=Qt.AlignBaseline)

    return hbox


