from PySide import QtGui, QtCore

class LogWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(600, 300)
        
        self.TextEdit = QtGui.QTextEdit()
        self.ButtonBox = QtGui.QDialogButtonBox()
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Close)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.TextEdit)
        self.mainLayout.addWidget(self.ButtonBox)
        
        self.connect(self.ButtonBox, QtCore.SIGNAL('rejected()'),
                     self.CloseWindow)
        self.connect(self.ButtonBox, QtCore.SIGNAL('accepted()'),
                     self.SaveLog)
        
    def showMessage(self, title, message):
        self.TextEdit.clear()
        self.setWindowTitle(title)
        self.TextEdit.insertPlainText(message)
        self.show()
        
    def CloseWindow(self):
        self.hide()
    
    def SaveLog(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as')
        if self.fname:
            f = open(self.fname, 'w')
            f.write(self.TextEdit.toPlainText())
