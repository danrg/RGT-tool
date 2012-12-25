from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType

class FeSpotLightNode(BasicSvgNode, PositionAttributes):
    
    svgNodeType= BasicSvgNode.SVG_FE_SPOT_LIGHT_NODE
    
    ATTRIBUTE_Z= 'z'
    ATTRIBUTE_POINTS_AT_X= 'pointsAtX'
    ATTRIBUTE_POINTS_AT_Y= 'pointsAtY'
    ATTRIBUTE_POINTS_AT_Z= 'pointsAtZ'
    ATTRIBUTE_SPECULAR_EXPONENT= 'specularExponent'
    ATTRIBUTE_LIMITING_CONE_ANGLE= 'limitingConeAngle'

    def __init__(self, ownerDoc, x= None, y= None, z= None, specularExponent= None, limitingConeAngle= None):
        BasicSvgNode.__init__(self, ownerDoc, 'feSpotLight')
        PositionAttributes.__init__(self)
        self.setX(x)
        self.setY(y)
        self.setZ(z)
        self.setSpecularExponent(specularExponent)
        self.setLimitingConeAngle(limitingConeAngle)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
    
    def setZ(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Z, data)
            
    def setPointsAtX(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_POINTS_AT_X, data)
    
    def setPointsAtY(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_POINTS_AT_Y, data)
    
    def setPointsAtZ(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_POINTS_AT_Z, data)
    
    def setSpecularExponent(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SPECULAR_EXPONENT, data)
    
    def setLimitingConeAngle(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_LIMITING_CONE_ANGLE, data)
        
    def getZ(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_Z)
        if node != None:
            return node.nodeValue
        return None
    
    def getPointsAtX(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_POINTS_AT_X)
        if node != None:
            return node.nodeValue
        return None
    
    def getPointsAtY(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_POINTS_AT_Y)
        if node != None:
            return node.nodeValue
        return None
    
    def getPointsAtZ(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_POINTS_AT_Z)
        if node != None:
            return node.nodeValue
        return None
    
    def getSpecularExponent(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_SPECULAR_EXPONENT)
        if node != None:
            return node.nodeValue
        return None
    
    def getLimitingConeAngle(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_LIMITING_CONE_ANGLE)
        if node != None:
            return node.nodeValue
        return None