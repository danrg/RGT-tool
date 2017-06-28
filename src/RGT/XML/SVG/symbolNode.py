from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class SymbolNode(BaseStructuralNode):
    svgNodeType = BasicSvgNode.SVG_SYMBOL_NODE

    ATTRIBUTE_PRESERVEASPECTRATIO = 'preserveAspectRatio'
    ATTRIBUTE_VIEWBOX = 'viewBox'


    def __init__(self, ownderDoc):
        BaseStructuralNode.__init__(self, ownderDoc, 'symbol')
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS,
                                          self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS,
                                          self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add indivudual elements
        self._allowedSvgChildNodes.update(
            {self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE,
             self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE, self.SVG_FONT_NODE,
             self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE, self.SVG_MARKER_NODE,
             self.SVG_MASK_NODE, self.SVG_PATTERN_NODE, self.SVG_SCRIPT_NODE,
             self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE})


    def setPreserveAspectRatio(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO, data)

    def setViewBox(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEWBOX, data)

    def getViewBox(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_VIEWBOX)
        if node is not None:
            return node.nodeValue
        return None

    def getPreserveAspectRatio(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO)
        if node is not None:
            return node.nodeValue
        return None