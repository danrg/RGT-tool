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