from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType

class MyClass(BaseFilterNode):
    
    ATTRIBUTE_IN= 'in'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feComponentTransfer')
        
    
    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)
    
    def getIn(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None