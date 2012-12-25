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
#filters
from RGT.XML.SVG.Filters.feDistantLightNode import FeDistantLightNode
from RGT.XML.SVG.Filters.fePointLightNode import FePointLightNode
from RGT.XML.SVG.Filters.feSpotLightNode import FeSpotLightNode
from RGT.XML.SVG.Filters.feBlendNode import FeBlendNode
from RGT.XML.SVG.Filters.feColorMatrixNode import FeColorMatrixNode 
from RGT.XML.SVG.Filters.feComponentTransferNode import FeComponentTransferNode
from RGT.XML.SVG.Filters.feFuncRNode import FeFuncRNode
from RGT.XML.SVG.Filters.feFuncGNode import FeFuncGNode
from RGT.XML.SVG.Filters.feFuncANode import FeFuncANode
from RGT.XML.SVG.Filters.feFuncBNode import FeFuncBNode
from RGT.XML.SVG.Filters.feCompositeNode import FeCompositeNode
from RGT.XML.SVG.Filters.feConvolveMatrixNode import FeConvolveMatrixNode
from RGT.XML.SVG.Filters.feDiffuseLightingNode import FeDiffuseLightingNode
from RGT.XML.SVG.Filters.feDisplacementMapNode import FeDisplacementMapNode
from RGT.XML.SVG.Filters.feFloodNode import FeFloodNode
from RGT.XML.SVG.Filters.feGaussianBlurNode import FeGaussianBlurNode
from RGT.XML.SVG.Filters.feImageNode import FeImageNode
from RGT.XML.SVG.Filters.feMergeNode import FeMergeNode
from RGT.XML.SVG.Filters.feMergeNodeNode import FeMergeNodeNode
from RGT.XML.SVG.Filters.feMorphologyNode import FeMorphologyNode
from RGT.XML.SVG.Filters.feOffsetNode import FeOffsetNode
from RGT.XML.SVG.Filters.feSpecularLightingNode import FeSpecularLightingNode
from RGT.XML.SVG.Filters.feTileNode import FeTileNode
from RGT.XML.SVG.Filters.feTurbulenceNode import FeTurbulenceNode
#finish filters
from RGT.XML.SVG.cursorNode import CursorNode
from RGT.XML.SVG.aNode import ANode
from RGT.XML.SVG.viewNode import ViewNode
from RGT.XML.SVG.scriptNode import ScriptNode
#animate
from RGT.XML.SVG.Animation.animateNode import AnimateNode
from RGT.XML.SVG.Animation.setNode import SetNode
from RGT.XML.SVG.Animation.animateMotionNode import AnimateMotionNode
from RGT.XML.SVG.Animation.mpathNode import MpathNode
from RGT.XML.SVG.Animation.animateColorNode import AnimateColorNode
from RGT.XML.SVG.Animation.animateTransformNode import AnimateTransformNode
#end animate
#font
from RGT.XML.SVG.fontNode import FontNode
from RGT.XML.SVG.glyphNode import GlyphNode
from RGT.XML.SVG.missingGlyphNode import MissingGlyph
from RGT.XML.SVG.hkernNode import HkernNode
from RGT.XML.SVG.vkernNode import VkernNode
from RGT.XML.SVG.fontFaceNode import FontFaceNode
from RGT.XML.SVG.fontFaceSrcNode import FontFaceSrcNode
from RGT.XML.SVG.fontFaceUriNode import FontFaceUriNode
from RGT.XML.SVG.fontFaceFormatNode import FontFaceFormatNode
from RGT.XML.SVG.fontFaceNameNode import FontFaceNameNode
#end font
from RGT.XML.SVG.metadataNode import MetadataNode
from RGT.XML.SVG.foreignObjectNode import ForeignObjectNode
#gradient
from RGT.XML.SVG.linearGradientNode import LinearGradientNode
from RGT.XML.SVG.radialGradientNode import RadialGradientNode
#end gradient
from RGT.XML.SVG.patternNode import PatternNode
from RGT.XML.SVG.stopNode import StopNode

#class copied from minidom
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

