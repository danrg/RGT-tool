from RGT.XML.SVG.Animation.baseAnimationNode import BaseAnimationNode
from RGT.XML.SVG.Attribs.animationEventAttributes import AnimationEventAttributes
from RGT.XML.SVG.Attribs.animationAttributeTargetAttributes import AnimationAttributeTargetAttributes
from RGT.XML.SVG.Attribs.animationValueAttributes import AnimationValueAttributes
from RGT.XML.SVG.Attribs.animationAdditionAttributes import AnimationAdditionAttributes
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class AnimateTransformNode(BaseAnimationNode, AnimationAdditionAttributes, AnimationAttributeTargetAttributes,
                           AnimationEventAttributes, AnimationValueAttributes):
    svgNodeType = BasicSvgNode.SVG_ANIMATE_TRANSFORM_NODE

    ATTRIBUTE_TYPE = 'type'

    def __init__(self, ownerDoc):
        BaseAnimationNode.__init__(self, ownerDoc, 'animateTransform')
        AnimationAdditionAttributes.__init__(self)
        AnimationAttributeTargetAttributes.__init__(self)
        AnimationEventAttributes.__init__(self)
        AnimationValueAttributes.__init__(self)


    def setType(self, data):
        allowedValues = ['translate', 'scale', 'rotate', 'skewX', 'skewY']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)

    def getType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node is not None:
            return node.nodeValue
        return None