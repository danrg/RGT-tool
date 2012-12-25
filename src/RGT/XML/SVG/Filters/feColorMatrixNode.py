from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeColorMatrixNode(BaseFilterNode):
   
    svgNodeType= BasicSvgNode.SVG_FE_COLOR_MATRIX_NODE
   
    ATTRIBUTE_IN= 'in'
    ATTRIBUTE_TYPE= 'type'
    ATTRIBUTE_VALUES= 'values'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feColorMatrix')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
    
    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)
    
    def setType(self, data):
        allowedValues= ['matrix', 'saturate', 'hueRotate', 'luminanceToAlpha']
        
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
                self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)
    
    def setValues(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VALUES, data)
    
    def getIn(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None
    
    def getType(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node != None:
            return node.nodeValue
        return None
    
    def getValues(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VALUES)
        if node != None:
            return node.nodeValue
        return None