#class copied from minidom
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
    
    #filters
    
    def createFeDistantLightNode(self, azimuth= None, elevation= None):
        return FeDistantLightNode(self, azimuth, elevation)
    
    def createFePointLightNode(self, x= None, y= None, z= None):
        return FePointLightNode(self, x, y, z)
    
    def createFeSpotLightNode(self, x= None, y= None, z= None, specularExponent= None, limitingConeAngle= None):
        return FeSpotLightNode(self, x, y, z, specularExponent, limitingConeAngle)
    
    def createFeBlendNode(self):
        return FeBlendNode(self)
    
    def createFeColorMatrixNode(self):
        return FeColorMatrixNode(self)
    
    def createFeComponentTransferNode(self):
        return FeComponentTransferNode(self)
    
    def createFeFuncRNode(self):
        return FeFuncRNode(self)
    
    def createFeFuncGNode(self):
        return FeFuncGNode(self)
    
    def createFeFuncA(self):
        return FeFuncANode(self)
    
    def createFeFuncB(self):
        return FeFuncBNode(self)
    
    def createFeCompositeNode(self):
        return FeCompositeNode(self)
    
    def createrFeConvolveMatrixNode(self):
        return FeConvolveMatrixNode(self)
    
    def createFeDiffuseLightingNode(self):
        return FeDiffuseLightingNode(self)
    
    def createFeDisplacementMapNode(self):
        return FeDisplacementMapNode(self)
    
    def createFeFloodNode(self):
        return FeFloodNode(self)
    
    def createFeGaussianBlurNode(self):
        return FeGaussianBlurNode(self)
    
    def createFeImageNode(self):
        return FeImageNode(self)
    
    def createFeMergeNode(self):
        return FeMergeNode(self)
    
    def createFeMergeNodeNode(self):
        return FeMergeNodeNode(self)
    
    def createFeMorphologyNode(self):
        return FeMorphologyNode(self)
    
    def createFeOffsetNode(self):
        return FeOffsetNode(self)
    
    def createFeSpecularLightingNode(self):
        return FeSpecularLightingNode(self)
    
    def createFeTileNode(self):
        return FeTileNode(self)
    
    def createFeTurbulenceNode(self):
        return FeTurbulenceNode(self)
    
    #end filters
    
    def createCursorNode(self, x= None, y= None):
        return CursorNode(self, x, y)
    
    def createANode(self):
        return ANode(self)
    
    def createViewNode(self):
        return ViewNode(self)
    
    def createScriptNode(self):
        return ScriptNode(self)
    
    #animate
    
    def createAnimateNode(self):
        return AnimateNode(self)
    
    def createSetNode(self):
        return SetNode(self)
    
    def createAnimateMotionNode(self):
        return AnimateMotionNode(self)
    
    def createMPathNode(self):
        return MpathNode(self)
    
    def createAnimateColorNode(self):
        return AnimateColorNode(self)
    
    def createAnimateTransformNode(self):
        return AnimateTransformNode(self)
    
    #end animate
    
    #font
    
    def createFontNode(self):
        return FontNode(self)
    
    def createGlypthNode(self):
        return GlyphNode(self)
    
    def createMissingGlypthNode(self):
        return MissingGlyph(self)
    
    def createHkernNode(self):
        return HkernNode(self)
    
    def createVkernNode(self):
        return VkernNode(self)
    
    def createFontFaceNode(self):
        return FontFaceNode(self)
    
    def createFontFaceSrcNode(self):
        return FontFaceSrcNode(self)
    
    def createFontFaceUriNode(self):
        return FontFaceUriNode(self)
    
    def createFontFaceFormatNode(self):
        return FontFaceFormatNode(self)
    
    def createFontFaceNameNode(self):
        return FontFaceNameNode(self)
    
    #end font
    
    def createMetadataNode(self):
        return MetadataNode(self)
    
    def createForeignObjectNode(self):
        return ForeignObjectNode(self)
    
    #gradient
    
    def createLinearGradientNode(self):
        return LinearGradientNode(self)
    
    def createRadialGradientNode(self):
        return RadialGradientNode(self)
    
    #end gradient
    
    def createGlyphNode(self):
        return GlyphNode(self)
    
    def createPatternNode(self):
        return PatternNode(self)
    
    def createStopNode(self):
        return StopNode(self)
        
    #copy from minidom, removed the part that writes the <?xml version="1.0" ?> and the encoding
    def writexml(self, writer, indent="", addindent="", newl="",
                 encoding = None):
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)        