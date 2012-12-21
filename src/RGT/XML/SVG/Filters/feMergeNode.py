from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode

class FeMergeNode(BaseFilterNode):

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feMerge')
        