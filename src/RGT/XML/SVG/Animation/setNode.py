from RGT.XML.SVG.Animation.baseAnimationNode import BaseAnimationNode
from RGT.XML.SVG.Attribs.animationEventAttributes import AnimationEventAttributes
from RGT.XML.SVG.Attribs.animationAttributeTargetAttributes import AnimationAttributeTargetAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class SetNode(BaseAnimationNode, AnimationAttributeTargetAttributes, AnimationEventAttributes):
    svgNodeType = BasicSvgNode.SVG_SET_NODE

    ATTRIBUTE_TO = 'to'

    def __init__(self, ownerDoc):
        BaseAnimationNode.__init__(self, ownerDoc, 'set')
        AnimationEventAttributes.__init__(self)
        AnimationAttributeTargetAttributes.__init__(self)

    def setTo(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TO, data)

    def getTo(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TO)
        if node != None:
            return node.nodeValue
        return None