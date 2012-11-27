from xml.dom.minidom import Element
from RGT.XML.SVG.Attribs.coreAttributes import CoreAttributes

class BasicSvgNode(Element, CoreAttributes):
    
    def __init__(self, ownerDoc, tagName):
        Element.__init__(self, tagName)
        CoreAttributes.__init__(self)
        if ownerDoc:
            self.ownerDocument= ownerDoc
        
    
