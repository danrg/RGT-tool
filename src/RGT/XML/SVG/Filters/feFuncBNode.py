from RGT.XML.SVG.Filters.baseComponentTransferNode import BaseComponentTransferNode

class FeFuncBNode(BaseComponentTransferNode):

    def __init__(self, ownerDoc):
        BaseComponentTransferNode.__init__(self, ownerDoc, 'feFuncB')
        