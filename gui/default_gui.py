from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QColorDialog, QRadioButton, QLabel, QTabWidget,
                             QSlider, QHBoxLayout, QCheckBox, QTabBar, QLineEdit, QGroupBox, QComboBox, QStyle)
from PyQt5.QtCore import Qt

from lib.visualization.utils import show_msg

start_stop_button = None
world = None
vis = None
simtab = None


def create_gui(w, v):
    global world, vis, simtab
    world = w
    vis = v
    tabbar = QTabWidget()
    tabbar.setMinimumWidth(200)
    simtab = sim_tab()
    tabbar.addTab(simtab, "Simulation")
    tabbar.addTab(vis_tab(), "Visualization")
    tabbar.addTab(grid_tab(), "Grid")
    tabbar.addTab(matter_tab(), "Matter")
    tabbar.addTab(help_tab(), "Help")
    return tabbar


def set_disable_sim(disable_flag):
    global simtab
    simtab.setDisabled(disable_flag)


def key_handler(key, w, v):
    if key == Qt.Key_Space:
        start_stop_button.click()


def help_tab():
    vcontrols = QLabel("view controls:")
    lmd = QLabel("\tmouse dragging with left mouse button:\n\t\trotation (only in 3D)")
    rmd = QLabel("\tmouse dragging with right mouse button:\n\t\tdragging the view")
    mw = QLabel("\tscrolling:\n\t\tzooming")
    ccontrols = QLabel("\ncursor controls:")
    sc = QLabel("\tholding 'CTRL':\n\t\tshow cursor")
    mcc = QLabel("\tleft mouse button click while holding 'CTRL':\n\t\tadding/removing matter at cursors position")
    mwc = QLabel("\tscrolling while holding 'CTRL':\n\t\tmoving the cursor in the relative z-direction")
    scontrols = QLabel("\nsimulation controls:")
    sss = QLabel("\tspacebar:\n\t\tstart / stop the simulation")
    vbox = QVBoxLayout()
    vbox.addWidget(vcontrols)
    vbox.addWidget(lmd)
    vbox.addWidget(rmd)
    vbox.addWidget(mw)
    vbox.addWidget(ccontrols)
    vbox.addWidget(sc)
    vbox.addWidget(mcc)
    vbox.addWidget(mwc)
    vbox.addWidget(scontrols)
    vbox.addWidget(sss)
    vbox.addStretch(0)
    tabbar = QTabBar()
    tabbar.setLayout(vbox)

    return tabbar


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


