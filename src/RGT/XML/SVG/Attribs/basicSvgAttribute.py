"""
    ############  Important  ############
    
    To be able to use the attributes one of the sub classes must be a child of xml.dom.minidom.Element 
    
"""


class BasicSvgAttribute(object):
    def _setNodeAttribute(self, attribName, data):
        attribNode = self.getAttributeNode(attribName)
        if attribNode == None:
            attribNode = self.ownerDocument.createAttribute(attribName)
            self.setAttributeNode(attribNode)

        attribNode.nodeValue = data

    def _getNodeAttribute(self, attribName):
        return self.getAttributeNode(attribName)