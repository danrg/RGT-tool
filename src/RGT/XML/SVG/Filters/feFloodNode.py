from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeFloodNode(BaseFilterNode):

    svgNodeType= BasicSvgNode.SVG_FE_FLOOD_NODE

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feFlood')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE, self.SVG_ANIMATE_COLOR_NODE})
        