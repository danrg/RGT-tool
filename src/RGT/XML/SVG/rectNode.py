from RGT.XML.SVG.baseShapeNode import BaseShapeNode
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class RectNode(BaseShapeNode, PositionAttributes, SizeAttributes):

    svgNodeType= BasicSvgNode.SVG_RECT_NODE

    ATTRIBUTE_RX= 'rx'
    ATTRIBUTE_RY= 'ry'
    
    def __init__(self, ownerDoc, x= None, y= None, height= None, width= None):
        BaseShapeNode.__init__(self, ownerDoc, 'rect')
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        self.setX(x)
        self.setY(y)
        self.setHeight(height)
        self.setWidth(width)
    
    def setRx(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RX, data)
    
    def setRy(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RY, data)
    
    def getRx(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_RX)
        if node != None:
            return node.nodeValue
        return None
    
    def getRy(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_RY)
        if node != None:
            return node.nodeValue
        return None
        