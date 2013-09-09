from RGT.XML.SVG.baseContainerNode import BaseContainerNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class MarkerNode(BaseContainerNode):
    svgNodeType = BasicSvgNode.SVG_MARKER_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'
    ATTRIBUTE_VIEW_BOX = 'viewBox'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO = 'preserveAspectRatio'
    ATTRIBUTE_REF_X = 'refX'
    ATTRIBUTE_REF_Y = 'refY'
    ATTRIBUTE_MARKER_UNITS = 'markerUnits'
    ATTRIBUTE_MARKER_WIDTH = 'markerWidth'
    ATTRIBUTE_MARKER_HEIGHT = 'markerHeight'
    ATTRIBUTE_ORIENT = 'orient'

    def __init__(self, ownderDoc):
        BaseContainerNode.__init__(self, ownderDoc, 'marker')
        #add the groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS,
                                          self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS,
                                          self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add the individual nodes
        self._allowedSvgChildNodes.update(
            {self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE,
             self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE,
             self.SVG_FONT_NODE, self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE,
             self.SVG_MARKER_NODE, self.SVG_MASK_NODE, self.SVG_PATTERN_NODE,
             self.SVG_SCRIPT_NODE, self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE})


    def setExternalResourcesRequired(self, data):
        allowedValues = ['true', 'false']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)

    def setViewBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEW_BOX, data)

    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO, data)

    def setRefX(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REF_X, data)

    def setRefY(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REF_Y, data)

    def setMarkerUnits(self, data):
        allowedValues = ['strokeWidth', 'userSpaceOnUse']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_MARKER_UNITS, data)

    def setMarkerWidth(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_WIDTH, data)

    def setMarkerHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_HEIGHT, data)

    def setOrient(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ORIENT, data)

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None

    def getViewBox(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_VIEW_BOX)
        if node != None:
            return node.nodeValue
        return None

    def getPreserveAspectRatio(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO)
        if node != None:
            return node.nodeValue
        return None

    def getRefX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_REF_X)
        if node != None:
            return node.nodeValue
        return None

    def getRefY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_REF_Y)
        if node != None:
            return node.nodeValue
        return None

    def getMarkerUnits(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MARKER_UNITS)
        if node != None:
            return node.nodeValue
        return None

    def getMarkerWidth(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MARKER_WIDTH)
        if node != None:
            return node.nodeValue
        return None

    def getMarkerHeight(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MARKER_HEIGHT)
        if node != None:
            return node.nodeValue
        return None

    def getOrient(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ORIENT)
        if node != None:
            return node.nodeValue
        return None