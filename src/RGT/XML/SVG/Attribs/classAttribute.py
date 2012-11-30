from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class ClassAttribute(BasicSvgAttribute):

    ATTRIBUTE_CLASS= 'class'
    
    def setClass(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CLASS, data)
            
    def getClass(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CLASS)
        if node != None:
            return node.nodeValue
        return None
        