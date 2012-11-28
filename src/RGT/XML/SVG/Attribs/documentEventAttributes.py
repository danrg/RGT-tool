from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class DocumentEventAttributes(BasicSvgAttribute):
    
    ATTRIBUTE_ON_UNLOAD= 'onunload'
    ATTRIBUTE_ON_ABORT= 'onabort'
    ATTRIBUTE_ON_ERROR= 'onerror'
    ATTRIBUTE_ON_RESIZE= 'onresize'
    ATTRIBUTE_ON_SCROLL= 'onscroll'
    ATTRIBUTE_ON_ZOOM= 'onzoom'
    
    
    def setOnUnload(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_UNLOAD, data)
    
    def setOnAbort(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_ABORT, data)
            
    def setOnError(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_ERROR, data)
    
    def setOnResize(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_RESIZE, data)

    def setOnScroll(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_SCROLL, data)
    
    def setOnZoom(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_ZOOM, data)
            
    def getOnUnload(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_UNLOAD)
        if node != None:
            return node.nodeValue
        return None
    
    def getOnAbort(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_ABORT)
        if node != None:
            return node.nodeValue
        return None
    
    def getOnError(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_ERROR)
        if node != None:
            return node.nodeValue
        return None
    
    def getOnResize(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_RESIZE)
        if node != None:
            return node.nodeValue
        return None
    
    def getOnScroll(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_SCROLL)
        if node != None:
            return node.nodeValue
        return None
    
    def getOnZoom(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ON_ZOOM)
        if node != None:
            return node.nodeValue
        return None