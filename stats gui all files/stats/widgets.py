from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

class sliderAndLabel(QSlider):
    def __init__(self, parent, minVal, maxVal, row, col, initVal=None, text="", textDiv=1):
        QSlider.__init__(self, parent)

        self.setOrientation(Qt.Horizontal)
        
        if not initVal: initVal = minVal
        
        self.setRange(int(minVal), int(maxVal))
        self.setValue(int(initVal))

        self.setFixedWidth(100)

        label = QLabel(self.window())

        label.setFont(QFont("CMU Serif"))
        label.setStyleSheet("color: white")
        label.setText(text)

        label.setFixedWidth(100)

        self.valueChanged.connect(lambda: label.setText(text + str(self.value()/textDiv)))
        
        self.parent().layout().addWidget(self,  row, col)
        self.parent().layout().addWidget(label, row, col+1)

class boxAndLabel(QCheckBox):
    def __init__(self, parent, row, col, initState=False, text=""):
        QCheckBox.__init__(self, parent)

        self.setChecked(initState)

        self.setFixedWidth(100)

        label = QLabel(self.window())

        label.setFont(QFont("CMU Serif"))
        label.setStyleSheet("color: white")
        label.setWordWrap(True)
        label.setText(text)

        label.setFixedWidth(100)

        self.parent().layout().addWidget(self, row, col)
        self.parent().layout().addWidget(label,    row, col+1)
