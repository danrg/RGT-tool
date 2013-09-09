from xml.dom.minidom import Element
from RGT.XML.SVG.Attribs.coreAttributes import CoreAttributes
from xml.dom import Node, HierarchyRequestErr


class BasicSvgNode(Element, CoreAttributes):
    allowNoSvgChildNode = False #used to allow other then svg nodes to be appended, also used to check if a node is a SVG nod. This attribute is not used current  for node checking
    allowAllSvgNodesAsChildNodes = False
    svgNodeType = None
    _allowedSvgChildNodes = set()

    #Svg node definitions
    SVG_SVG_NODE = 1
    SVG_G_NODE = 2
    SVG_DEFS_NODE = 3
    SVG_DESC_NODE = 4
    SVG_TITLE_NODE = 5
    SVG_SYMBOL_NODE = 6
    SVG_USE_NODE = 7
    SVG_IMAGE_NODE = 8
    SVG_SWITCH_NODE = 9
    SVG_STYLE_NODE = 10
    #shape
    SVG_PATH_NODE = 11
    SVG_RECT_NODE = 12
    SVG_CIRCLE_NODE = 13
    SVG_ELLIPSE_NODE = 14
    SVG_LINE_NODE = 15
    SVG_POLYLINE_NODE = 16
    SVG_POLYGON_NODE = 17
    #end shape
    SVG_TEXT_NODE = 18
    SVG_TSPAN_NODE = 19
    SVG_TREF_NODE = 20
    SVG_TEX_PATH_NODE = 21
    SVG_ALT_GLYPH_NODE = 22
    SVG_ALT_GLYPH_DEF_NODE = 23
    SVG_ALT_GLYPH_ITEM_NODE = 24
    SVG_GLYPH_REF_NODE = 25
    SVG_MARKER_NODE = 26
    SVG_COLOR_PROFILE_NODE = 27
    SVG_CLIP_PATH_NODE = 28
    SVG_MASK_NODE = 29
    SVG_FILTER_NODE = 30
    SVG_FE_DISTANT_LIGHT_NODE = 31
    SVG_FE_POINT_LIGHT_NODE = 32
    SVG_FE_SPOT_LIGHT_NODE = 33
    SVG_FE_BLEND_NODE = 34
    SVG_FE_COLOR_MATRIX_NODE = 35
    SVG_FE_COMPONENT_TRANSFER_NODE = 36
    SVG_FE_FUNC_R_NODE = 37
    SVG_FE_FUNC_G_NODE = 38
    SVG_FE_FUNC_B_NODE = 39
    SVG_FE_FUNC_A_NODE = 40
    SVG_FE_COMPOSITE_NODE = 41
    SVG_FE_CONVOLVE_MATRIX_NODE = 42
    SVG_FE_DIFFUSE_LIGHTING_NODE = 43
    SVG_FE_DISPLACEMENT_MAP_NODE = 44
    SVG_FE_FLOOD_NODE = 45
    SVG_FE_GAUSSIAN_BLUR_NODE = 46
    SVG_FE_IMAGE_NODE = 47
    SVG_FE_MERGE_NODE = 48
    SVG_FE_MERGE_NODE_NODE = 49
    SVG_FE_MORPHOLOGY_NODE = 50
    SVG_FE_OFFSET_NODE = 51
    SVG_FE_SPECULAR_LIGHTING_NODE = 52
    SVG_FE_TILE_NODE = 53
    SVG_FE_TURBULENCE_NODE = 54
    SVG_CURSOR_NODE = 55
    SVG_A_NODE = 56
    SVG_VIEW_NODE = 57
    SVG_SCRIPT_NODE = 58
    #animation
    SVG_ANIMATE_NODE = 59
    SVG_SET_NODE = 60
    SVG_ANIMATE_MOTION_NODE = 61
    SVG_MPATH_NODE = 62
    SVG_ANIMATE_COLOR_NODE = 63
    SVG_ANIMATE_TRANSFORM_NODE = 64
    # end animation
    SVG_FONT_NODE = 65
    SVG_GLYPTH_NODE = 66
    SVG_MISSING_GLYPH_NODE = 67
    SVG_HKERN_NODE = 68
    SVG_VKERN_NODE = 69
    SVG_FONT_FACE_NODE = 70
    SVG_FONT_FACE_SRC_NODE = 71
    SVG_FONT_FACE_URI_NODE = 72
    SVG_FONT_FACE_FORMAT_NODE = 73
    SVG_FONT_FACE_NAME_NODE = 74
    SVG_METADATA_NODE = 75
    SVG_FOREIGN_OBJECT_NODE = 76
    #gradient
    SVG_LINEAR_GRADIENT_NODE = 77
    SVG_RADIAL_GRADIENT_NODE = 78
    #end gradient
    SVG_GLYPH_NODE = 79
    SVG_PATTERN_NODE = 80
    SVG_STOP_NODE = 81

    #group definitions
    SVG_GROUP_ANIMATION_ELEMENTS = {SVG_ANIMATE_NODE, SVG_SET_NODE, SVG_ANIMATE_MOTION_NODE, SVG_ANIMATE_COLOR_NODE,
                                    SVG_ANIMATE_TRANSFORM_NODE}
    SVG_GROUP_DESCRIPTIVE_ELEMENTS = {SVG_METADATA_NODE, SVG_DESC_NODE, SVG_TITLE_NODE}
    SVG_GROUP_SHAPE_ELEMENTS = {SVG_PATH_NODE, SVG_RECT_NODE, SVG_CIRCLE_NODE, SVG_ELLIPSE_NODE, SVG_LINE_NODE,
                                SVG_POLYLINE_NODE, SVG_POLYGON_NODE}
    SVG_GROUP_STRUCTURAL_ELEMENTS = {SVG_DEFS_NODE, SVG_G_NODE, SVG_SVG_NODE, SVG_SYMBOL_NODE, SVG_USE_NODE}
    SVG_GROUP_GRADIENT_ELEMENTS = {SVG_LINEAR_GRADIENT_NODE, SVG_RADIAL_GRADIENT_NODE}
    SVG_GROUP_TEXT_CONTENT_CHILD_ELEMENTS = {SVG_ALT_GLYPH_NODE, SVG_TEX_PATH_NODE, SVG_TREF_NODE, SVG_TSPAN_NODE}
    SVG_GROUP_FILTER_PRIMITIVE_ELEMENTS = {SVG_FE_BLEND_NODE, SVG_FE_COLOR_MATRIX_NODE, SVG_FE_COMPONENT_TRANSFER_NODE,
                                           SVG_FE_COMPOSITE_NODE, SVG_FE_CONVOLVE_MATRIX_NODE,
                                           SVG_FE_DIFFUSE_LIGHTING_NODE, SVG_FE_DISPLACEMENT_MAP_NODE,
                                           SVG_FE_FLOOD_NODE, SVG_FE_GAUSSIAN_BLUR_NODE, SVG_FE_IMAGE_NODE,
                                           SVG_FE_MERGE_NODE, SVG_FE_MORPHOLOGY_NODE, SVG_FE_OFFSET_NODE,
                                           SVG_FE_SPECULAR_LIGHTING_NODE, SVG_FE_TILE_NODE, SVG_FE_TURBULENCE_NODE}
    SVG_GROUP_LIGHT_SOURCE_ELEMENTS = {SVG_FE_DISTANT_LIGHT_NODE, SVG_FE_POINT_LIGHT_NODE, SVG_FE_POINT_LIGHT_NODE}

    def __init__(self, ownerDoc, tagName):
        Element.__init__(self, tagName)
        CoreAttributes.__init__(self)
        if ownerDoc:
            self.ownerDocument = ownerDoc


    def _nodeCodeToText(self, code):

        codes = {Node.ELEMENT_NODE: 'ELEMENT_NODE', Node.ATTRIBUTE_NODE: 'ATTRIBUTE_NODE', Node.TEXT_NODE: 'TEXT_NODE',
                 Node.CDATA_SECTION_NODE: 'CDATA_SECTION_NODE', Node.ENTITY_REFERENCE_NODE: 'ENTITY_REFERENCE_NODE',
                 Node.ENTITY_NODE: 'ENTITY_NODE', Node.PROCESSING_INSTRUCTION_NODE: 'PROCESSING_INSTRUCTION_NODE',
                 Node.COMMENT_NODE: 'COMMENT_NODE', Node.DOCUMENT_NODE: 'DOCUMENT_NODE',
                 Node.DOCUMENT_TYPE_NODE: 'DOCUMENT_TYPE_NODE ', Node.DOCUMENT_FRAGMENT_NODE: 'DOCUMENT_FRAGMENT_NODE',
                 Node.NOTATION_NODE: 'NOTATION_NODE'}

        if codes.has_key(code) == True:
            return codes[code]
        return None

    def appendChild(self, node):
        if hasattr(node, 'allowNoSvgChildNode'):
            if not self.allowAllSvgNodesAsChildNodes:
                if not (node.svgNodeType in self._allowedSvgChildNodes):
                    raise HierarchyRequestErr(
                        "%s cannot be child of %s" % (repr(node), repr(self)))
                else:
                    Element.appendChild(self, node)
        Element.appendChild(self, node)
            
            