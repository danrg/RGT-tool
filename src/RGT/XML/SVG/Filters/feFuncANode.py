from RGT.XML.SVG.Filters.baseComponentTransferNode import BaseComponentTransferNode

class FeFuncANode(BaseComponentTransferNode):

    def __init__(self, ownerDoc):
        BaseComponentTransferNode.__init__(self, ownerDoc, 'feFuncA')
        