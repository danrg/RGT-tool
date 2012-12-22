from xml.dom.minidom import  DOMImplementation
from xml.dom.minidom import Document
from RGT.XML.SVG.svgNode import SvgNode
from RGT.XML.SVG.gNode import GNode
from RGT.XML.SVG.defsNode import DefsNode
from RGT.XML.SVG.descNode import DescNode
from RGT.XML.SVG.titleNode import TitleNode
from RGT.XML.SVG.symbolNode import SymbolNode
from RGT.XML.SVG.imageNode import ImageNode
from RGT.XML.SVG.useNode import UseNode
from RGT.XML.SVG.switchNode import SwitchNode
from RGT.XML.SVG.styleNode import StyleNode
from RGT.XML.SVG.pathNode import PathNode
from RGT.XML.SVG.rectNode import RectNode
from RGT.XML.SVG.circleNode import CircleNode
from RGT.XML.SVG.ellipseNode import EllipseNode
from RGT.XML.SVG.lineNode import LineNode
from RGT.XML.SVG.polylineNode import PolylineNode
from RGT.XML.SVG.polygonNode import PolygonNode
from RGT.XML.SVG.textNode import TextNode
from RGT.XML.SVG.tspanNode import TspanNode
from RGT.XML.SVG.trefNode import TrefNode
from RGT.XML.SVG.textPathNode import TextPathNode
from RGT.XML.SVG.altGlyphNode import AltGlyphNode
from RGT.XML.SVG.altGlyDefNode import AltGlyphDefNode
from RGT.XML.SVG.altGlyphItemNode import AltGlyphItemNode
from RGT.XML.SVG.glyphRefNode import GlyphRefNode
from RGT.XML.SVG.markerNode import MarkerNode
from RGT.XML.SVG.colorProfileNode import ColorProfileNode
from RGT.XML.SVG.clipPathNode import ClipPathNode
from RGT.XML.SVG.maskNode import MaskNode
from RGT.XML.SVG.filterNode import FilterNode

class SvgDOMImplementation(DOMImplementation):
   
        def createSvgDocument(self):
            #namespaceURI= None
            doctype= None
            #qualifiedName= 'svg'
            
            doc = SvgDocument()
    
            element = doc.createSvgNode()
            doc.appendChild(element)
    
    
            doc.doctype = doctype
            doc.implementation = self
            return doc

class SvgDocument(Document):
    
    implementation = SvgDOMImplementation
    
    def __init__(self):
        Document.__init__(self)
    
    def createSvgNode(self):
        return SvgNode(self)
    
    def createGNode(self):
        return GNode(self)
    
    def createDefsNode(self):
        return DefsNode(self)
    
    def createDescNode(self):
        return DescNode(self)
    
    def createTitleNode(self):
        return TitleNode(self)
    
    def createSymbolNode(self):
        return SymbolNode(self)
    
    def createUseNode(self):
        return UseNode(self)
    
    def createImageNode(self):
        return ImageNode(self)
    
    def createSwitchNode(self):
        return SwitchNode(self)
    
    def createStyleNode(self):
        return StyleNode(self)
    
    def createPathNode(self):
        return PathNode(self)
    
    def createRectNode(self, x= None, y= None, height= None, width= None):
        return RectNode(self, x, y, height, width)
    
    def createCircleNode(self, cx= None, cy= None, r= None):
        return CircleNode(self, cx, cy, r)
    
    def createEllipseNode(self, rx= None, ry= None):
        return EllipseNode(self, rx, ry)
    
    def createLineNode(self, x1= None, y1= None, x2= None, y2= None):
        lineNode= LineNode(self, x1, y1, x2, y2)
        return lineNode
    
    def createPolylineNode(self, points= None):
        return PolylineNode(self, points)
    
    def createPolygonNode(self, points= None):
        return PolygonNode(self, points)
    
    def createSvgTextNode(self, x= None, y= None, text= None):
        return TextNode(self)
    
    def createTspanNode(self, x= None, y= None):
        return TspanNode(self, x, y)
    
    def createTrefNode(self):
        return TrefNode(self)
    
    def createTextPathNode(self):
        return TextPathNode(self)
    
    def createAltGlyphNode(self):
        return AltGlyphNode(self)
    
    def createAltGlyphDefNode(self):
        return AltGlyphDefNode(self)
    
    def createAltGlyphItemNode(self):
        return AltGlyphItemNode(self)
    
    def createGlyphRefNode(self):
        return GlyphRefNode(self)
    
    def createMarkerNode(self):
        return MarkerNode(self)
    
    def createColorProfileNode(self):
        return ColorProfileNode(self)
    
    def createClipPathNode(self):
        return ClipPathNode(self)
    
    def createMaskNode(self):
        return MaskNode(self)
    
    def createFilterNode(self):
        return FilterNode(self)
    
    #copy from minidom, removed the part that writes the <?xml version="1.0" ?> and the encoding
    def writexml(self, writer, indent="", addindent="", newl="",
                 encoding = None):
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)        