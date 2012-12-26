from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.documentEventAttributes import DocumentEventAttributes
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class SvgNode(BaseStructuralNode, PositionAttributes, SizeAttributes, ConditionalProcessingAttributes, DocumentEventAttributes):

    svgNodeType= BasicSvgNode.SVG_SVG_NODE
    
    ATTRIBUTE_VIEWBOX= 'viewBox'
    ATTRIBUTE_PRESERVEASPECTRATIO= 'preserveAspectRatio'
    ATTRIBUTE_ZOOMANDPAN= 'zoomAndPan'
    ATTRIBUTE_VERSION= 'version'
    ATTRIBUTE_BASEPROFILE= 'baseProfile'
    ATTRIBUTE_CONTENTSCRIPTTYPE= 'contentScriptType'
    ATTRIBUTE_CONTENTSTYLETYPE= 'contentStyleType'
    ATTRIBUTE_XMLNS= 'xmlns'


    def __init__(self, ownerDoc):
        BaseStructuralNode.__init__(self, ownerDoc, 'svg')
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        ConditionalProcessingAttributes.__init__(self)
        DocumentEventAttributes.__init__(self)
        #add the groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS, self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add the individual nodes
        self._allowedSvgChildNodes.update({self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE, self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE,
                                           self.SVG_FONT_NODE, self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE, self.SVG_MARKER_NODE, self.SVG_MASK_NODE, self.SVG_PATTERN_NODE,
                                           self.SVG_SCRIPT_NODE, self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE
                                           })   
    def setViewBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEWBOX, data)
            
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO, data)
    
    def setZoomAndPan(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ZOOMANDPAN, data)
    
    def setVersion(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERSION, data)
            
    def setBaseProfile(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BASEPROFILE, data)
    
    def setContentScriptType(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CONTENTSCRIPTTYPE, data)
            
    def setContentStyleType(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CONTENTSTYLETYPE, data)
            
    def setXmlns(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XMLNS, data)
    
    def getViewBox(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VIEWBOX)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO)
        if node != None:
            return node.nodeValue
        return None
    
    def getZoomAndPan(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ZOOMANDPAN)
        if node != None:
            return node.nodeValue
        return None
    
    def getVersion(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VERSION)
        if node != None:
            return node.nodeValue
        return None
    
    def getBaseProfile(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_BASEPROFILE)
        if node != None:
            return node.nodeValue
        return None
    
    def getContentScriptType(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CONTENTSCRIPTTYPE)
        if node != None:
            return node.nodeValue
        return None
    
    def getContentStyleType(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CONTENTSTYLETYPE)
        if node != None:
            return node.nodeValue
        return None
    
    def getXmlns(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_XMLNS)
        if node != None:
            return node.nodeValue
        return None