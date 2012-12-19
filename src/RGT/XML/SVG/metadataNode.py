from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class MetadataNode(BasicSvgNode):

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'metadata')
        