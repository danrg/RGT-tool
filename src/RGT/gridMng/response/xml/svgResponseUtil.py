from xml.dom.minidom import DOMImplementation


#This function is used to create a successful
#svgDoc: String with the svg document
def createSvgResponse(svgDoc, extraData=None):
    imp = DOMImplementation()
    xmlDoc = imp.createDocument(None, 'svgResponse', '')
    root = xmlDoc.documentElement
    #create the node where the svg data should be stored
    tempNode = xmlDoc.createElement('svgData')
    tempNode.appendChild(xmlDoc.createCDATASection(svgDoc))
    root.appendChild(tempNode)
    #add extra data
    if extraData != None:
        extraInfoNode = xmlDoc.createElement('extraInfo')
        if hasattr(extraData, 'documentElement'):
            extraInfoNode.appendChild(extraData.documentElement)
        else:
            extraInfoNode.appendChild(extraData)
        root.appendChild(extraInfoNode)
    return xmlDoc.toxml()
