from RGT.XML.SVG.baseTextNode import BaseTextNode
from types import StringType
from xml.dom import Node

class BaseEditableTextNode(BaseTextNode):

    def __init__(self, ownerDoc, tagName):
        BaseTextNode.__init__(self, ownerDoc, tagName)
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS)
    
    def setText(self, text):
        if text != None:
            textNode= None
            if type(text) != StringType:
                text= str(text)
            
            if self.hasChildNodes() == True:
                for child in self.childNodes:
                    if child.nodeType == Node.CDATA_SECTION_NODE or child.nodeType == Node.TEXT_NODE:
                        textNode= child
                        break
            if textNode == None:
                textNode= self.ownerDocument.createTextNode('')
                self.appendChild(textNode)
            
            textNode.nodeValue= text
            
    
    def getText(self):
        for child in self.childNodes:
            if child.nodeType == Node.CDATA_SECTION_NODE or child.nodeType == Node.TEXT_NODE:
                return child.nodeValue
            return None
                        
                    
        
        