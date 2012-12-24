'''
This file contains all the needed functions to create the svg xml nodes
'''
from xml.dom.minidom import Document, DOMImplementation
#from RGT.XML.SVG.graphicNode import GraphicNode
from RGT.XML.SVG.scriptNode import ScriptNode
from RGT.XML.SVG.svgNode import SvgNode
from RGT.XML.SVG.descNode import DescNode

#class copied from minidom
class SvgDOMImplementation(DOMImplementation):

    def createSvgDocument(self):
        #namespaceURI= None
        doctype= None
        #qualifiedName= 'svg'
        
        doc = SvgDocument()

        element = doc.createSvgNode()
        doc.appendChild(element)


        doc.doctype = doctype
        doc.implementation = self
        return doc
       

#function copied from minidom
def _nssplit(qualifiedName):
    fields = qualifiedName.split(':', 1)
    if len(fields) == 2:
        return fields
    else:
        return (None, fields[0])

class SvgDocument (Document):
    
    implementation = SvgDOMImplementation()
    
    def __init__(self):
        Document.__init__(self)
    
#    def createLineNode(self, x1= None, y1= None, x2= None, y2= None):
#        #Document.__init__(self)
#        lineNode= LineNode(self, x1, y1, x2, y2)
#        return lineNode
    
    def createCssStyleNode(self, cssData):
        cssNode= CssStyleNode(self, cssData)
        return cssNode
    
    def createJavaScriptNode(self, jsData):
        jsNode= JavaScriptNode(self, jsData)
        return jsNode
    
    def createSvgNode(self):
        return SvgNode(self)
    
    def createDescNode(self):
        return DescNode(self)
    
    #copy from minidom, removed the part that writes the <?xml version="1.0" ?> and the encoding
    def writexml(self, writer, indent="", addindent="", newl="",
                 encoding = None):
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)
     
#class LineNode(GraphicNode):
#    
#    def __init__(self, ownerDoc, x1= None, y1= None, x2= None, y2= None):
#        GraphicNode.__init__(self, ownerDoc, 'line')
#        if (x1 or x2 or y1 or y2) and ownerDoc == None:
#            raise Exception('ownerDoc can not be None went trying to set line parameters')
#        self.setX1(x1)
#        self.setY1(y1)
#        self.setX2(x2)
#        self.setY2(y2)
#    
#    def setX1(self,  x):
#        if x != None and x >= 0:
#            self._setNodeAttribute('x1', str(x))
#                
#    def setY1(self, y):
#        if y != None and y >= 0:
#            self._setNodeAttribute('y1', str(y))
#            
#    def setX2(self, x):
#        if x != None and x >= 0:
#            self._setNodeAttribute('x2', str(x))
#    
#    def setY2(self, y):
#        if y != None and y >= 0:
#            self._setNodeAttribute('y2', str(y))
#            
#    def getX1(self):
#        x1Node= self._getNodeAttribute('x1')
#        if x1Node != None and x1Node != '':
#            return int(x1Node.nodeValue)
#        
#    def getY1(self):
#        y1Node= self._getNodeAttribute('y1')
#        if y1Node != None and y1Node != '':
#            return int(y1Node.nodeValue)
#    
#    def getX2(self):
#        x2Node= self._getNodeAttribute('x2')
#        if x2Node != None and x2Node != '':
#            return int(x2Node.nodeValue)
#    
#    def getY2(self):
#        y2Node= self._getNodeAttribute('y2')
#        if y2Node != None and y2Node != '':
#            return int(y2Node.nodeValue)

class CssStyleNode(ScriptNode):
    
    def __init__(self, ownerDoc, cssData= None):
        ScriptNode.__init__(self, 'style')
        if not ownerDoc:
            raise ValueError('ownderDoc can not be None')
        typeNode= self.ownerDocument.createAttribute('type')
        typeNode.nodeValue= 'text/css'
        self.setAttributeNode(typeNode)
        
        if cssData != None:
            self.setData(cssData)

class JavaScriptNode(ScriptNode):
    
    TEXT_JAVASCRIPT= 'text/javascript'
    TEXT_ECMASCRIPT= 'text/ecmascript'
    
    
    def __init__(self, ownerDoc, jsData= None):
        ScriptNode.__init__(self, ownerDoc, 'script')
        if not ownerDoc:
            raise ValueError('ownderDoc can not be None')
        self.setType(self.TEXT_JAVASCRIPT)
        
        if jsData != None:
            self.setData(jsData)
            
    
    def setType(self, typeData):
        self._setNodeAttribute('type', typeData)
            