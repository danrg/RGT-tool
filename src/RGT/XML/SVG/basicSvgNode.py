from xml.dom.minidom import Element
from RGT.XML.SVG.Attribs.coreAttributes import CoreAttributes
from xml.dom import Node

class BasicSvgNode(Element, CoreAttributes):
    
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