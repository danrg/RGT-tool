from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType

class FeGaussianBlurNode(BaseFilterNode):

    ATTRIBUTE_IN= 'in'
    ATTRIBUTE_STD_DEVIATION= 'stdDeviation'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feGaussianBlur')
    
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
        