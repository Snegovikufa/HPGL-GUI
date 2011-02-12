from PyQt4 import QtGui, QtCore

class UndefChangeWidget(QtGui.QDialog):
    def __init__(self, cubes, index, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.contCubes = cubes
        self.index = index

        self.initWidgets()
        self.initSignals()
        self.retranslateUI()

    def initWidgets(self):
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        doubleValidator = QtGui.QDoubleValidator(self)
        self.value = QtGui.QLineEdit()
        self.value.setValidator(doubleValidator)

        oldValue = self.contCubes.undefValue(self.index)
        self.value.setText(str(oldValue))

        self.changeButton = QtGui.QPushButton()

        self.vbox.addWidget(self.value)
        self.vbox.addWidget(self.changeButton)

    def initSignals(self):
        self.connect(self.changeButton, QtCore.SIGNAL("clicked()"), self.applyChange)

    def applyChange(self):
        self.hide()
        newValue = float(self.value.text())
        self.contCubes.changeUndefValue(newValue, self.index)

    def retranslateUI(self):
        self.changeButton.setText(self.__tr("Change"))
        self.setWindowTitle(self.__tr("HPGL GUI: ") +
                            self.__tr("Change undefined value"))

    def __tr(self, string, dis=None):
        return QtGui.qApp.translate("MainWindow", string, dis,
                                    QtGui.QApplication.UnicodeUTF8)
