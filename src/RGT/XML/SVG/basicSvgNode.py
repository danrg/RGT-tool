from xml.dom.minidom import Element
from RGT.XML.SVG.Attribs.coreAttributes import CoreAttributes
from xml.dom import Node

class BasicSvgNode(Element, CoreAttributes):
    
    allowNoSvgChildNode= False
    svgNodeType= None
    _allowedSvgChildNodes= []
    
    #Svg node definitions
    SVG_SVG_NODE= 1
    SVG_G_NODE= 2
    SVG_DEFS_NODE= 3
    SVG_DESC_NODE= 4
    SVG_TITLE_NODE= 5
    SVG_SYMBOL_NODE= 6
    SVG_USE_NODE= 7
    SVG_IMAGE_NODE= 8
    SVG_SWITCH_NODE= 9
    SVG_STYLE_NODE= 10
    SVG_PATH_NODE= 11
    SVG_RECT_NODE= 12
    SVG_CIRCLE_NODE= 13
    SVG_ELLIPSE_NODE= 14
    SVG_LINE_NODE= 15
    SVG_POLYLINE_NODE= 16
    SVG_POLYGON_NODE= 17
    SVG_TEXT_NODE= 18
    SVG_TSPAN_NODE= 19
    SVG_TREF_NODE= 20
    SVG_TEX_PATH_NODE= 21
    SVG_ALT_GLYPH_NODE= 22
    SVG_ALT_GLYPH_DEF_NODE= 23
    SVG_ALT_GLYPH_ITEM_NODE= 24
    SVG_GLYPH_REF_NODE= 25
    SVG_MARKER_NODE= 26
    SVG_COLOR_PROFILE_NODE= 27
    SVG_CLIP_PATH_NODE= 28
    SVG_MASK_NODE= 29
    SVG_FILTER_NODE= 30
    
    def __init__(self, ownerDoc, tagName):
        Element.__init__(self, tagName)
        CoreAttributes.__init__(self)
        if ownerDoc:
            self.ownerDocument= ownerDoc
        
    

    def _nodeCodeToText(self, code):
        
        codes= {Node.ELEMENT_NODE: 'ELEMENT_NODE', Node.ATTRIBUTE_NODE: 'ATTRIBUTE_NODE', Node.TEXT_NODE: 'TEXT_NODE', Node.CDATA_SECTION_NODE: 'CDATA_SECTION_NODE', Node.ENTITY_REFERENCE_NODE: 'ENTITY_REFERENCE_NODE', Node.ENTITY_NODE: 'ENTITY_NODE', Node.PROCESSING_INSTRUCTION_NODE: 'PROCESSING_INSTRUCTION_NODE', Node.COMMENT_NODE: 'COMMENT_NODE', Node.DOCUMENT_NODE: 'DOCUMENT_NODE', Node.DOCUMENT_TYPE_NODE: 'DOCUMENT_TYPE_NODE ', Node.DOCUMENT_FRAGMENT_NODE: 'DOCUMENT_FRAGMENT_NODE', Node.NOTATION_NODE: 'NOTATION_NODE'}
        
        if codes.has_key(code) == True:
            return codes[code]
        return None