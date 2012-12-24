from RGT.XML.SVG.baseContainerNode import BaseContainerNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.graphicalEventAttributes import GraphicalEventAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class ANode(BaseContainerNode, ConditionalProcessingAttributes, GraphicalEventAttributes, XlinkAttributes):

    svgNodeType= BasicSvgNode.SVG_A_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_TRANSFORM= 'transform'
    ATTRIBUTE_TARGET= 'target'
    

    def __init__(self, ownerDoc):
        BaseContainerNode.__init__(self, ownerDoc, 'a')
        ConditionalProcessingAttributes.__init__(self)
        GraphicalEventAttributes.__init__(self)
        XlinkAttributes.__init__(self)
    
    def setExternalResourcesRequired(self, data):
        allowedValues= ['true', 'false']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)
    
    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)
            
    def setTarget(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TARGET, data)
            
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None
    
    def getTarget(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TARGET)
        if node != None:
            return node.nodeValue
        return None