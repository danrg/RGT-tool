from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeMorphologyNode(BaseFilterNode):
    
    svgNodeType= BasicSvgNode.SVG_FE_MORPHOLOGY_NODE
    
    ATTRIBUTE_IN= 'in'
    ATTRIBUTE_OPERATOR= 'operator'
    ATTRIBUTE_RADIUS= 'radius'


    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feMorphology')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
    
    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)
    
    def setOperator(self, data):
        allowedValues= ['erode', 'dilate']
        
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_OPERATOR, data)
        
    def setRadius(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RADIUS, data)
    
    def getIn(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None
    
    def getOperator(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_OPERATOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getRadius(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_RADIUS)
        if node != None:
            return node.nodeValue
        return None