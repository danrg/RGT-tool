from RGT.XML.SVG.Animation.baseAnimationNode import BaseAnimationNode
from RGT.XML.SVG.Attribs.animationEventAttributes import AnimationEventAttributes
from RGT.XML.SVG.Attribs.animationValueAttributes import AnimationValueAttributes
from RGT.XML.SVG.Attribs.animationAdditionAttributes import AnimationAdditionAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class AnimateMotionNode(BaseAnimationNode, AnimationAdditionAttributes, AnimationEventAttributes,
                        AnimationValueAttributes):
    svgNodeType = BasicSvgNode.SVG_ANIMATE_MOTION_NODE

    ATTRIBUTE_PATH = 'path'
    ATTRIBUTE_KEY_POINTS = 'keyPoints'
    ATTRIBUTE_ROTATE = 'rotate'
    ATTRIBUTE_ORIGIN = 'origin'

    def __init__(self, ownerDoc):
        BaseAnimationNode.__init__(self, ownerDoc, 'animateMotion')
        AnimationAdditionAttributes.__init__(self)
        AnimationEventAttributes.__init__(self)
        AnimationValueAttributes.__init__(self)
        #add individual nodes
        self._allowedSvgChildNodes.add(self.SVG_MPATH_NODE)

    def setPath(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PATH, data)

    def setKeyPoints(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KEY_POINTS, data)

    def setRotate(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ROTATE, data)

    def setOrigin(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ORIGIN, data)

    def getPath(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_PATH)
        if node != None:
            return node.nodeValue
        return None

    def geKeyPoints(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_KEY_POINTS)
        if node != None:
            return node.nodeValue
        return None

    def getRotate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ROTATE)
        if node != None:
            return node.nodeValue
        return None

    def getOrigin(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ORIGIN)
        if node != None:
            return node.nodeValue
        return None