from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeGaussianBlurNode(BaseFilterNode):

    svgNodeType= BasicSvgNode.SVG_FE_GAUSSIAN_BLUR_NODE

    ATTRIBUTE_IN= 'in'
    ATTRIBUTE_STD_DEVIATION= 'stdDeviation'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feGaussianBlur')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
    
    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)
    
    def setStdDeviation(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STD_DEVIATION, data)
    
    def getIn(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None
    
    def getStdDeviation(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STD_DEVIATION)
        if node != None:
            return node.nodeValue
        return None
        