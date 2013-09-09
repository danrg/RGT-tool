from RGT.XML.SVG.Filters.baseComponentTransferNode import BaseComponentTransferNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeFuncANode(BaseComponentTransferNode):
    svgNodeType = BasicSvgNode.SVG_FE_FUNC_A_NODE

    def __init__(self, ownerDoc):
        BaseComponentTransferNode.__init__(self, ownerDoc, 'feFuncA')
        