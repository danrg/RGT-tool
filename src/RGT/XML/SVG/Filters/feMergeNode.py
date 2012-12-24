from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FeMergeNode(BaseFilterNode):
    
    svgNodeType= BasicSvgNode.SVG_FE_MERGE_NODE
    
    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feMerge')
        