def sim_tab():
    tab = QTabBar()
    layout = QVBoxLayout()
    global start_stop_button
    # start stop button

    start_stop_button = QPushButton("start Simulation")
    start_stop_button.setIcon(start_stop_button.style().standardIcon(QStyle.SP_MediaPlay))
    start_stop_button.setStyleSheet("font-weight:bold;")
    status = QLabel("Simulation not running")
    status.setStyleSheet("font-weight:bold;color:#bb4444;")

    def start_stop_sim():
        vis.start_stop()
        if vis.is_running():
            status.setText("Simulation running")
            status.setStyleSheet("font-weight:bold;color:#44bb44;")
            start_stop_button.setText("pause Simulation")
            start_stop_button.setIcon(start_stop_button.style().standardIcon(QStyle.SP_MediaPause))
        else:
            status.setText("Simulation paused")
            status.setStyleSheet("font-weight:bold;color:#4444bb;")
            start_stop_button.setText("unpause Simulation")
            start_stop_button.setIcon(start_stop_button.style().standardIcon(QStyle.SP_MediaPlay))

    start_stop_button.clicked.connect(start_stop_sim)

    # screenshot buttons
    quick_screenshot = QPushButton("quick")
    save_as_screenshot = QPushButton("save as")

    def qs():
        vis.take_screenshot(True)

    def sas():
        vis.take_screenshot(False)

    quick_screenshot.clicked.connect(qs)
    save_as_screenshot.clicked.connect(sas)

    # WARNING: VECTOR SCREENSHOTS ONLY FOR TRIANGULARGRID IMPLEMENTED!
    vector_screenshot = QPushButton("export as vector graphics (svg)")
    def eas():
        vis.take_vector_screenshot()
    vector_screenshot.clicked.connect(eas)
    screenshot_buttons = QHBoxLayout()
    screenshot_buttons.addWidget(quick_screenshot)
    screenshot_buttons.addWidget(save_as_screenshot)
    vbox = QVBoxLayout()
    vbox.addLayout(screenshot_buttons)
    vbox.addWidget(vector_screenshot)
    screenshot_box = QGroupBox("screenshot")
    screenshot_box.setLayout(vbox)


    # recording buttons
    start_recording_button = QPushButton("start")
    del_recording_button = QPushButton("delete")
    export_recording_button = QPushButton("export")

    hbox = QHBoxLayout()
    hbox.addWidget(start_recording_button)
    hbox.addWidget(del_recording_button)
    hbox.addWidget(export_recording_button)
    recording_box = QGroupBox("Recording")
    recording_box.setLayout(hbox)

    def startstoprec():
        if vis.is_recording():
            start_recording_button.setText("start")
            recording_box.setTitle("recording")
            if vis.is_running():
                start_stop_sim()
            vis.stop_recording()
        else:
            recording_box.setTitle("Recording (running)")
            start_recording_button.setText("stop")
            vis.start_recording()
    start_recording_button.clicked.connect(startstoprec)

    def del_rec():
        if vis.is_recording():
            startstoprec()
        vis.delete_recording()
    del_recording_button.clicked.connect(del_rec)
    export_recording_button.clicked.connect(vis.export_recording)

    reset_button = QPushButton("reset Simulation")

    def reset_sim():
        world.reset()
        start_stop_button.setText("start Simulation")
        start_stop_button.setIcon(start_stop_button.style().standardIcon(QStyle.SP_MediaPlay))
        status.setText("Simulation not running")
        status.setStyleSheet("font-weight:bold;color:#bb4444;")

    reset_button.clicked.connect(reset_sim)

    quick_scenario_button = QPushButton("quick")
    save_as_scenario_button = QPushButton("save as")

    def qs_scenario(): world.save_scenario(True)
    def sas_scenario(): world.save_scenario(False)

    quick_scenario_button.clicked.connect(qs_scenario)
    save_as_scenario_button.clicked.connect(sas_scenario)
    scenario_buttons = QHBoxLayout()
    scenario_buttons.addWidget(quick_scenario_button)
    scenario_buttons.addWidget(save_as_scenario_button)
    scenario_box = QGroupBox("scenario")
    scenario_box.setLayout(scenario_buttons)

    sim_box = QGroupBox("main controls")
    vbox = QVBoxLayout()
    vbox.addWidget(status)
    vbox.addWidget(start_stop_button)
    vbox.addLayout(get_rps_slider())
    vbox.addWidget(reset_button)
    sim_box.setLayout(vbox)
    layout.addWidget(sim_box)
    layout.addWidget(screenshot_box)
    layout.addWidget(scenario_box)
    layout.addWidget(recording_box)

    new_matter_box = QGroupBox("new matter")
    vbox = QVBoxLayout()
    vbox.addLayout(get_matter_radios())
    vbox.addWidget(get_new_matter_color_picker())
    new_matter_box.setLayout(vbox)
    layout.addWidget(new_matter_box)

    layout.addStretch(0)
    tab.setLayout(layout)

    return tab


def get_new_matter_color_picker():
    cp_button = QPushButton("change color of new matter")

    def cp():
        cd = QColorDialog()
        cd.setCurrentColor(QColor.fromRgbF(*vis.get_added_matter_color()))
        cd.exec()
        if cd.result() == 1:
            vis.set_added_matter_color((cd.selectedColor().getRgbF()))
    cp_button.clicked.connect(cp)
    return cp_button


def get_matter_radios():
    p_radio = QRadioButton("particle")
    p_radio.setChecked(False)
    t_radio = QRadioButton("tile")
    t_radio.setChecked(True)
    l_radio = QRadioButton("location")
    l_radio.setChecked(False)

    def on_toggle():
        if p_radio.isChecked():
            vis.set_on_cursor_click_matter_type("particle")

        if t_radio.isChecked():
            vis.set_on_cursor_click_matter_type("tile")

        if l_radio.isChecked():
            vis.set_on_cursor_click_matter_type("location")

    p_radio.toggled.connect(on_toggle)
    t_radio.toggled.connect(on_toggle)
    l_radio.toggled.connect(on_toggle)

    vbox = QVBoxLayout()
    vbox.addWidget(p_radio)
    vbox.addWidget(t_radio)
    vbox.addWidget(l_radio)

    return vbox


