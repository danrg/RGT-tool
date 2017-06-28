from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from xml.dom.minidom import Node


class BaseScriptNode(BasicSvgNode):
    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
        self.allowAllSvgNodesAsChildNodes = True

    def setData(self, data):

        if data is not None:
            foundCDataNode = False

            #check to see if we have a child node (text node) 
            if len(self.childNodes) >= 1:
                for child in self.childNodes:
                    #search for the first cdata node and interpret it as being the node that contains the data
                    if child.nodeType == Node.CDATA_SECTION_NODE:
                        child.data = data
                        foundCDataNode = True
                        break

                if foundCDataNode == False:
                    textNode = self.ownerDocument.createCDATASection(data)
                    self.appendChild(textNode)
            else:
                textNode = self.ownerDocument.createCDATASection(data)
                self.appendChild(textNode)

    def getData(self):

        if len(self.childNodes) >= 1:
            for child in self.childNodes:
                #search for the first text node and interpret it as being the node that contains the css data
                if child.nodeType == Node.CDATA_SECTION_NODE:
                    return child.data

        return None

    def appendChild(self, node):

        if node.nodeType == Node.CDATA_SECTION_NODE:
            if len(self.childNodes) == 0:
                BasicSvgNode.appendChild(self, node)
            else:
                raise Exception('only one CDATA node can be present, use the getData and setData to change the data')
        else:
            raise Exception('only CDATA nodes can be added')
        