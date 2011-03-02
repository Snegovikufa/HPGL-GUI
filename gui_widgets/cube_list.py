# -*- coding: utf-8 -*-
import numpy
from geo_bsd import ContProperty, IndProperty

class CubeItem(object):
    def __init__(self, parent = None):
        self.__items = []
        self.__parent = parent
        self.__childItems = []

    #===========================================================================
    # Functions to work with list of cubes
    #===========================================================================
    def append(self, property, undefinedValue,
                     indicatorValues, gridObject, name, gridSize, log=''):
        '''Append cube to list'''
        self.__items.append([property,
                           undefinedValue,
                           indicatorValues,
                           gridObject,
                           name,
                           gridSize,
                           log])
        print self.__items

    def appendItem(self, cubeItem):
        self.__items += cubeItem.__items
        print self.__items

    def deleteItem(self, index=0):
        print 'ITEMS:', self.__items
        print 'DELETING:', index
        del(self.__items[index])

    def count(self):
        '''Return count of cubes in list'''
        return len(self.__items)

    def setProperty(self, property, index = 0):
        self.__items[index][0] = property

    def setUndefValue(self, value,index = 0):
        self.__items[index][1] = value

    def setIndicators(self, indicators=None, index=0):
        self.__items[index][2] = indicators

    def setGridObject(self, gridObject, index=0):
        self.__items[index][3] = gridObject

    def setName(self, name, index=0):
        self.__items[index][4] = str(name)

    def setGridSize(self, gridSize, index=0):
        '''Sets grid size of cube at index, gridSize must be list (x, y, z)'''
        if type(gridSize) != type(tuple()):
            return
        if type(gridSize) != type(list()):
            return
        if len(gridSize) != 3:
            return

        self.__items[index][5] = gridSize

    def setLog(self, text, index=0):
        self.__items[index][6] += text

    def changeUndefValue(self, newValue, index=0):
        print newValue, index
        
        if self.undefValue(index) == newValue:
            return

        # Changing undefined value
        self.setUndefValue(newValue, index)

        # Also we need to change mask
        allValues = self.allValues(index)
        indexes = numpy.nonzero(allValues != newValue)
        shape = numpy.shape(allValues)
        # Creating zero array ...
        mask = numpy.zeros(shape, dtype='uint8', order='F')
        # ... and filling mask with 1 to indexes of defined values
        mask[indexes] = 1
        # Changing old mask with new
        if not self.isIndicator(index):
            prop = ContProperty(allValues, mask)
        else:
            prop = IndProperty(allValues, mask, self.indicatorsCount(index))
        self.setProperty(prop)
    #------------------------------------------------------------------------------

    #===========================================================================
    # Variables that needed for algorithms
    #===========================================================================

    def item(self, index=0):
        '''Return one item at index'''
        item = CubeItem()
        item.append(*self.__items[index])
        return item

    def property(self, index=0):
        '''Return cubes property at index'''
        return self.__items[index][0]

    def undefValue(self, index=0):
        '''Return undefined value of cube at index'''
        return self.__items[index][1]

    def indicators(self, index=0):
        '''Return indicators of cube at index'''
        return self.__items[index][2]

    def indicatorsCount(self, index=0):
        return numpy.float32(len(self.__items[index][2]))

    def gridObject(self, index=0):
        '''Return grid object of cube at index'''
        return self.__items[index][3]

    def name(self, index=0):
        '''Return name of cube at index'''
        return str(self.__items[index][4])

    def allNames(self):
        '''Return list of cubes' names'''
        a = range(self.count())

        for i in xrange(self.count()):
            a[i] = self.name(i)

        return a

    def size(self, index=0):
        '''Return grid size of cube at index'''
        return self.__items[index][5]

    def log(self, index=0):
        return self.__items[index][6]

    def isIndicator(self, index=0):
        '''Returns True if cube is indicator else returns False'''
        if self.__items[index][2] == None:
            return False
        else:
            return True
    #------------------------------------------------------------------------------

    #===========================================================================
    # Values in cubes
    #===========================================================================

    def allValues(self, index=0):
        '''Returns all values of cube (with undefined)'''
        return self.__items[index][0][0]

    def mask(self, index=0):
        return self.__items[index][0][1]

    def definedValues(self, index=0):
        '''Returns values of cube without undefined'''
        allValues = self.allValues(index)
        undefined = self.undefValue(index)

        # nonzero return indexes of defined values, but we need values
        return allValues[numpy.nonzero(allValues != undefined)]
    
    def hasDefined(self, index):
        if len(self.definedValues(index)) != 0:
            return True
        
        return False

    def maxOf(self, index=0):
        '''Maximum defined value of cube at index'''
        defValues = self.definedValues(index)
        return numpy.max(defValues)

    def minOf(self, index=0):
        '''Minimum defined value of cube at index'''
        defValues = self.definedValues(index)
        return numpy.min(defValues)

    def medianOf(self, index=0):
        defValues = self.definedValues(index)
        return numpy.median(defValues)

    def meanOf(self, index=0):
        defValues = self.definedValues(index)
        return numpy.mean(defValues)

    def varianceOf(self, index=0):
        defValues = self.definedValues(index)
        return numpy.var(defValues)
    #------------------------------------------------------------------------------
    
    def parent(self):
        return self.__parent

class RootItem():
    def __init__(self):
        self.__childItems = []
        
    def childCount(self, index):
        return len(self.__childItems)
    
    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0
    
    def columnCount(self):
        return 4
    
    def parent(self):
        return None
    
    def appendChildItem(self, cubeItem):
        self.__childItems.append(cubeItem)
