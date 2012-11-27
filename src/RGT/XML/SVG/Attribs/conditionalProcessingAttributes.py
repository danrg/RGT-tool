from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class ConditionalProcessingAttributes(BasicSvgAttribute):

    ATTRIBUTE_REQUIRED_FEATURES= 'requiredFeatures'
    ATTRIBUTE_REQUIRED_EXTENSIONS= 'requiredExtensions'
    ATTRIBUTE_SYSTEM_LANGUAGE= 'systemLanguage'
    
    def setRequiredFeatures(self, features):
        if features != None:
            if type(features) != StringType:
                raise TypeError('extensions must be a string with a list of URLs separated by a space')
            self._setNodeAttribute(self.ATTRIBUTE_REQUIRED_FEATURES, features)
    
    def setRequiredExtension(self, extensions):
        if extensions != None:
            if type(extensions) != StringType:
                raise TypeError('extensions must be a string with a list of URLs separated by a space')
            self._setNodeAttribute(self.ATTRIBUTE_REQUIRED_EXTENSIONS, extensions)
    
    def setSystemLanguage(self, sysLanguage):
        if sysLanguage != None:
            if type(sysLanguage) != StringType:
                raise TypeError('extensions must be a string with a list of URLs separated by a comma')
            self._setNodeAttribute(self.ATTRIBUTE_SYSTEM_LANGUAGE, sysLanguage)
            
            
    def getRequiredFeatures(self):
        featureNode= self._getNodeAttribute(self.ATTRIBUTE_REQUIRED_FEATURES)
        if featureNode != None:
            return featureNode.nodeValue
        return None
    
    
    def getRequiredExtension(self):
        extensionNode= self._getNodeAttribute(self.ATTRIBUTE_REQUIRED_EXTENSIONS)
        if extensionNode != None:
            return extensionNode.nodeValue
        return None
    
    def getSystemLanguage(self):
        languageNode= self._getNodeAttribute(self.ATTRIBUTE_SYSTEM_LANGUAGE)
        if languageNode != None:
            return languageNode.nodeValue
        return None
        