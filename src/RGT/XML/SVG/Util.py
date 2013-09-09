'''
Utility file containing some help functions
'''


def createCssStyleNode(svgDoc, cssData=None):
    node = svgDoc.createStyleNode()
    node.setType('text/css')

    if cssData != None:
        node.setData(cssData)

    return node


def createJavaScriptNode(svgDoc, jsData=None):
    node = svgDoc.createScriptNode()
    node.setType('text/javascript')

    if jsData != None:
        node.setData(jsData)

    return node


def createEcmaScriptNode(svgDoc, ecmaData):
    node = svgDoc.createScriptNode()
    node.setType('text/ecmascript')

    if ecmaData != None:
        node.setData(ecmaData)

    return node
            