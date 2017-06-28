from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType


class FeMergeNodeNode(BasicSvgNode):
    svgNodeType = BasicSvgNode.SVG_FE_MERGE_NODE_NODE

    ATTRIBUTE_IN = 'in'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'feMergeNode')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setIn(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node is not None:
            return node.nodeValue
        return None