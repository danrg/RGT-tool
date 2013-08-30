from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeComponentTransferNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_COMPONENT_TRANSFER_NODE

    ATTRIBUTE_IN = 'in'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feComponentTransfer')
        self._allowedSvgChildNodes.update(
            {self.SVG_FE_FUNC_A_NODE, self.SVG_FE_FUNC_B_NODE, self.SVG_FE_FUNC_G_NODE, self.SVG_FE_FUNC_R_NODE})


    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None