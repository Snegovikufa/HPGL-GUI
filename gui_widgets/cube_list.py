class CubeItem():
    def __init__(self):
        self.Items = []
        
    def append(self, Property, UndefinedValue, IndicatorValues, GridObject, CubeName, GridSize):
        '''Append cube to list'''
        self.Items.append([Property, 
                           UndefinedValue, 
                           IndicatorValues,
                           GridObject, 
                           CubeName, 
                           GridSize])
        
    def count(self):
        '''Return count of cubes in list'''
        return len(self.Items)
    
    def property(self, index):
        '''Return cubes property at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][0]
    
    def indicators(self, index):
        '''Return indicators of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][2]
    
    def undefValue(self, index):
        '''Return undefined value of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][1]
    
    def name(self, index):
        '''Return name of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][4]
    
    def size(self, index):
        '''Return grid size of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][5]
    
    def gridObject(self, index):
        '''Return grid object of cube at index'''
        if index < 0 or index > self.count():
            return None
        
        return self.Items[index][3]
