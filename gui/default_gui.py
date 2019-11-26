from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QColorDialog, QRadioButton, QLabel, QWidget, QTabWidget, \
                            QSlider, QHBoxLayout
from PyQt5.QtCore import Qt


def rgba_tuple_to_qcolor(color):
    return QColor(int(color[0]*255),
                  int(color[1]*255),
                  int(color[2]*255),
                  int(color[3]*255))


def qcolor_to_rgba_tuple(qcolor):
    return qcolor.red8() / 255.0, qcolor.green8() / 255.0, qcolor.blue8() / 255.0, qcolor.alpha8() / 255.0


def define_gui(world):

    tabbar = QTabWidget()
    tabbar.setMinimumWidth(100)
    tabbar.addTab(sim_tab(world), "Simulation")
    tabbar.addTab(vis_tab(world), "Visualization")

    return tabbar


def sim_tab(world):
    tab = QWidget()
    layout = QVBoxLayout()
    layout.addLayout(get_rps_slider(world))
    layout.addStretch(0)
    # start stop button
    start_stop_button = QPushButton("start Simulation")

    def start_stop_sim():
        world.vis.running = not world.vis.running
        if world.vis.running:
            start_stop_button.setText("stop Simulation")
        else:
            start_stop_button.setText("start Simulation")

    start_stop_button.clicked.connect(start_stop_sim)
    layout.addWidget(start_stop_button)
    tab.setLayout(layout)

    return tab

def get_rps_slider(world):
    hbox = QVBoxLayout()
    desc = QLabel("rounds per second (%d) : " % world.vis.rounds_per_second)
    hbox.addWidget(desc)
    rps_slider = QSlider(Qt.Horizontal)
    rps_slider.setTickInterval(10)
    rps_slider.setTickPosition(2)
    rps_slider.setMaximum(60)
    rps_slider.setMinimum(1)
    rps_slider.setSliderPosition(world.vis.rounds_per_second)

    def set_rps():
        world.vis.rounds_per_second = rps_slider.value()
        desc.setText("rounds per second (%d) : " % world.vis.rounds_per_second)

    rps_slider.valueChanged.connect(set_rps)

    hbox.addWidget(rps_slider)
    return hbox


def vis_tab(world):
    tab = QWidget()
    layout = QVBoxLayout()
    #layout.addLayout(get_grid_alpha_slider(world))
    layout.addLayout(get_projection_switch(world))
    layout.addLayout(get_fov_slider(world))
    layout.addLayout(get_drag_sens_slider(world))
    layout.addLayout(get_zoom_sens_slider(world))
    layout.addLayout(get_rota_sens_slider(world))
    layout.addLayout(get_color_picker(world))

    layout.addStretch(0)

    reset_position_button = QPushButton("reset position")

    def reset_pos():
        world.vis.viewer.x_offset = 0
        world.vis.viewer.y_offset = 0
        world.vis.viewer.radius = 10
        world.vis.viewer.phi = 0
        world.vis.viewer.theta = 0
        world.vis.viewer.update_view()

    reset_position_button.clicked.connect(reset_pos)
    layout.addWidget(reset_position_button)

    tab.setLayout(layout)
    return tab


def get_fov_slider(world):
    hbox = QVBoxLayout()
    desc = QLabel("(only for perspective projection)\nfield of view (%d°) : " % world.vis.viewer.fov)
    hbox.addWidget(desc)
    fov_slider = QSlider(Qt.Horizontal)
    fov_slider.setTickInterval(10)
    fov_slider.setTickPosition(2)
    fov_slider.setMaximum(120)
    fov_slider.setMinimum(10)
    fov_slider.setSliderPosition(world.vis.viewer.fov)

    def set_fov():
        world.vis.viewer.fov = fov_slider.value()
        desc.setText("(only for perspective projection)\nfield of view (%d°) : " % world.vis.viewer.fov)
        world.vis.viewer.update_view()

    fov_slider.valueChanged.connect(set_fov)

    hbox.addWidget(fov_slider)
    return hbox


def get_drag_sens_slider(world):
    hbox = QVBoxLayout()
    desc = QLabel("drag sensitivity:")
    hbox.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setTickInterval(500)
    slider.setTickPosition(2)
    slider.setMaximum(5000)
    slider.setMinimum(100)
    slider.setSliderPosition(5100-world.vis.viewer.drag_sensitivity)

    def set_fov():
        world.vis.viewer.drag_sensitivity = 5100-slider.value()
        desc.setText("drag sensitivity:")
        world.vis.viewer.update_view()

    slider.valueChanged.connect(set_fov)

    hbox.addWidget(slider)
    return hbox


