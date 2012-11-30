from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class PresentationAttributes(BasicSvgAttribute):

    #1st line
    ATTRIBUTE_ALIGMENT_BASELINE= 'alignment-baseline'
    ATTRIBUTE_BASELINE_SHIFT= 'baseline-shift'
    ATTRIBUTE_CLIP= 'clip'
    ATTRIBUTE_CLIP_PATH= 'clip-path'
    ATTRIBUTE_CLIP_RULE= 'clip-rule'
    ATTRIBUTE_COLOR= 'color'
    ATTRIBUTE_COLOR_INTERPOLATION= 'color-interpolation'
    ATTRIBUTE_COLOR_INTERPOLATION_FILTERS= 'color-interpolation-filters'
    ATTRIBUTE_COLOR_PROFILE= 'color-profile'
    ATTRIBUTE_COLOR_RENDERING= 'color-rendering'
    ATTRIBUTE_CURSOR= 'cursor'
    ATTRIBUTE_DIRECTION= 'direction'
    ATTRIBUTE_DISPLAY= 'display'
    ATTRIBUTE_DOMINANT_BASELINE= 'dominant-baseline'
    #2nd line
    ATTRIBUTE_ENABLE_BACKGROUND= 'enable-background'
    ATTRIBUTE_FILL= 'fill'
    ATTRIBUTE_FILL_OPACITY= 'fill-opacity'
    ATTRIBUTE_FILL_RULE= 'fill-rule'
    ATTRIBUTE_FILTER= 'filter'
    ATTRIBUTE_FLOOD_COLOR= 'flood-color'
    ATTRIBUTE_FLOOD_OPACITY= 'flood-opacity'
    ATTRIBUTE_FONT_FAMILY= 'font-family'
    ATTRIBUTE_FONT_SIZE= 'font-size'
    ATTRIBUTE_FONT_SIZE_ADJUST= 'font-size-adjust'
    ATTRIBUTE_FONT_STRETCH= 'font-stretch'
    ATTRIBUTE_FONT_STYLE= 'font-style'
    ATTRIBUTE_FONT_VARIANT= 'font-variant'
    ATTRIBUTE_FONT_WEIGHT= 'font-weight'
    ATTRIBUTE_GLYPH_ORIENTATION_HORIZONTAL= 'glyph-orientation-horizontal'
    ATTRIBUTE_GLYPH_ORIENTATION_VERTICAL= 'glyph-orientation-vertical'
    #3rd line
    ATTRIBUTE_IMAGE_RENDERING= 'image-rendering'
    ATTRIBUTE_KERNING= 'kerning'
    ATTRIBUTE_LETTER_SPACING= 'letter-spacing'
    ATTRIBUTE_LIGHTING_COLOR= 'lighting-color'
    ATTRIBUTE_MARKER_END= 'marker-end'
    ATTRIBUTE_MARKER_MID= 'marker-mid'
    ATTRIBUTE_MARKER_START= 'marker-start'
    ATTRIBUTE_MASK= 'mask'
    ATTRIBUTE_OPACITY= 'opacity'
    ATTRIBUTE_OVERFLOW= 'overflow'
    ATTRIBUTE_POINTER_EVENTS= 'pointer-events'
    ATTRIBUTE_SHAPE_RENDERING= 'shape-rendering'
    ATTRIBUTE_STOP_COLOR= 'stop-color'
    ATTRIBUTE_STOP_OPACITY= 'stop-opacity'
    ATTRIBUTE_STROKE= 'stroke'
    ATTRIBUTE_STROKE_DASHARRAY= 'stroke-dasharray'
    #4th line
    ATTRIBUTE_STROKE_DASHOFFSET= 'stroke-dashoffset'
    ATTRIBUTE_STROKE_LINECAP= 'stroke-linecap'
    ATTRIBUTE_STROKE_LINEJOIN= 'stroke-linejoin'
    ATTRIBUTE_STROKE_MITERLIMIT= 'stroke-miterlimit'
    ATTRIBUTE_STROKE_OPACITY= 'stroke-opacity'
    ATTRIBUTE_STROKE_WIDTH= 'stroke-width'
    ATTRIBUTE_TEXT_ANCHOR= 'text-anchor'
    ATTRIBUTE_TEXT_DECORATION= 'text-decoration'
    ATTRIBUTE_TEXT_RENDERING= 'text-rendering'
    ATTRIBUTE_UNICODE_BIDI= 'unicode-bidi'
    ATTRIBUTE_VISIBILIY= 'visibility'
    ATTRIBUTE_WORD_SPACING= 'word-spacing'
    ATTRIBUTE_WRITING_MODE= 'writing-mode'
    
    #1st line sets
    
    def setAligmentBaseline(self, data):
        allowedValues= ['auto', 'baseline', 'before-edge', 'text-before-edge', 'middle', 'central', 'after-edge', 'text-after-edge', 'ideographic', 'alphabetic', 'hanging', 'mathematical', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ALIGMENT_BASELINE, data)
            
    def setBaseLineShift(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BASELINE_SHIFT, data)
            
    def setClip(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CLIP, data)
            
    def setClipPath(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CLIP_PATH, data)
            
    def setClipRule(self, data):
        allowedValues= ['nonzero', 'evenodd', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_CLIP_RULE, data)
    
    def setColor(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_COLOR, data)   
    
    def setColorInterpolation(self, data):
        allowedValues= ['auto', 'sRGB', 'linearRGB', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_COLOR_INTERPOLATION, data)
    
    def setColorInterpolationFilter(self, data):
        allowedValues= ['auto', 'sRGB', 'linearRGB', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_COLOR_INTERPOLATION_FILTERS, data)   
    
    def setColorProfile(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_COLOR_PROFILE, data)             
            
    def setColorRendering(self, data):
        allowedValues= ['auto', 'optimizeSpeed', 'optimizeQuality', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_COLOR_RENDERING, data)
    
    def setCursor(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CURSOR, data)
            
    def setDirection(self, data):
        allowedValues= ['ltr', 'rtl', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_DIRECTION, data)
    
    def setDisplay(self, data):
        allowedValues= ['inline', 'block', 'list-item', 'run-in', 'compact', 'marker', 'table', 'inline-table', 'table-row-group', 'table-header-group', 'table-footer-group', 'table-row', 'table-column-group', 'table-column', 'table-cell', 'table-caption', 'none', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_DISPLAY, data)
    
    def setDominantBaseline(self, data):
        allowedValues= ['auto', 'use-script', 'no-change', 'reset-size', 'ideographic', 'alphabetic', 'hanging', 'mathematical', 'central', 'middle', 'text-after-edge', 'text-before-edge', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_DOMINANT_BASELINE, data)
   
    #2nd line sets
                 
    def setEnableBackground(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ENABLE_BACKGROUND, data)
    
    def setFill(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FILL, data)
    
    def setFillOpacity(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FILL_OPACITY, data)
    
    def setFillRule(self, data):
        allowedValues= ['nonzero', 'evenodd', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FILL_RULE, data)
    
    def setFilter(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FILTER, data)
    
    def setFloodColor(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FLOOD_COLOR, data)
    
    def setFloodOpacity(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FLOOD_OPACITY, data)
    
    def setFontFamily(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_FAMILY, data)
    
    def setFontSize(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_SIZE, data)
    
    def setFontSizeAdjust(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_SIZE_ADJUST, data)
    
    def setFontStretch(self, data):
        allowedValues= ['normal', 'wider', 'narrower', 'ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FONT_STRETCH, data)
                
    def setFontStyle(self, data):
        allowedValues= ['normal', 'italic', 'ablique', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FONT_STYLE, data)
                
    def setFontVariant(self, data):
        allowedValues= ['normal', 'small-caps', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FONT_VARIANT, data)
    
    def setFontWeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_WEIGHT, data)
    
    def setGlyphOrientationHorizontal(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_GLYPH_ORIENTATION_HORIZONTAL, data)
    
    def setGlyphOrientationVertical(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_GLYPH_ORIENTATION_VERTICAL, data)
            
    #3rd line sets
    
    def setImageRendering(self, data):
        allowedValues= ['auto', 'optimizeSpeed', 'optimizeQuality', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_IMAGE_RENDERING, data)
    
    def setKerning(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KERNING, data)
            
    
    def setLetterSpacing(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_LETTER_SPACING, data)
            
    def setLightingColor(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_LIGHTING_COLOR, data)
            
    def setMarkerEnd(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_END, data)
            
    def setMarkerMid(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_MID, data)
            
    def setMarkerStart(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MARKER_START, data)
            
    def setMask(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MASK, data)
            
    def setOpacity(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_OPACITY, data) 
            
    def setOverflow(self, data):
        allowedValues= ['visible', 'hidden', 'scroll', 'auto','inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_OVERFLOW, data)
    
    def setPointerEvents(self, data):
        allowedValues= ['visiblePainted', 'visibleFill', 'visibleStroke', 'visible', 'painted', 'fill', 'stroke', 'all', 'none', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_POINTER_EVENTS, data)
    
    def setShapeRendering(self, data):
        allowedValues= ['auto', 'optimizeSpeed', 'crispEdges', 'geometricPrecision', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_SHAPE_RENDERING, data)
    
    def setStopColor(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STOP_COLOR, data)
            
    def setStopOpacity(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STOP_OPACITY, data)
    
    def setStroke(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE, data)
    
    def setStrokeDasharray(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE_DASHARRAY, data)  
            
    #4th line sets
    
    def setStrokeDashoffset(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE_DASHOFFSET, data) 
            
    def setStrokeLinecap(self, data):
        allowedValues= ['butt', 'round', 'square', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_STROKE_LINECAP, data) 
                
    def setStrokeLinejoin(self, data):
        allowedValues= ['miter', 'round', 'bevel', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_STROKE_LINEJOIN, data)
                
    def setStrokeMiterlimit(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE_MITERLIMIT, data)
            
    def setStrokeOpacity(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE_OPACITY, data) 
            
    def setStrokeWidth(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STROKE_WIDTH, data)
            
    def setTextAnchor(self, data):
        allowedValues= ['start', 'middle', 'end', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_TEXT_ANCHOR, data)
                
    def setTextDecoration(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TEXT_DECORATION, data)
            
    def setTextRendering(self, data):
        allowedValues= ['auto', 'optimizeSpeed', 'optimizeLegibility', 'geometricPrecision', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_TEXT_RENDERING, data)
                
    def setUnicodeBidi(self, data):
        allowedValues= ['normal', 'embed', 'bidi-override', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_UNICODE_BIDI, data)
                
    def setVisibility(self, data):
        allowedValues= ['visible', 'hidden', 'collapse', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_VISIBILIY, data)
    
    def setWordSpacing(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_WORD_SPACING, data)
    
    def setWritingMode(self, data):
        allowedValues= ['lr-tb', 'rl-tb', ' tb-rl', 'lr', 'rl', 'tb', 'inherit']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_WRITING_MODE, data)
    
    #1st line gets
    
    def getAligmentBaseline(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ALIGMENT_BASELINE)
        if node != None:
            return node.nodeValue
        return None
    
    def getBaseLineShift(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_BASELINE_SHIFT)
        if node != None:
            return node.nodeValue
        return None
    
    def getClip(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CLIP)
        if node != None:
            return node.nodeValue
        return None
    
    def getClipPath(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CLIP_PATH)
        if node != None:
            return node.nodeValue
        return None
    
    def getClipRule(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CLIP_RULE)
        if node != None:
            return node.nodeValue
        return None
    
    def getColor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_COLOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getColorInterpolation(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_COLOR_INTERPOLATION)
        if node != None:
            return node.nodeValue
        return None
    
    def getColorInterpolationFilter(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_COLOR_INTERPOLATION_FILTERS)
        if node != None:
            return node.nodeValue
        return None
    
    def getColorProfile(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_COLOR_PROFILE)
        if node != None:
            return node.nodeValue
        return None
    
    def getColorRendering(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_COLOR_RENDERING)
        if node != None:
            return node.nodeValue
        return None
    
    def getCursor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CURSOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getDirection(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DIRECTION)
        if node != None:
            return node.nodeValue
        return None
    
    def getDisplay(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DISPLAY)
        if node != None:
            return node.nodeValue
        return None
    
    def getDominantBaseline(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DOMINANT_BASELINE)
        if node != None:
            return node.nodeValue
        return None
    
    #2nd line gets
    
    def getEnableBackground(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ENABLE_BACKGROUND)
        if node != None:
            return node.nodeValue
        return None
    
    def getFill(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILL)
        if node != None:
            return node.nodeValue
        return None
    
    def getFillOpacity(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILL_OPACITY)
        if node != None:
            return node.nodeValue
        return None
    
    def getFillRule(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILL_RULE)
        if node != None:
            return node.nodeValue
        return None
    
    def getFilter(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILTER)
        if node != None:
            return node.nodeValue
        return None
    
    def getFloodColor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FLOOD_COLOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getFloodOpacity(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FLOOD_OPACITY)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontFamily(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_FAMILY)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontSize(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_SIZE)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontSizeAdjust(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_SIZE_ADJUST)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontStretch(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_STRETCH)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontStyle(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_STYLE)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontVariant(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_VARIANT)
        if node != None:
            return node.nodeValue
        return None
    
    def getFontWeight(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FONT_WEIGHT)
        if node != None:
            return node.nodeValue
        return None
    
    def getGlynphOrientationHorizontal(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_GLYPH_ORIENTATION_HORIZONTAL)
        if node != None:
            return node.nodeValue
        return None
    
    def getGlynphOrientationVertical(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_GLYPH_ORIENTATION_VERTICAL)
        if node != None:
            return node.nodeValue
        return None
    
    #3rd line gets
    
    def getImageRendering(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_IMAGE_RENDERING)
        if node != None:
            return node.nodeValue
        return None
    
    def getKerning(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_KERNING)
        if node != None:
            return node.nodeValue
        return None
    
    def getLetterSpacing(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_LETTER_SPACING)
        if node != None:
            return node.nodeValue
        return None
    
    def getLightingColor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_LIGHTING_COLOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getMarkerEnd(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_END)
        if node != None:
            return node.nodeValue
        return None
    
    def getMarkerMid(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_MID)
        if node != None:
            return node.nodeValue
        return None
    
    def getMakerStart(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MARKER_START)
        if node != None:
            return node.nodeValue
        return None
    
    def getMask(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MASK)
        if node != None:
            return node.nodeValue
        return None
    
    def getOpacity(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_OPACITY)
        if node != None:
            return node.nodeValue
        return None
    
    def getOverflow(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_OVERFLOW)
        if node != None:
            return node.nodeValue
        return None
    
    def getPointerEvents(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_POINTER_EVENTS)
        if node != None:
            return node.nodeValue
        return None
    
    def getShapeRendering(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_SHAPE_RENDERING)
        if node != None:
            return node.nodeValue
        return None
    
    def getStopColor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STOP_COLOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getStopOpacity(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STOP_OPACITY)
        if node != None:
            return node.nodeValue
        return None
    
    def getStroke(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeDasharray(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_DASHARRAY)
        if node != None:
            return node.nodeValue
        return None
    
    #4th line gets
    
    def getStrokeDashoffset(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_DASHOFFSET)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeLinecap(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_LINECAP)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeLinejoin(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_LINEJOIN)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeMiterlimit(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_MITERLIMIT)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeOpacity(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_OPACITY)
        if node != None:
            return node.nodeValue
        return None
    
    def getStrokeWidth(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STROKE_WIDTH)
        if node != None:
            return node.nodeValue
        return None
    
    def getTextAnchor(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TEXT_ANCHOR)
        if node != None:
            return node.nodeValue
        return None
    
    def getTextDecoration(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TEXT_DECORATION)
        if node != None:
            return node.nodeValue
        return None
    
    def getTextRendering(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TEXT_RENDERING)
        if node != None:
            return node.nodeValue
        return None
    
    def getUnicodeBidi(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_UNICODE_BIDI)
        if node != None:
            return node.nodeValue
        return None
    
    def getVisibility(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VISIBILIY)
        if node != None:
            return node.nodeValue
        return None
    
    def getWordSpacing(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_WORD_SPACING)
        if node != None:
            return node.nodeValue
        return None
    
    def getWritingMode(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_WRITING_MODE)
        if node != None:
            return node.nodeValue
        return None