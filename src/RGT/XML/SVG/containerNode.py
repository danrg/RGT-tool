from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute

class ContainerNode(BasicSvgNode, PresentationAttributes, StyleAttribute, ClassAttribute):

    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
        PresentationAttributes.__init__(self)
        StyleAttribute.__init__(self)
        ClassAttribute.__init__(self)
        