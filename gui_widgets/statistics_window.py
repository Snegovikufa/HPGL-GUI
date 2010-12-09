from PyQt4 import QtGui, QtCore
import numpy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.path as path

class Statistics(QtGui.QDialog):
    def __init__(self, ValuesArray, UndefValue, CubeName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(720, 600)
        self.ValuesArray = ValuesArray
        self.UndefValue = UndefValue
        
        # Layouts, groupboxes
        self.Layout = QtGui.QGridLayout()
        self.setLayout(self.Layout)
        
        self.ValuesGB = QtGui.QGroupBox()
        self.ValuesGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.ValuesGBLayout = QtGui.QGridLayout(self.ValuesGB)
        
        self.MeanLabel = QtGui.QLabel(self.ValuesGB)
        self.VarianceLabel = QtGui.QLabel(self.ValuesGB)
        self.MaxLabel = QtGui.QLabel(self.ValuesGB)
        self.MinLabel = QtGui.QLabel(self.ValuesGB)
        self.MedianLabel = QtGui.QLabel(self.ValuesGB)
        self.DefPointsLabel = QtGui.QLabel(self.ValuesGB)
        self.AllPointsLabel = QtGui.QLabel(self.ValuesGB)
        
        self.MeanField = QtGui.QLineEdit(self.ValuesGB)
        self.MeanField.setReadOnly(1)
        self.VarianceField = QtGui.QLineEdit(self.ValuesGB)
        self.VarianceField.setReadOnly(1)
        self.MaxField = QtGui.QLineEdit(self.ValuesGB)
        self.MaxField.setReadOnly(1)
        self.MinField = QtGui.QLineEdit(self.ValuesGB)
        self.MinField.setReadOnly(1)
        self.MedianField = QtGui.QLineEdit(self.ValuesGB)
        self.MedianField.setReadOnly(1)
        self.DefPointsField = QtGui.QLineEdit(self.ValuesGB)
        self.DefPointsField.setReadOnly(1)
        self.AllPointsField = QtGui.QLineEdit(self.ValuesGB)
        self.AllPointsField.setReadOnly(1)
        
        self.ValuesSpacer = QtGui.QSpacerItem(40, 20, 
                                              QtGui.QSizePolicy.Expanding, 
                                              QtGui.QSizePolicy.Minimum)
        
        self.ValuesWidgets = [self.MaxLabel, self.MaxField,
                              self.MinLabel, self.MinField,
                              self.MeanLabel, self.MeanField,
                              self.MedianLabel, self.MedianField,
                              self.VarianceLabel, self.VarianceField,
                              self.DefPointsLabel, self.DefPointsField,
                              self.AllPointsLabel, self.AllPointsField,
                              ]
        self.ValuesWidgetsPlaces = [[0, 1, 1, 1], [0, 2, 1, 1],
                                    [0, 3, 1, 1], [0, 4, 1, 1],
                                    [1, 1, 1, 1], [1, 2, 1, 1],
                                    [1, 3, 1, 1], [1, 4, 1, 1],
                                    [2, 3, 1, 1], [2, 4, 1, 1],
                                    [4, 1, 1, 1], [4, 2, 1, 1],
                                    [4, 3, 1, 1], [4, 4, 1, 1],
                                    ]
        self.PlaceWidgetsAtPlaces(self.ValuesGBLayout, self.ValuesWidgets, 
                                  self.ValuesWidgetsPlaces)
        
        self.ViewConfigGB = QtGui.QGroupBox()
        self.ViewConfigGB.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.ViewConfigGBLayout = QtGui.QGridLayout(self.ViewConfigGB)
        
        self.RowCountLabel = QtGui.QLabel(self.ViewConfigGB)
        self.RowCount = QtGui.QSpinBox(self.ViewConfigGB)
        self.RowCount.setValue(10)
        self.RowCount.setSingleStep(20)
        self.RowCount.setRange(10, 150)
        self.ViewConfigWidgets = [self.RowCountLabel, self.RowCount,]
        self.ViewConfigWidgetsPlaces = [[0, 0, 1, 1], [0, 1, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.ViewConfigGBLayout, 
                                  self.ViewConfigWidgets,
                                  self.ViewConfigWidgetsPlaces)
        # Graphics
        self.GraphBG = QtGui.QGroupBox()
        self.GraphBGLayout = QtGui.QGridLayout(self.GraphBG)
        self.GraphWidget = QtGui.QWidget()
        self.GraphBGLayout.addWidget(self.GraphWidget)
        
        self.WindowWidgets = [self.ViewConfigGB,
                              self.GraphBG,
                              self.ValuesGB]
        self.WindowWidgetsPlaces = [[0, 0, 1, 1], [0, 1, 3, 1],
                                    [2, 0, 1, 1]]
        self.PlaceWidgetsAtPlaces(self.Layout, self.WindowWidgets, 
                                  self.WindowWidgetsPlaces)
        
        self.RetranslateUI(self)
        
        # Let's draw graph and calculate cube's values
        self.CalculateValues()
        self.CreateHistogramFrame()
        self.UpdateHistogram()
        
        self.connect(self.RowCount, QtCore.SIGNAL('valueChanged(int)'),
                     self.UpdateHistogram)
                
    def PlaceWidgetsAtPlaces(self, layout, widgets, places):
        '''Places list of widgets to their places'''
        for i in xrange(len(widgets)):
            if type(widgets[i]) == type(self.ValuesSpacer):
                layout.addItem(widgets[i], places[i][0], places[i][1], 
                               places[i][2], places[i][3])
            else:
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
        
        self.MaxField.setText(str(Max))
        self.MinField.setText(str(Min))
        self.MeanField.setText(str(Mean))
        self.VarianceField.setText(str(Variance))
        self.MedianField.setText(str(Median))
        self.DefPointsField.setText(str(DefPoints))
        self.AllPointsField.setText(str(AllPoints))
        
    def CreateHistogramFrame(self):
        self.dpi = 100
        self.Fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.Canvas = FigureCanvas(self.Fig)
        self.Canvas.setParent(self.GraphWidget)
        self.Canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.CanvasToolbar = NavigationToolbar(self.Canvas, self.GraphWidget)
        
        self.Axes = self.Fig.add_subplot(111)
        
        GraphLayout = QtGui.QVBoxLayout()
        GraphLayout.addWidget(self.Canvas)
        GraphLayout.addWidget(self.CanvasToolbar)
        self.GraphWidget.setLayout(GraphLayout)
        
    def UpdateHistogram(self):
        self.Axes.clear()
        N, Bins = numpy.histogram(self.ClearValues, self.RowCount.value())
        
        Left = numpy.array(Bins[:-1])
        Right = numpy.array(Bins[1:])
        Bottom = numpy.zeros(len(Left))
        # if checked :
        Top = (Bottom + N)/N.max()
        # else:
        # Top = Bottom+N
        
        XY = numpy.array([[Left,Left,Right,Right], [Bottom,Top,Top,Bottom]]).T
        BarPath = path.Path.make_compound_path_from_polys(XY)
        Patch = patches.PathPatch(BarPath, facecolor='blue', edgecolor='gray', alpha=0.8)
        
        self.Axes.add_patch(Patch)
        self.Axes.set_xlim(Left[0], Right[-1])
        self.Axes.set_ylim(Bottom.min(), Top.max())
        
        self.Axes.grid(1)
        self.Axes.set_xlabel(self.__tr('Value'))
        
        self.Canvas.draw()
        
    def RetranslateUI(self, MainWindow):
        self.setWindowTitle(self.__tr("HPGL GUI: Statistics"))
        
        self.MeanLabel.setText(self.__tr('Mean:'))
        self.VarianceLabel.setText(self.__tr('Variance:'))
        self.MaxLabel.setText(self.__tr('Max:'))
        self.MinLabel.setText(self.__tr('Min:'))
        self.MedianLabel.setText(self.__tr('Median:'))
        self.DefPointsLabel.setText(self.__tr('Defined points:'))
        self.AllPointsLabel.setText(self.__tr('Total points:'))
        self.RowCountLabel.setText(self.__tr('Row count:'))
        
        self.ValuesGB.setTitle(self.__tr("Values:"))
        self.ViewConfigGB.setTitle(self.__tr("Histogram config"))
    
    def __tr(self, string, dis=None):
        '''Small function to translate'''
        return QtGui.qApp.translate("MainWindow", string, dis, 
                                     QtGui.QApplication.UnicodeUTF8)
                
