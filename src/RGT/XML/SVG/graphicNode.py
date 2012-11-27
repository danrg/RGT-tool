from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class GraphicNode(BasicSvgNode):
    
    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
    
    def setStyle(self, cssCode):
        self._setNodeAttribute('style', cssCode)   
        
    def setOnClick(self, jsCode):
        self._setNodeAttribute('onclick', jsCode)
    
    def setOnMouseDown(self, jsCode):
        self._setNodeAttribute('onmousedown', jsCode)
        
    def setOnMouseUp(self, jsCode):
        self._setNodeAttribute('onmouseup', jsCode)
        
    def setOnMouseOver(self, jsCode):
        self._setNodeAttribute('onmouseover', jsCode)
        
    def setOnMouseMove(self, jsCode):
        self._setNodeAttribute('onmousemove', jsCode)
    
    def setOnMouseOut(self, jsCode):
        self._setNodeAttribute('onmouseout', jsCode)
        