def get_rps_slider():
    hbox = QVBoxLayout()
    desc = QLabel("rounds per second (%d) : " % vis.get_rounds_per_second())
    hbox.addWidget(desc)

    def set_rps(value):
        vis.set_rounds_per_second(value)
        desc.setText("rounds per second (%d) : " % vis.get_rounds_per_second())

    hbox.addWidget(create_slider(10, 2, 120, 1, vis.get_rounds_per_second(), set_rps))
    return hbox


def vis_tab():
    tab = QTabBar()
    layout = QVBoxLayout()
    proj_box = QGroupBox("projection settings")
    vbox = QVBoxLayout()
    vbox.addLayout(get_projection_switch())
    vbox.addLayout(get_fov_slider())
    vbox.addLayout(get_render_distance_slider())
    proj_box.setLayout(vbox)
    layout.addWidget(proj_box)
    sens_slider_box = QGroupBox("control sensitivity")
    vbox = QVBoxLayout()
    vbox.addLayout(get_drag_sens_slider())
    vbox.addLayout(get_zoom_sens_slider())
    vbox.addLayout(get_rota_sens_slider())
    sens_slider_box.setLayout(vbox)
    layout.addWidget(sens_slider_box)

    misc_box = QGroupBox("miscellaneous")
    vbox = QVBoxLayout()
    vbox.addLayout(get_antialiasing_combobox())
    vbox.addLayout(get_vis_show_checkboxes())
    reset_position_button = QPushButton("reset camera position")
    reset_position_button.clicked.connect(vis.reset_camera_position)
    vbox.addWidget(reset_position_button)
    misc_box.setLayout(vbox)
    layout.addWidget(misc_box)
    layout.addStretch(0)
    tab.setLayout(layout)
    return tab


def grid_tab():
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_grid_lines_scale_slider())
    layout.addLayout(get_grid_coordinates_scale_slider())
    layout.addLayout(get_show_checkboxes())
    layout.addLayout(recalculate_grid())
    layout.addLayout(get_color_picker())
    layout.addStretch(0)
    tab.setLayout(layout)
    return tab


def matter_tab():
    tab = QTabBar()
    layout = QVBoxLayout()
    layout.addLayout(get_scaler("particle"))
    layout.addLayout(get_scaler("tile"))
    layout.addLayout(get_scaler("location"))
    layout.addStretch(1)
    tab.setLayout(layout)
    return tab


def get_scaler(mattertype):
    if mattertype == "particle":
        current_scaling = vis.get_particle_scaling()

        def x_scaler_change(value):
            cs = vis.get_particle_scaling()
            new_scaling = (value/10.0, cs[1], cs[2])
            vis.set_particle_scaling(new_scaling)

        def y_scaler_change(value):
            cs = vis.get_particle_scaling()
            new_scaling = (cs[0], value/10.0, cs[2])
            vis.set_particle_scaling(new_scaling)

        def z_scaler_change(value):
            cs = vis.get_particle_scaling()
            new_scaling = (cs[0], cs[1], value/10.0)
            vis.set_particle_scaling(new_scaling)
    elif mattertype == "tile":
        current_scaling = vis.get_tile_scaling()

        def x_scaler_change(value):
            cs = vis.get_tile_scaling()
            new_scaling = (value / 10.0, cs[1], cs[2])
            vis.set_tile_scaling(new_scaling)

        def y_scaler_change(value):
            cs = vis.get_tile_scaling()
            new_scaling = (cs[0], value / 10.0, cs[2])
            vis.set_tile_scaling(new_scaling)

        def z_scaler_change(value):
            cs = vis.get_tile_scaling()
            new_scaling = (cs[0], cs[1], value / 10.0)
            vis.set_tile_scaling(new_scaling)
    else:
        current_scaling = vis.get_location_scaling()

        def x_scaler_change(value):
            cs = vis.get_location_scaling()
            new_scaling = (value / 10.0, cs[1], cs[2])
            vis.set_location_scaling(new_scaling)

        def y_scaler_change(value):
            cs = vis.get_location_scaling()
            new_scaling = (cs[0], value / 10.0, cs[2])
            vis.set_location_scaling(new_scaling)

        def z_scaler_change(value):
            cs = vis.get_location_scaling()
            new_scaling = (cs[0], cs[1], value / 10.0)
            vis.set_location_scaling(new_scaling)

    x_desc = QLabel("x scale:")
    y_desc = QLabel("y scale:")
    z_desc = QLabel("z scale:")
    x_scaler = create_slider(2, 2, 20, 1, current_scaling[0]*10, x_scaler_change)
    y_scaler = create_slider(2, 2, 20, 1, current_scaling[0]*10, y_scaler_change)
    z_scaler = create_slider(2, 2, 20, 1, current_scaling[0]*10, z_scaler_change)

    hbox1 = QHBoxLayout()
    hbox1.addWidget(x_desc)
    hbox1.addWidget(x_scaler)

    hbox2 = QHBoxLayout()
    hbox2.addWidget(y_desc)
    hbox2.addWidget(y_scaler)

    hbox3 = QHBoxLayout()
    hbox3.addWidget(z_desc)
    hbox3.addWidget(z_scaler)

    vbox = QVBoxLayout()
    vbox.addWidget(QLabel("%s scaling:" % mattertype))
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox3)

    return vbox


