from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class MetadataNode(BasicSvgNode):
    
    svgNodeType= BasicSvgNode.SVG_METADATA_NODE

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'metadata')
        self.allowAllSvgNodesAsChildNodes= True
        