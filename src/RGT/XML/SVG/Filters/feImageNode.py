from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeImageNode(BaseFilterNode, XlinkAttributes):

    svgNodeType= BasicSvgNode.SVG_FE_IMAGE_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO= 'preserveAspectRatio'     


    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feImage')
        XlinkAttributes.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE, self.SVG_ANIMATE_TRANSFORM_NODE})
        
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
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO, data)
    
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO)
        if node != None:
            return node.nodeValue
        return None