def get_fov_slider():
    hbox = QVBoxLayout()
    desc = QLabel("(only for perspective projection)\nfield of view (%d°) : " % vis.get_field_of_view())
    hbox.addWidget(desc)

    def set_fov(value):
        vis.set_field_of_view(value)
        desc.setText("(only for perspective projection)\nfield of view (%d°) : " % vis.get_field_of_view())

    hbox.addWidget(create_slider(10, 2, 120, 10, vis.get_field_of_view(), set_fov))
    return hbox


def get_drag_sens_slider():
    hbox = QHBoxLayout()
    desc = QLabel("drag:")
    hbox.addWidget(desc)

    def set_ds(value):
        vis.set_drag_sensitivity(5100-value)

    hbox.addWidget(create_slider(500, 2, 5000, 100, 5100-vis.get_drag_sensitivity(), set_ds),
                   alignment=Qt.AlignBaseline)
    return hbox


def get_zoom_sens_slider():
    hbox = QHBoxLayout()
    desc = QLabel("zoom:")
    hbox.addWidget(desc)

    def set_zs(value):
        vis.set_zoom_sensitivity(1001-value)

    hbox.addWidget(create_slider(100, 2, 1000, 1, 1001-vis.get_zoom_sensitivity(), set_zs))
    return hbox


def get_rota_sens_slider():
    hbox = QHBoxLayout()
    desc = QLabel("(only 3D)\nrotation:")
    hbox.addWidget(desc)

    def set_rs(value):
        vis.set_rotation_sensitivity(11-value)

    hbox.addWidget(create_slider(1, 2, 10, 1, 11-vis.get_rotation_sensitivity(), set_rs))
    return hbox


def get_projection_switch():
    vbox = QVBoxLayout()
    desc = QLabel("projection type:")
    vbox.addWidget(desc)

    o = QRadioButton("orthographic")

    def orth_toggle():
        if o.isChecked():
            vis.set_projection_type("ortho")

    p = QRadioButton("perspective")

    def pers_toggle():
        if p.isChecked():
            vis.set_projection_type("perspective")

    if vis.get_projection_type() == "ortho":
        o.setChecked(True)
    else:
        p.setChecked(True)

    o.toggled.connect(orth_toggle)
    p.toggled.connect(pers_toggle)

    hbox = QHBoxLayout()
    hbox.addWidget(o)
    hbox.addWidget(p)
    vbox.addLayout(hbox)
    return vbox


def get_color_picker():

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

    locs_button = QPushButton("grid coordinates")

    def locs():
        qcd = QColorDialog()
        qcd.setOption(QColorDialog.ShowAlphaChannel)
        qcd.setCurrentColor(QColor.fromRgbF(*vis.get_grid_coordinates_color()))
        qcd.exec()
        if qcd.result() == 1:
            vis.set_grid_coordinates_color((qcd.selectedColor().getRgbF()))

    locs_button.clicked.connect(locs)

    brd_button = QPushButton("grid border")

    def brd():
        qcd = QColorDialog()
        qcd.setOption(QColorDialog.ShowAlphaChannel)
        qcd.setCurrentColor(QColor.fromRgbF(*vis.get_grid_border_color()))
        qcd.exec()
        if qcd.result() == 1:
            vis.set_grid_border_color((qcd.selectedColor().getRgbF()))

    brd_button.clicked.connect(brd)

    vbox = QVBoxLayout()
    desc = QLabel("change color of:")
    vbox.addWidget(desc)
    hbox1 = QHBoxLayout()
    hbox1.addWidget(lines_button)
    hbox1.addWidget(locs_button)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(bg_button)
    hbox2.addWidget(brd_button)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox2)
    return vbox


