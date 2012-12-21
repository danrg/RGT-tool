from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType

class ViewNode(BasicSvgNode):

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_VIEW_BOX= 'viewBox'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO= 'preserveAspectRatio'
    ATTRIBUTE_ZOOM_AND_PAN= 'zoomAndPan'
    ATTRIBUTE_VIEW_TARGET= 'viewTarget'


    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'view')
        
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
    
    def setZoomAndPan(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ZOOM_AND_PAN, data)
    
    def setViewTarget(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEW_TARGET, data)
    
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
    
    def getZoomAndPan(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ZOOM_AND_PAN)
        if node != None:
            return node.nodeValue
        return None
    
    def getViewTarget(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VIEW_TARGET)
        if node != None:
            return node.nodeValue
        return None