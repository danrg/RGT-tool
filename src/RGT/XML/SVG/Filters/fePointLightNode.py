from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType

class FePointLightNode(BasicSvgNode, PositionAttributes):
    
    svgNodeType= BasicSvgNode.SVG_FE_POINT_LIGHT_NODE
    
    ATTRIBUTE_Z= 'z'

    def __init__(self, ownerDoc, x= None, y= None, z= None):
        BasicSvgNode.__init__(self, ownerDoc, 'fePointLight')
        PositionAttributes.__init__(self)
        self.setX(x)
        self.setY(y)
        self.setZ(z)
    
    def setZ(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Z, data)
    
    def getZ(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_Z)
        if node != None:
            return node.nodeValue
        return None