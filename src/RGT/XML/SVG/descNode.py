from RGT.XML.SVG.baseInformationNode import BaseInformationNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class DescNode(BaseInformationNode):
    
    svgNodeType= BasicSvgNode.SVG_DESC_NODE

    def __init__(self, ownerDoc):
        BaseInformationNode.__init__(self, ownerDoc, 'desc')
        self.allowAllSvgNodesAsChildNodes= True
        
    

            
        