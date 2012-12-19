from RGT.XML.SVG.baseInformationNode import BaseInformationNode

class TitleNode(BaseInformationNode):

    def __init__(self, ownerDoc):
        BaseInformationNode.__init__(self, ownerDoc, 'title')
        