from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class GNode(BaseStructuralNode, ConditionalProcessingAttributes):
    svgNodeType = BasicSvgNode.SVG_G_NODE

    ATTRIBUTE_TRANSFORM = 'transform'


    def __init__(self, ownerDoc):
        BaseStructuralNode.__init__(self, ownerDoc, 'g')
        ConditionalProcessingAttributes.__init__(self)
        #add the groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS,
                                          self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add the individual nodes
        self._allowedSvgChildNodes.update(
            {self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE,
             self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE,
             self.SVG_FONT_NODE, self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE,
             self.SVG_MARKER_NODE, self.SVG_MASK_NODE, self.SVG_PATTERN_NODE,
             self.SVG_SCRIPT_NODE, self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE})


    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)


    def getTransform(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None