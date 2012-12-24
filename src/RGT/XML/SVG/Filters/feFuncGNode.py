from RGT.XML.SVG.Filters.baseComponentTransferNode import BaseComponentTransferNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeFuncGNode(BaseComponentTransferNode):

    svgNodeType= BasicSvgNode.SVG_FE_FUNC_G_NODE

    def __init__(self, ownerDoc):
        BaseComponentTransferNode.__init__(self, ownerDoc, 'feFuncG')
        