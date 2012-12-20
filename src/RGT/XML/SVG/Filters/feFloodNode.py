from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode

class FeFloodNode(BaseFilterNode):

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feFlood')
        