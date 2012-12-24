from RGT.XML.SVG.Animation.baseAnimationNode import BaseAnimationNode
from RGT.XML.SVG.Attribs.animationEventAttributes import AnimationEventAttributes
from RGT.XML.SVG.Attribs.animationAttributeTargetAttributes import AnimationAttributeTargetAttributes
from RGT.XML.SVG.Attribs.animationValueAttributes import AnimationValueAttributes
from RGT.XML.SVG.Attribs.animationAdditionAttributes import AnimationAdditionAttributes
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class AnimateColorNode(BaseAnimationNode, AnimationAdditionAttributes, AnimationAttributeTargetAttributes, AnimationEventAttributes, AnimationValueAttributes, PresentationAttributes):

    svgNodeType= BasicSvgNode.SVG_ANIMATE_COLOR_NODE

    def __init__(self, ownerDoc):
        BaseAnimationNode.__init__(self, ownerDoc, 'animateColor')
        AnimationAdditionAttributes.__init__(self)
        AnimationAttributeTargetAttributes.__init__(self)
        AnimationEventAttributes.__init__(self)
        AnimationValueAttributes.__init__(self)
        PresentationAttributes.__init__(self)
        