def get_render_distance_slider():
    vbox = QVBoxLayout()
    desc = QLabel("render distance (%d):" % vis.get_render_distance())
    vbox.addWidget(desc)

    def set_mrd(value):
        vis.set_render_distance(value)
        desc.setText("render distance (%d):" % vis.get_render_distance())

    vbox.addWidget(create_slider(500, 2, 5000, 5, vis.get_render_distance(), set_mrd))
    return vbox


def get_vis_show_checkboxes():
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

    vbox = QVBoxLayout()
    vbox.addWidget(center_cb)
    vbox.addWidget(focus_cb)
    vbox.addWidget(rl_cb)
    return vbox


def get_show_checkboxes():

    lines_cb = QCheckBox()
    lines_cb.setText("show lines")
    lines_cb.setChecked(vis.get_show_lines())

    def lines_clicked():
        vis.set_show_lines(lines_cb.isChecked())
    lines_cb.clicked.connect(lines_clicked)

    coords_cb = QCheckBox()
    coords_cb.setText("show coordinates")
    coords_cb.setChecked(vis.get_show_coordinates())

    def coords_clicked():
        vis.set_show_coordinates(coords_cb.isChecked())

    coords_cb.clicked.connect(coords_clicked)

    hbox = QHBoxLayout()
    hbox.addWidget(lines_cb)
    hbox.addWidget(coords_cb)
    if world.config_data.border:
        border_cb = QCheckBox()
        border_cb.setText("show border")
        border_cb.setChecked(vis.get_show_border())

        def border_clicked():
            vis.set_show_border(border_cb.isChecked())

        border_cb.clicked.connect(border_clicked)
        hbox.addWidget(border_cb)

    return hbox


def get_grid_lines_scale_slider():
    vbox = QVBoxLayout()
    desc = QLabel("grid lines scale (%d%%):" % int(vis.get_grid_line_scaling()[0]*100))
    vbox.addWidget(desc)

    def set_scale(value):
        vis.set_grid_line_scaling([value/50.0, value/50.0, value/50.0])
        desc.setText("grid lines scale (%d%%):" % (int(value*2.0)))

    vbox.addWidget(create_slider(10, 2, 50, 10, int(vis.get_grid_line_scaling()[0]*50), set_scale),
                   alignment=Qt.AlignBaseline)
    return vbox


def get_grid_coordinates_scale_slider():
    vbox = QVBoxLayout()
    desc = QLabel("grid coordinates model scale (%d%%):" % int(vis.get_grid_coordinates_scaling()[0]*500))
    vbox.addWidget(desc)

    def set_scale(value):
        vis.set_grid_coordinates_scaling([value/1000.0, value/1000.0, value/1000.0])
        desc.setText("grid coordinates model scale (%d%%):" % (int(value/2.0)))

    vbox.addWidget(create_slider(10, 2, 200, 10, int(vis.get_grid_coordinates_scaling()[0]*1000.0), set_scale),
                   alignment=Qt.AlignBaseline)
    return vbox


def recalculate_grid():
    hbox = QHBoxLayout()
    rec_button = QPushButton("update grid with size:")

    size_edit = QLineEdit()
    size_edit.setValidator(QIntValidator())
    size_edit.setText(str(world.grid.size))

    def on_click():
        if size_edit.text().isnumeric():
            vis.recalculate_grid(int(size_edit.text()))
        else:
            show_msg("Grid size has to be a number.", 2)

    rec_button.clicked.connect(on_click)

    hbox.addWidget(rec_button)
    hbox.addWidget(size_edit)

    return hbox


def get_antialiasing_combobox():
    hbox = QHBoxLayout()
    combo = QComboBox()
    combo.addItem("disabled", 0)
    combo.addItem("2 samples", 2)
    combo.addItem("4 samples", 4)
    combo.addItem("8 samples", 8)
    combo.setCurrentIndex(2)

    def onchange():
        vis.set_antialiasing(combo.currentData())

    combo.currentIndexChanged.connect(onchange)
    hbox.addWidget(QLabel("antialiasing:"))
    hbox.addWidget(combo)

    return hbox