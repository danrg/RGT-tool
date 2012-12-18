from RGT.XML.SVG.containerNode import ContainerNode
from types import StringType

class MarkerNode(ContainerNode):

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_VIEW_BOX= 'viewBox'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO= 'preserveAspectRatio'
    ATTRIBUTE_REF_X= 'refX'
    ATTRIBUTE_REF_Y= 'refY'
    ATTRIBUTE_MARKER_UNITS= 'markerUnits'
    ATTRIBUTE_MARKER_WIDTH= 'markerWidth'
    ATTRIBUTE_MARKER_HEIGHT= 'markerHeight'
    ATTRIBUTE_ORIENT= 'orient'

    def __init__(self, ownderDoc):
        ContainerNode.__init__(self, ownderDoc, 'marker')
        
    
    def setExternalResourcesRequired(self, data):
        allowedValues= ['true', 'false']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)
    
    def setViewBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEW_BOX, data)
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO, data)
    
    def setRefX(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REF_X, data)
    
    def setRefY(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REF_Y, data)
    
    def setMarkerUnits(self, data):
        allowedValues= ['strokeWidth', 'userSpaceOnUse']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_MARKER_UNITS, data)
    
    def setMarkerWidth(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_WIDTH, data)
    
    def setMarkerHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_HEIGHT, data)
            
    def setOrient(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ORIENT, data)
            
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getViewBox(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VIEW_BOX)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO)
        if node != None:
            return node.nodeValue
        return None
        
    def getRefX(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_REF_X)
        if node != None:
            return node.nodeValue
        return None
    
    def getRefY(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_REF_Y)
        if node != None:
            return node.nodeValue
        return None
    
    def getMarkerUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_UNITS)
        if node != None:
            return node.nodeValue
        return None
    
    def getMarkerWidth(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_WIDTH)
        if node != None:
            return node.nodeValue
        return None
    
    def getMarkerHeight(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_HEIGHT)
        if node != None:
            return node.nodeValue
        return None
    
    def getOrient(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ORIENT)
        if node != None:
            return node.nodeValue
        return None