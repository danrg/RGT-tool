from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.filterPrimitiveAttributes import FilterPrimitiveAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute


class BaseFilterNode(BasicSvgNode, PresentationAttributes, FilterPrimitiveAttributes, ClassAttribute, StyleAttribute):
    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
        PresentationAttributes.__init__(self)
        FilterPrimitiveAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        