def get_zoom_sens_slider(world):
    hbox = QVBoxLayout()
    desc = QLabel("zoom sensitivity:")
    hbox.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setTickInterval(100)
    slider.setTickPosition(2)
    slider.setMaximum(1000)
    slider.setMinimum(1)
    slider.setSliderPosition(1001-world.vis.viewer.zoom_sensitivity)

    def set_fov():
        world.vis.viewer.zoom_sensitivity = 1001-slider.value()
        desc.setText("zoom sensitivity:")
        world.vis.viewer.update_view()

    slider.valueChanged.connect(set_fov)

    hbox.addWidget(slider)
    return hbox


def get_rota_sens_slider(world):
    hbox = QVBoxLayout()
    desc = QLabel("(only for 3D)\nrotation sensitivity:")
    hbox.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setTickInterval(1)
    slider.setTickPosition(2)
    slider.setMaximum(10)
    slider.setMinimum(1)
    slider.setSliderPosition(11 - world.vis.viewer.rotate_sensitivity)

    def set_fov():
        world.vis.viewer.rotate_sensitivity = 11 - slider.value()
        desc.setText("(only for 3D)\nrotation sensitivity:")
        world.vis.viewer.update_view()

    slider.valueChanged.connect(set_fov)

    hbox.addWidget(slider)
    return hbox


def get_projection_switch(world):
    vbox = QVBoxLayout()
    desc = QLabel("projection type:")
    vbox.addWidget(desc)

    o = QRadioButton("orthographic")

    def orthotoggle():
        if o.isChecked():
            world.vis.viewer.projection = "ortho"
            world.vis.viewer.update_view()
    o.toggled.connect(orthotoggle)

    p = QRadioButton("perspective")
    p.setChecked(True)

    def perstoggle():
        if p.isChecked():
            world.vis.viewer.projection = "perspective"
            world.vis.viewer.update_view()
    p.toggled.connect(perstoggle)
    hbox = QHBoxLayout()
    hbox.addWidget(o)
    hbox.addWidget(p)
    vbox.addLayout(hbox)
    return vbox

def get_color_picker(world):
    pc_button = QPushButton("particles")
    def pc():
        current = rgba_tuple_to_qcolor(world.vis.viewer.matter_program.particle_color)
        world.vis.viewer.matter_program.particle_color = \
            qcolor_to_rgba_tuple(QColorDialog.getColor(current).rgba64())
        world.vis.viewer.update_view()

    pc_button.clicked.connect(pc)

    tc_button = QPushButton("tiles")

    def tc():
        current = rgba_tuple_to_qcolor(world.vis.viewer.matter_program.tile_color)
        world.vis.viewer.matter_program.tile_color = \
            qcolor_to_rgba_tuple(QColorDialog.getColor(current).rgba64())
        world.vis.viewer.update_view()

    tc_button.clicked.connect(tc)

    mc_button = QPushButton("markers")

    def mc():
        current = rgba_tuple_to_qcolor(world.vis.viewer.matter_program.marker_color)
        world.vis.viewer.matter_program.marker_color = \
            qcolor_to_rgba_tuple(QColorDialog.getColor(current).rgba64())
        world.vis.viewer.update_view()

    mc_button.clicked.connect(mc)

    gr_button = QPushButton("grid")

    def gr():
        current = rgba_tuple_to_qcolor(world.vis.viewer.grid_program.color)
        new = qcolor_to_rgba_tuple(QColorDialog.getColor(current, options=QColorDialog.ShowAlphaChannel).rgba64())
        world.vis.viewer.grid_program.set_color(new)
        world.vis.viewer.update_view()

    gr_button.clicked.connect(gr)

    bg_button = QPushButton("background")

    def bg():
        current = rgba_tuple_to_qcolor(world.vis.viewer.background)
        new = qcolor_to_rgba_tuple(QColorDialog.getColor(current).rgba64())
        world.vis.viewer.set_background(new)
        world.vis.viewer.update_view()

    bg_button.clicked.connect(bg)

    vbox = QVBoxLayout()
    desc = QLabel("change color of:")
    vbox.addWidget(desc)
    hbox1 = QHBoxLayout()
    hbox1.addWidget(pc_button)
    hbox1.addWidget(tc_button)
    hbox1.addWidget(mc_button)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(gr_button)
    hbox2.addWidget(bg_button)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    return vbox