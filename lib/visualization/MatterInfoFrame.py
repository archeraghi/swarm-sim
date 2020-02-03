from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt


class MatterInfoFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(MatterInfoFrame, self).__init__(*args, **kwargs)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: white; border: 2px solid black;")

        self.text = QLabel()
        self.text.setStyleSheet("border: 0px; padding: 0px; margin: 0px;")

        vbox = QVBoxLayout()
        vbox.addWidget(self.text, alignment=Qt.AlignBaseline)
        self.setLayout(vbox)

    def set_info(self, sim_objects):

        info_text = ""
        counter = 0
        for o in sim_objects:
            if counter > 0:
                info_text += "\n\n"
            info_text += str(o.type).upper()
            if o.type == "particle" and o.get_carried_status():
                info_text += " (carried)"
            if o.type == "tile" and o.get_tile_status():
                info_text += "(carried)"
            info_text += "\nid: %s" % str(o.get_id())
            info_text += "\ncoordinates: %s" % str(o.coordinates)
            info_text += "\ncolor: %s" % str(o.color)
            info_text += "\nmemory:"
            mem = o.read_whole_memory()
            for x in mem:
                info_text += "\n\t"+str(x)+": "+str(mem[x])
            counter += 1
        self.text.setText(info_text)
        self.adjustSize()
