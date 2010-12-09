from PyQt4 import QtGui, QtCore
import numpy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.path as path

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, Datain, Header, Parent=None):
        QtCore.QAbstractTableModel.__init__(self, Parent)
        self.ArrayData = Datain
        self.HeaderData = Header

    def rowCount(self, parent):
        return len(self.ArrayData[0])

    def columnCount(self, parent):
        return len(self.ArrayData)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.ArrayData[index.column()][index.row()])
    
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.HeaderData[col])
        return QtCore.QVariant()

class Statistics(QtGui.QDialog):
    def __init__(self, ValuesArray, UndefValue, CubeName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(840, 500)
        self.ValuesArray = ValuesArray
        self.UndefValue = UndefValue
        self.setWindowTitle(self.__tr("HPGL GUI: Statistics for: " + CubeName))
        
        # Layouts, groupboxes
        self.Layout = QtGui.QHBoxLayout()
        self.setLayout(self.Layout)
        
        # Values GroupBox
        self.ValuesGB = QtGui.QGroupBox()
        self.ValuesGBLayout = QtGui.QVBoxLayout(self.ValuesGB)
        
        self.ValuesTable = QtGui.QTableView()
        self.ValuesGBLayout.addWidget(self.ValuesTable)
        
        # Histogram configuring widgets
        self.ViewConfigGB = QtGui.QGroupBox()
        self.ViewConfigGBLayout = QtGui.QGridLayout(self.ViewConfigGB)
        
        self.RowCountLabel = QtGui.QLabel(self.ViewConfigGB)
        self.RowCount = QtGui.QSpinBox(self.ViewConfigGB)
        self.RowCount.setValue(10)
        self.RowCount.setSingleStep(20)
        self.RowCount.setRange(10, 150)
        
        self.ProbabilityChange = QtGui.QCheckBox()
        self.ProbabilityChange.setLayoutDirection(QtCore.Qt.RightToLeft)
        
        self.XMin = QtGui.QSpinBox(self.ViewConfigGB)
        self.XMinLabel = QtGui.QLabel(self.ViewConfigGB)
        self.XMax = QtGui.QSpinBox(self.ViewConfigGB)
        self.XMaxLabel = QtGui.QLabel(self.ViewConfigGB)
        
        self.ViewConfigWidgets = [self.RowCountLabel, self.RowCount,
                                  self.ProbabilityChange,
                                  self.XMinLabel, self.XMin,
                                  self.XMaxLabel, self.XMax,]
        self.ViewConfigWidgetsPlaces = [[0, 0, 1, 1], 
                                        [0, 1, 1, 1],
                                        [1, 0, 1, 1],
                                        [2, 0, 1, 1], [2, 1, 1, 1],
                                        [3, 0, 1, 1], [3, 1, 1, 1],
                                        ]
        self.PlaceWidgetsAtPlaces(self.ViewConfigGBLayout, 
                                  self.ViewConfigWidgets,
                                  self.ViewConfigWidgetsPlaces)
        
        # Graphics
        self.GraphWidget = QtGui.QWidget()
        self.GraphLayout = QtGui.QVBoxLayout(self.GraphWidget)
        
        self.CloseButtonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Close)
        
        # Translating UI
        self.RetranslateUI(self)
        
        # Let's draw graph and calculate cube's values
        self.CalculateValues()
        self.CreateHistogramFrame()
        
        # Catching Histogram window
        self.GraphLayout.addWidget(self.Canvas)
        self.GraphLayout.addWidget(self.CloseButtonBox)
        
        # Update Histogram and set ranges
        self.UpdateHistogram()
        self.InitRanges()
        
        # Layouts
        LeftVBox = QtGui.QVBoxLayout()
        LeftVBox.addWidget(self.ViewConfigGB)
        LeftVBox.addWidget(self.ValuesGB)
        LeftVBox.addWidget(QtGui.QWidget())
        
        RightVBox = QtGui.QVBoxLayout()
        RightVBox.addWidget(self.GraphWidget)
        
        self.Layout.addLayout(LeftVBox)
        self.Layout.addLayout(RightVBox)
        self.Layout.setStretch(1, 1)
        
        # Signals and slots
        self.connect(self.RowCount, QtCore.SIGNAL('valueChanged(int)'),
                     self.UpdateHistogram)
        self.connect(self.ProbabilityChange, QtCore.SIGNAL('stateChanged(int)'),
                     self.UpdateHistogram)
        self.connect(self.XMax, QtCore.SIGNAL('valueChanged(int)'),
                     self.UpdateHistogram)
        self.connect(self.XMin, QtCore.SIGNAL('valueChanged(int)'),
                     self.UpdateHistogram)
        self.connect(self.CloseButtonBox, QtCore.SIGNAL('rejected()'),
                     self, QtCore.SLOT('close()'))
                
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            layout.addWidget(widgets[i], places[i][0], places[i][1], 
                                 places[i][2], places[i][3])
                
    def CalculateValues(self):
        self.ClearValues = self.ValuesArray[numpy.nonzero(self.ValuesArray != self.UndefValue)]
        
        Max = '%.2f' % numpy.max(self.ClearValues)
        Mean = '%.2f' % numpy.mean(self.ClearValues)
        Min = '%.2f' % numpy.min(self.ClearValues)
        Median = '%.2f' % numpy.median(self.ClearValues)
        Variance = '%.2f' % numpy.var(self.ClearValues)
        DefPoints = numpy.size(self.ClearValues)
        AllPoints = numpy.size(self.ValuesArray)
        Values = [['Max', 'Min', 'Mean', 'Median',
                  'Variance', 'Defined points', 'Total points'],
                  [Max, Min, Mean, Median, Variance,
                   DefPoints, AllPoints]]
        Header = ['Property', 'Value']
        
        self.TableModel = TableModel(Values, Header, self)
        self.ValuesTable.setModel(self.TableModel)
        self.ValuesTable.resizeColumnToContents(0)
        
    def CreateHistogramFrame(self):
        self.dpi = 100
        self.Fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.Canvas = FigureCanvas(self.Fig)
        
        self.Axes = self.Fig.add_subplot(111)
        
    def InitRanges(self):
        self.XMin.setValue(self.XMin.minimum())
        self.XMax.setValue(self.XMax.maximum())
        self.UpdateHistogram()
        
    def UpdateHistogram(self):
        self.Axes.clear()
        N, Bins = numpy.histogram(self.ClearValues, self.RowCount.value())
        
        Left = numpy.array(Bins[:-1])
        Right = numpy.array(Bins[1:])
        Bottom = numpy.zeros(len(Left))
        
        if self.ProbabilityChange.isChecked():
            Top = (Bottom + N)/N.max()
            self.Axes.set_ylabel(self.__tr("Probability"))
        else:
            Top = Bottom+N
            self.Axes.set_ylabel(self.__tr("Number of cells"))
        
        XY = numpy.array([[Left,Left,Right,Right], [Bottom,Top,Top,Bottom]]).T
        BarPath = path.Path.make_compound_path_from_polys(XY)
        Patch = patches.PathPatch(BarPath, facecolor='blue', 
                                  edgecolor='gray', alpha=0.8)
        
        self.Axes.add_patch(Patch)
        
        # Limits
        self.XMin.setRange(Left[0], Right[-2])
        self.XMax.setRange(self.XMin.value()+1, Right[-1])
        self.Axes.set_xlim(self.XMin.value(), self.XMax.value())
        self.Axes.set_ylim(Bottom.min(), Top.max())
        
        self.Axes.grid(1)
        self.Axes.set_xlabel(self.__tr('Value'))
        
        self.Canvas.draw()
        
    def RetranslateUI(self, MainWindow):
        self.ValuesGB.setTitle(self.__tr("Values:"))
        self.ViewConfigGB.setTitle(self.__tr("Histogram config"))
        
        self.RowCountLabel.setText(self.__tr('Row count:'))
        self.ProbabilityChange.setText(self.__tr('Show as probability'))
        self.XMaxLabel.setText(self.__tr("X max:"))
        self.XMinLabel.setText(self.__tr("X min:"))
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
                
