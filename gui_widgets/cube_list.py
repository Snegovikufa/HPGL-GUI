# -*- coding: utf-8 -*-
import numpy

class CubeItem():
    def __init__(self):
        self.__items = []
        
    #===========================================================================
    # Functions to work with list of cubes
    #===========================================================================
    def append(self, property, undefinedValue, indicatorValues, gridObject, name, gridSize):
        '''Append cube to list'''
        self.__items.append([property, 
                           undefinedValue, 
                           indicatorValues,
                           gridObject, 
                           name, 
                           gridSize])
        
    def count(self):
        '''Return count of cubes in list'''
        return len(self.__items)
    
    def setProperty(self, index, property):
        if index < 0 or index > self.count():
            return
        
        self.__items[index][0] = property
    
    def setUndefValue(self, index, value):
        if index < 0 or index > self.count():
            return
        
        self.__items[index][1] = value
        
    def setIndicators(self, index, indicators=None):
        if index < 0 or index > self.count():
            return
        
        self.__items[index][2] = indicators
        
    def setGridObject(self, index, gridObject):
        if index < 0 or index > self.count():
            return
        
        self.__items[index][3] = gridObject
        
    def setName(self, index, name):
        if index < 0 or index > self.count():
            return
        
        self.__items[index][4] = unicode(name, 'utf-8')
        
    def setGridSize(self, index, gridSize):
        '''Sets grid size of cube at index, gridSize must be list (x, y, z)'''
        if index < 0 or index > self.count():
            return
        if type(gridSize) != type(tuple()): 
            return
        if type(gridSize) != type(list()):
            return
        if len(gridSize) != 3:
            return
        
        self.__items[index][5] = gridSize
    #------------------------------------------------------------------------------ 
    
    #===========================================================================
    # Variables that needed for algorithms
    #===========================================================================
    
    def property(self, index):
        '''Return cubes property at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][0]
    
    def undefValue(self, index):
        '''Return undefined value of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][1]
    
    def indicators(self, index):
        '''Return indicators of cube at index'''
        if index < 0 or index > self.count():
            return None
        # May be return something another?
        
        return self.__items[index][2]
    
    def gridObject(self, index):
        '''Return grid object of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][3]
    
    def name(self, index):
        '''Return name of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][4]
    
    def size(self, index):
        '''Return grid size of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][5]
    
    def isIndicator(self, index):
        '''Returns True if cube is indicator else returns False'''
        if index < 0 or index > self.count():
            return None
        # May be return something another?
        
        if self.__items[index][2] == None:
            return False
        else:
            return True
    #------------------------------------------------------------------------------ 
    
    #===========================================================================
    # Values in cubes
    #===========================================================================
    
    def allValues(self, index):
        '''Returns all values of cube (with undefined)'''
        if index < 0 or index > self.count():
            return None
        
        return self.__items[index][0][0]
    
    def definedValues(self, index):
        '''Returns values of cube without undefined'''
        if index < 0 or index > self.count():
            return None
        
        allValues = self.allValues(index)
        undefined = self.undefValue(index)
        
        # nonzero return indexes of defined values, but we need values, not indexes
        return allValues[numpy.nonzero(allValues != undefined)]
    
    def maxOf(self, index):
        '''Maximum defined value of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        defValues = self.definedValues(index)
        return numpy.max(defValues)
    
    def minOf(self, index):
        if index < 0 or index > self.count():
            return None
        
        defValues = self.definedValues(index)
        return numpy.min(defValues)
    
    def medianOf(self, index):
        if index < 0 or index > self.count():
            return None
        
        defValues = self.definedValues(index)
        return numpy.median(defValues)
    
    def meanOf(self, index):
        if index < 0 or index > self.count():
            return None
        
        defValues = self.definedValues(index)
        return numpy.mean(defValues)
    
    def varianceOf(self, index):
        if index < 0 or index > self.count():
            return None
        
        defValues = self.definedValues(index)
        return numpy.var(defValues)
    #------------------------------------------------------------------------------ 