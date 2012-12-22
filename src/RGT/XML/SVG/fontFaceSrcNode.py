from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FontFaceSrcNode(BasicSvgNode):

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face-src')
        