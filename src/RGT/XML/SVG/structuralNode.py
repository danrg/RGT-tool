from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.graphicalEventAttributes import GraphicalEventAttributes
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from types import StringType
from RGT.XML.SVG.Attribs.Error.valueParsingError import ValueParsingError

class StructuralNode(BasicSvgNode, GraphicalEventAttributes, PresentationAttributes, ClassAttribute, StyleAttribute):

    ATTRIBUTE_EXTERNALRESOURCESREQUIRED= 'externalResourcesRequired'
    
    
    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'svg')
        PresentationAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
    
    def setExternalResourcesRequired(self, data):
        allowedValues= ['true', 'false']
        
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
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNALRESOURCESREQUIRED, data)
    
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNALRESOURCESREQUIRED)
        if node != None:
            value= node.nodeValue
            if value == 'false' or value == 'False':
                return False
            elif value == 'true' or value == 'True':
                return True
            else:
                raise ValueParsingError('Could not parse the value of the ' + self.ATTRIBUTE_EXTERNALRESOURCESREQUIRE + ' attribute', value)
        return None