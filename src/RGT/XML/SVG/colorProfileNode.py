from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from types import StringType

class ColorProfileNode(BasicSvgNode, XlinkAttributes):

    ATTRIBUTE_LOCAL= 'local'
    ATTRIBUTE_NAME= 'name'
    ATTRIBUTE_RENDERING_INTENT= 'rendering-intent'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'color-profile')
        XlinkAttributes.__init__(self)
    
    def setLocal(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_LOCAL, data)
    
    def setName(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_NAME, data)
    
    def setRenderingIntent(self, data):
        allowedValues= ['auto', 'perceptual', 'relative-colorimetric', 'saturation', 'absolute-colorimetric']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_RENDERING_INTENT, data)
    
    def getLocal(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_LOCAL)
        if node != None:
            return node.nodeValue
        return None
    
    def getName(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_NAME)
        if node != None:
            return node.nodeValue
        return None
    
    def getRenderingIntent(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_RENDERING_INTENT)
        if node != None:
            return node.nodeValue
        return None