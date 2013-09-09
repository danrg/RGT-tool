from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType


class GraphicalEventAttributes(BasicSvgAttribute):
    ATTRIBUTE_ON_FOCUS_IN = 'onfocusin'
    ATTRIBUTE_ON_FOCUS_OUT = 'onfocusout'
    ATTRIBUTE_ON_ACTIVATE = 'onactivate'
    ATTRIBUTE_ON_CLICK = 'onclick'
    ATTRIBUTE_ON_MOUSE_DOWN = 'onmousedown'
    ATTRIBUTE_ON_MOUSE_UP = 'onmouseup'
    ATTRIBUTE_ON_MOUSE_OVER = 'onmouseover'
    ATTRIBUTE_ON_MOUSE_MOVE = 'onmousemove'
    ATTRIBUTE_ON_MOUSE_OUT = 'onmouseout'
    ATTRIBUTE_ON_LOAD = 'onload'

    def setOnFocusIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_FOCUS_IN, data)

    def setOnFocusOut(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_FOCUS_OUT, data)

    def setOnActivate(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_ACTIVATE, data)

    def setOnClick(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_CLICK, data)

    def setOnMouseDown(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_MOUSE_DOWN, data)

    def setOnMouseUp(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_MOUSE_UP, data)

    def setOnMouseOver(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_MOUSE_OVER, data)

    def setOnMouseMove(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_MOUSE_MOVE, data)

    def setOnMouseOut(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_MOUSE_OUT, data)

    def setOnLoad(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ON_LOAD, data)

    def getOnFocusIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_FOCUS_IN)
        if node != None:
            return node.nodeValue
        return None

    def getOnFocusOut(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_FOCUS_OUT)
        if node != None:
            return node.nodeValue
        return None

    def getOnActivate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_ACTIVATE)
        if node != None:
            return node.nodeValue
        return None

    def getOnClick(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_CLICK)
        if node != None:
            return node.nodeValue
        return None

    def getOnMouseDown(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_MOUSE_DOWN)
        if node != None:
            return node.nodeValue
        return None

    def getOnMouseUp(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_MOUSE_UP)
        if node != None:
            return node.nodeValue
        return None

    def getOnMouseOver(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_MOUSE_OVER)
        if node != None:
            return node.nodeValue
        return None

    def getOnMouseMove(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_MOUSE_MOVE)
        if node != None:
            return node.nodeValue
        return None

    def getOnMouseOut(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_MOUSE_OUT)
        if node != None:
            return node.nodeValue
        return None

    def getOnLoad(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ON_LOAD)
        if node != None:
            return node.nodeValue
        return None
    
    