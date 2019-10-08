from pprint import pprint

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, \
    QLabel, QCheckBox, QWidget, QTabWidget, QSlider, QSizePolicy, QStyle, QStyleFactory
from PyQt5.QtCore import Qt


def define_gui(visualization, world):

    tabbar = QTabWidget()
    tabbar.setMinimumWidth(800)
    tabbar.addTab(sim_tab(visualization), "Simulation")
    tabbar.addTab(vis_tab(visualization), "Visualization")
    set_color(tabbar, QColor(0, 0, 0, 100))

    return tabbar


def sim_tab(visualization):
    tab = QWidget()
    layout = QVBoxLayout()

    #rounds per second slider
    hbox = QHBoxLayout()
    desc = QLabel("rounds per second (%d) : " % visualization.rounds_per_second)
    hbox.addWidget(desc)
    rps_slider = QSlider(Qt.Horizontal)
    rps_slider.setTickInterval(10)
    rps_slider.setTickPosition(2)
    rps_slider.setMaximum(60)
    rps_slider.setMinimum(1)
    rps_slider.setSliderPosition(visualization.rounds_per_second)

    def set_rps():
        visualization.rounds_per_second = rps_slider.value()
        desc.setText("rounds per second (%d): " % rps_slider.value())
    rps_slider.valueChanged.connect(set_rps)

    hbox.addWidget(rps_slider)
    layout.addLayout(hbox)

    #start stop button
    start_stop_button = QPushButton("start")

    def start_stop_sim():
        visualization.running = not visualization.running
        if visualization.running:
            start_stop_button.setText("stop")
        else:
            start_stop_button.setText("start")

    start_stop_button.clicked.connect(start_stop_sim)
    layout.addWidget(start_stop_button)


    tab.setLayout(layout)

    return tab


def vis_tab(visualization):
    tab = QWidget()
    main_layout = QVBoxLayout()

    # fov slider
    fov_layout = QHBoxLayout()
    fov_desc = QLabel("field of view (%d): " % visualization.controller.fov)
    fov_layout.addWidget(fov_desc)
    fov_slider = QSlider(Qt.Horizontal)
    fov_slider.setMinimum(1)
    fov_slider.setMaximum(120)
    fov_slider.setTickInterval(10)
    fov_slider.setTickPosition(2)
    fov_slider.setSliderPosition(50)

    def set_fov():
        visualization.controller.fov = fov_slider.value()
        fov_desc.setText("field of view (%d): " % visualization.controller.fov)
        visualization.controller.update_window()

    fov_slider.valueChanged.connect(set_fov)
    fov_layout.addWidget(fov_slider)

    main_layout.addLayout(fov_layout)

    # projection radio buttons
    projection_layout = QHBoxLayout()
    projection_layout.addWidget(QLabel("projection: "))
    projection_layout.addWidget(QRadioButton("orthografic"))
    persproj = QRadioButton("perspective")

    def change():
        if visualization.controller.projection_type == 'orth':
            visualization.controller.projection_type = 'pers'
        else:
            visualization.controller.projection_type = 'orth'
    persproj.setChecked(True)
    persproj.toggled.connect(change)
    projection_layout.addWidget(persproj)
    main_layout.addLayout(projection_layout)


    tab.setLayout(main_layout)
    return tab

def set_color(widget, color):
    widget.setAutoFillBackground(True)
    p = widget.palette()
    p.setColor(widget.backgroundRole(),color)
    widget.setPalette(p)