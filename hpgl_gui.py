from PyQt4 import QtGui, QtCore
import gui_widgets.load_cube_widget as LCW
import gui_widgets.cont_alg_widget as CAW
import gui_widgets.ind_alg_widget as IAW

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout(self)
        self.Toolbar = QtGui.QToolBar()
        self.resize(800, 400)
        
        # Load cube button
        self.LoadCubeButton = QtGui.QPushButton()
        
        # Tree
        self.Tree = QtGui.QTreeWidget()
        self.Tree.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.Tree.setColumnCount(1)
        # Branches
        self.IndBranch = QtGui.QTreeWidgetItem()
        self.ContBranch = QtGui.QTreeWidgetItem()
        self.TestBranch = QtGui.QTreeWidgetItem()
        
        self.Tree.addTopLevelItem(self.IndBranch)
        self.Tree.addTopLevelItem(self.ContBranch)
        self.ContBranchChilds = []
        self.IndBranchChilds = []
        self.TreeHeader = self.Tree.headerItem()
        
        self.Tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # Actions
        self.DeleteAction = QtGui.QAction(self.__tr("Delete"), self)
        self.RenameAction = QtGui.QAction(self.__tr("Rename"), self)
        self.StatisticsAction = QtGui.QAction(self.__tr("Statistics"), self)
        self.AlgorithmAction = QtGui.QAction(self.__tr("Apply algorithm"), self)

        # Menu
        self.PopMenu = QtGui.QMenu( self )
        self.PopMenu.addAction(self.AlgorithmAction)
        self.PopMenu.addAction(self.DeleteAction)
        self.PopMenu.addAction(self.RenameAction)
        
        # 3D View
        self.View = QtGui.QGraphicsView()
        
        # Placing on form
        self.Widgets = [self.LoadCubeButton, self.Tree,
                        self.View]
        self.WidgetsPlaces = [[0, 0, 1, 1], [1, 0, 1, 1],
                              [0, 1, 2, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.Widgets, self.WidgetsPlaces)
        
        # Other widgets, etc.
        self.LoadCubesWidget = LCW.LoadCube()
        self.connect(self.LoadCubesWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"),
                     self.CatchCube)
        
        self.CubesCont = []
        self.CubesInd = []
        
        # Retranslate
        self.RetranslateUI(self)
        
        # Signals and slots
        self.connect(self.LoadCubeButton, QtCore.SIGNAL("clicked()"),
                     self.LoadCube)
        self.connect(self.Tree, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), 
                     self.ContextMenu)
        self.connect(self.DeleteAction, QtCore.SIGNAL("triggered()"),
                     self.DeleteCube)
        self.connect(self.RenameAction, QtCore.SIGNAL("triggered()"),
                     self.RenameItem)
        self.connect(self.AlgorithmAction, QtCore.SIGNAL("triggered()"),
                     self.ApplyAlgorithm)
    
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1], 
                                 places[i][2], places[i][3])
            
    def LoadCube(self):
        self.LoadCubesWidget.show()
        
    def CatchCube(self, Cube):
        NewChild = QtGui.QTreeWidgetItem()
        NewChild.setText(0, self.__tr(Cube[4]))
        if Cube[2] == None:
            self.CubesCont.append(Cube)
            self.ContBranch.addChild(NewChild)
            self.ContBranchChilds.append(NewChild)            
        else:
            self.CubesInd.append(Cube)
            self.IndBranch.addChild(NewChild)
            self.IndBranchChilds.append(NewChild)
        
    def ContextMenu(self, point):
        if self.Tree.itemAt(point) != self.IndBranch and \
            self.Tree.itemAt(point) != self.ContBranch:
            self.PopMenu.exec_(self.Tree.mapToGlobal(point))
            
    def RenameItem(self):
        text = self.ContBranch.text(0)
        self.ContBranch.setText(QtCore.Qt.EditRole, text)
        
    def ApplyAlgorithm(self):
        self.index = self.Tree.currentIndex()
        if self.IndBranch.indexOfChild(self.Tree.currentItem()) != -1:
            self.IndAlgWidget = IAW.IndAlgWidget()
            self.IndAlgWidget.Push(self.CubesInd, self.index.row())
        else:
            self.ContAlgWidget = CAW.ContAlgWidget()
            self.ContAlgWidget.Push(self.CubesCont, self.index.row())
        
    def DeleteCube(self):
        self.index = self.Tree.currentIndex()
        
        if self.IndBranch.indexOfChild(self.Tree.currentItem()) != -1:
            self.IndBranch.removeChild(self.Tree.currentItem())
            del(self.CubesInd[self.index.row()])
        else:
            self.ContBranch.removeChild(self.Tree.currentItem())
            del(self.CubesCont[self.index.row()])
        
    def RetranslateUI(self, MainWindow):
        self.LoadCubeButton.setText(self.__tr("Load cube"))
        self.IndBranch.setText(0, self.__tr("Indicator cubes"))
        self.ContBranch.setText(0, self.__tr("Continuous cubes"))
        self.TreeHeader.setText(0, self.__tr("Loaded cubes"))
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
