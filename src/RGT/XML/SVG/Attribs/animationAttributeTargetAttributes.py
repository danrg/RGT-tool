from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class AnimationAttributeTargetAttributes(BasicSvgAttribute):
    
    ATTRIBUTE_ATTRIBUTE_TYPE= 'attributeType'
    ATTRIBUTE_ATTRIBUTE_NAME= 'attributeName'

    def __init__(self):
        BasicSvgAttribute.__init__(self)
    
    def setAttributeName(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ATTRIBUTE_NAME, data)
    
    def setAttributeType(self, data):
        allowedValues= ['CSS', 'XML', 'auto']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ATTRIBUTE_TYPE, data)
    
    def getAttributeName(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ATTRIBUTE_NAME)
        if node != None:
            return node.nodeValue
        return None
    
    def getAttributeType(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ATTRIBUTE_TYPE)
        if node != None:
            return node.nodeValue
        return None
        