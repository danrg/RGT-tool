from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.transferFunctionElementAttributes import TransferFunctionElementAttributes


class BaseComponentTransferNode(BasicSvgNode, TransferFunctionElementAttributes):

    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
        TransferFunctionElementAttributes.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
        
        