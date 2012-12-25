from RGT.XML.SVG.baseInformationNode import BaseInformationNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class TitleNode(BaseInformationNode):

    svgNodeType= BasicSvgNode.SVG_TITLE_NODE

    def __init__(self, ownerDoc):
        BaseInformationNode.__init__(self, ownerDoc, 'title')
        self.allowAllSvgNodesAsChildNodes= True
        