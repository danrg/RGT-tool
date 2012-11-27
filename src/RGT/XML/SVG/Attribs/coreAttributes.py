from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class CoreAttributes(BasicSvgAttribute):

    ATTRIBUTE_ID= 'id'
    ATTRIBUTE_XML_BASE= 'xml:base'
    ATTRIBUTE_XML_LANG= 'xml:lang'
    ATTRIBUTE_XML_SPACE= 'xml:space'

    def setId(self, idData= None):
        if idData != None:
            if type(idData) is not StringType:
                idData= str(idData)
            self._setNodeAttribute(self.ATTRIBUTE_ID, idData)
        
    def setXmlBase(self, xmlBase= None):
        if xmlBase != None:
            if type(xmlBase) is not StringType:
                xmlBase= str(xmlBase)
            self._setNodeAttribute(self.ATTRIBUTE_XML_BASE, xmlBase)
    
    def setXmlLang(self, xmlLang= None):
        if xmlLang != None:
            if type(xmlLang) is not StringType:
                xmlLang= str(xmlLang)
            self._setNodeAttribute(self.ATTRIBUTE_XML_LANG, xmlLang)
    
    def setXmlSpace(self, xmlSpace= None):
        if xmlSpace != None:
            if xmlSpace == 'default' or xmlSpace == 'preserve':
                self._setNodeAttribute(self.ATTRIBUTE_XML_SPACE, xmlSpace)
            else:
                raise ValueError('the ' + self.ATTRIBUTE_XML_SPACE + ' attribute can only be set to default or preserve')
            
    def getId(self):
        idNode= self._getNodeAttribute(self.ATTRIBUTE_ID)
        if idNode != None:
            return idNode.nodeValue
        return None
    
    def getXmlBase(self):
        xmlBaseNode= self._getNodeAttribute(self.ATTRIBUTE_XML_BASE)
        if xmlBaseNode != None:
            return xmlBaseNode.nodeValue
        return None
    
    def getXmlLang(self):
        xmlLangNode= self._getNodeAttribute(self.ATTRIBUTE_XML_LANG)
        if xmlLangNode != None:
            return xmlLangNode.nodeValue
        return None
    
    def getXmlSpace(self):
        xmlSpaceNode= self._getNodeAttribute(self.ATTRIBUTE_XML_SPACE)
        if xmlSpaceNode != None:
            return xmlSpaceNode.nodeValue
        return None
        