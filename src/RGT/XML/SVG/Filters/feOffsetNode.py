from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeOffsetNode(BaseFilterNode):
    
    svgNodeType= BasicSvgNode.SVG_FE_OFFSET_NODE
    
    ATTRIBUTE_IN= 'in'
    ATTRIBUTE_DX= 'dx'
    ATTRIBUTE_DY= 'dy'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feOffset')
    
    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)
    
    def setDx(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DX, data)
    
    def setDy(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DY, data)
    
    def getIn(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None
    
    def getDx(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DX)
        if node != None:
            return node.nodeValue
        return None
    
    def getDy(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DY)
        if node != None:
            return node.nodeValue
        return None
        