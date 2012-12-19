from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Errors.wrongNodeType import WrongNodeType
from xml.dom import Node
from types import StringType

class BaseInformationNode(BasicSvgNode):
    
    '''
    The children of this class are allowed to have as child a text node or any other type of nodes, including a different marked-up text.
    If the user wants to use text only he can use the set and get text functions. If not, he can use the minidom as usual
    to add other nodes to the node classes that implements this class. 
    '''


    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)


    def setText(self, text):
        if type(text) != StringType:
            text= str(text)
            
        #check to see if we have a child node that is a text node, if we have that, reuse it with a new text.
        #in case we don't have any text nodes create a new one
        #and in case we have a node(s) that is not a text node, remove it
        if self.hasChildNodes() == True:
            if self.childNodes[0].nodeType == Node.TEXT_NODE:
                self.childNodes[0].nodeValue= text
            else:
                i= len(self.childNodes)
                while i >= 1:
                    self.removeChild(self.childNodes[i - 1])
                    i-= 1
                self.appendChild(self.ownerDocument.createTextNode(text))
        else:
            self.appendChild(self.ownerDocument.createTextNode(text))
    
    def getText(self):
        if len(self.childNodes) > 0:
            if self.hasChildNodes() == True:
                if self.childNodes[0].nodeType == Node.TEXT_NODE:
                    return self.childNodes[0].nodeValue
                else:
                    raise WrongNodeType('Expecting a TextNode but ' + self._nodeCodeToText(self.childNodes[0].nodeType) + ' was found')
        return None 
    
    #this function is used to check if the 1st child is a TextNode
    def isChildTextNode(self):
        
        if self.hasChildNodes() == True:
            if self.childNodes[0].nodeType == Node.TEXT_NODE:
                return True
        return False
        