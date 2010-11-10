from PyQt4 import QtGui, QtCore

class error_window(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.TextEdit = QtGui.QTextEdit()
        self.ButtonBox = QtGui.QDialogButtonBox()
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Close)
        
        self.Layout = QtGui.QVBoxLayout()
        self.setLayout(self.Layout)
        self.Layout.addWidget(self.TextEdit)
        self.Layout.addWidget(self.ButtonBox)
        
        self.connect(self.ButtonBox, QtCore.SIGNAL('rejected()'), 
                     self.CloseWindow)
        self.connect(self.ButtonBox, QtCore.SIGNAL('accepted()'),
                     self.SaveLog)
        
    def showmessage(self, title, message):
        self.TextEdit.clear()
        self.setWindowTitle(title)
        self.message = message
        self.TextEdit.insertPlainText(self.message)
        self.show()
        
    def CloseWindow(self):
        self.hide()
    
    def SaveLog(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self,'Save as ... ')
        if self.fname:
            f = open(self.fname, 'wb')
            f.write(self.message)