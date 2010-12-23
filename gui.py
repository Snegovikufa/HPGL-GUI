from PyQt4 import QtGui, QtCore
import gui_widgets.load_cube_widget as LCW
import gui_widgets.cont_alg_widget as CAW
import gui_widgets.ind_alg_widget as IAW
import gui_widgets.statistics_window as SW
from geo_bsd.geo import write_property

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.Layout = QtGui.QGridLayout(self)
        self.resize(800, 400)
        
        self.Iterator = 0 # Iterator for cubes' names
        
        self.InitWidgets()
        self.InitSignals()
        self.RetranslateUI(self)
        
        self.CubesCont = []
        self.CubesInd = []

    def InitSignals(self):
        # Signals and slots
        self.connect(self.LoadCubesWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"), self.CatchCube)
        self.connect(self.LoadCubeButton, QtCore.SIGNAL("clicked()"), self.LoadCube)
        self.connect(self.Tree, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.ContextMenu)
        self.connect(self.Tree, QtCore.SIGNAL('collapsed(const QModelIndex &)'), self.ResizeColumn)
        self.connect(self.Tree, QtCore.SIGNAL('expanded(const QModelIndex &)'), self.ResizeColumn)
        self.connect(self.DeleteAction, QtCore.SIGNAL("triggered()"), self.DeleteCube)
        self.connect(self.AlgorithmAction, QtCore.SIGNAL("triggered()"), self.ApplyAlgorithm)
        self.connect(self.StatisticsAction, QtCore.SIGNAL("triggered()"), self.ShowStatistics)
        self.connect(self.SaveAction, QtCore.SIGNAL("triggered()"), self.SaveCube)
        self.connect(self.RenderAction, QtCore.SIGNAL("triggered()"), self.RenderCube)

    def InitWidgets(self):
        # Buttons
        self.LoadCubeButton = QtGui.QPushButton()
        self.LoadCubeButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        
        # Tree
        self.Tree = QtGui.QTreeView()
        self.Model = self.CreateModel(self)
        self.Tree.setModel(self.Model)
        self.Tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ResizeColumn()
        
        # Actions
        self.DeleteAction = QtGui.QAction(self.__tr("Delete"), self)
        self.StatisticsAction = QtGui.QAction(self.__tr("Statistics"), self)
        self.AlgorithmAction = QtGui.QAction(self.__tr("Apply algorithm"), self)
        self.SaveAction = QtGui.QAction(self.__tr("Save"), self)
        self.RenderAction = QtGui.QAction(self.__tr("Render"), self)
        
        # Menu
        self.PopMenu = QtGui.QMenu(self)
        self.PopMenu.addAction(self.AlgorithmAction)
        self.PopMenu.addAction(self.StatisticsAction)
        self.PopMenu.addAction(self.RenderAction)
        self.PopMenu.addAction(self.SaveAction)
        self.PopMenu.addAction(self.DeleteAction)
        
        # 3D View
        self.View = QtGui.QGraphicsView()
        
        # Placing on form
        self.Splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.Tree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.View.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Splitter.addWidget(self.Tree)
        self.Splitter.addWidget(self.View)
        self.Widgets = [self.LoadCubeButton, self.Splitter]
        self.WidgetsPlaces = [[0, 0, 1, 1], 
                              [2, 0, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.Widgets, self.WidgetsPlaces)
        # Other widgets
        self.LoadCubesWidget = LCW.LoadCube(self)

    def RenderCube(self):
        from gui_widgets.visualisator import MayaviQWidget
        Index = self.Tree.currentIndex()
        if Index.parent().row() == 0:
            self.v = MayaviQWidget(self.CubesCont[Index.row()][0][0],
                                            self.CubesCont[Index.row()][1],
                                            self.CubesCont[Index.row()][4])
        else:
            self.v = MayaviQWidget(self.CubesInd[Index.row()][0][0],
                                            self.CubesInd[Index.row()][1],
                                            self.CubesInd[Index.row()][4])
        self.v.run()
        
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1],
                                 places[i][2], places[i][3])
            
    def LoadCube(self):
        self.LoadCubesWidget.show()
        
    def ResizeColumn(self):
        self.Tree.resizeColumnToContents(0)
        self.Tree.resizeColumnToContents(1)
        self.Tree.resizeColumnToContents(2)
        
    def CatchCube(self, Cube):
        child = QtGui.QStandardItem(self.__tr(Cube[4]))
        child.setEditable(0)
        child_size = QtGui.QStandardItem(str(Cube[5]))
        child_size.setEditable(0)
        if Cube[2] != None:
            child_indicators = QtGui.QStandardItem(str(len(Cube[2])))
        else:
            child_indicators = QtGui.QStandardItem(str('-'))
        child_indicators.setEditable(0)
        list = [child, child_size, child_indicators]
        if Cube[2] == None:
            # This is Continuous cube
            self.Model.item(0, 0).appendRow(list)
            self.CubesCont.append(Cube)
        else:
            # This is Indicator cube
            self.Model.item(1, 0).appendRow(list)
            self.CubesInd.append(Cube)
        self.ResizeColumn()
    
    def ContextMenu(self, point):
        Index = self.Tree.indexAt(point)
        if Index.parent().row() != -1:
            self.PopMenu.exec_(self.Tree.mapToGlobal(point))
    
    def DeleteCube(self):
        Index = self.Tree.currentIndex()
        self.Model.removeRow(Index.row(), Index.parent())
        if Index.parent().row() == 0:
            del(self.CubesCont[Index.row()])
        else:
            del(self.CubesInd[Index.row()])
            
    def SaveCube(self):
        Index = self.Tree.currentIndex()
        Row = Index.row()
        Fname = QtGui.QFileDialog.getSaveFileName(self, 'Save as ...')
        if Fname and Index.parent().row() == 0:
            write_property( self.CubesCont[Row][0], unicode(Fname), 'Output',
                            self.CubesCont[Row][1], self.CubesCont[Row][2] )
        elif Fname and Index.parent().row() == 1:
            write_property( self.CubesInd[Row][0], unicode(Fname), 'Output',
                            self.CubesInd[Row][1], self.CubesInd[Row][2])
    
    def CreateModel(self, parent=None):
        Model = QtGui.QStandardItemModel(2, 2, parent)
    
        ContBranch = QtGui.QStandardItem("Continuous cubes")
        ContBranch.setEditable(0)
        IndBranch = QtGui.QStandardItem("Indicator cubes")
        IndBranch.setEditable(0)
        Model.setItem(0, 0, ContBranch)
        Model.setItem(1, 0, IndBranch)
                    
        Model.setHorizontalHeaderItem(0, QtGui.QStandardItem("Cube"))
        Model.setHorizontalHeaderItem(1, QtGui.QStandardItem("Size"))
        Model.setHorizontalHeaderItem(2, QtGui.QStandardItem("Indicators"))
        return Model
    
    def ApplyAlgorithm(self):
        Index = self.Tree.currentIndex()
        if Index.parent().row() == 0:
            self.ContAlgWidget = CAW.ContAlgWidget(self.Iterator)
            self.ContAlgWidget.Push(self.CubesCont, Index.row())
            self.connect(self.ContAlgWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"),
                         self.CatchCube)
        else:
            self.IndAlgWidget = IAW.IndAlgWidget(self.Iterator)
            self.IndAlgWidget.Push(self.CubesInd, Index.row())
            self.connect(self.IndAlgWidget, QtCore.SIGNAL("Cube(PyQt_PyObject)"),
                         self.CatchCube)
        self.Iterator += 1

    def ShowStatistics(self):
        Index = self.Tree.currentIndex()
        if Index.parent().row() == 0:
            self.StatWindow = SW.Statistics(self.CubesCont[Index.row()][0][0],
                                            self.CubesCont[Index.row()][1],
                                            self.CubesCont[Index.row()][4])
        else:
            self.StatWindow = SW.Statistics(self.CubesInd[Index.row()][0][0],
                                            self.CubesInd[Index.row()][1],
                                            self.CubesInd[Index.row()][4])
        self.StatWindow.show()
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis,
                                     QtGui.QApplication.UnicodeUTF8)
    
    def RetranslateUI(self, MainWindow):
        self.LoadCubeButton.setText(self.__tr("Load cube"))
        self.setWindowTitle('HPGL GUI')
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv).instance()
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
