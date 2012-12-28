from xml.dom.minidom import DOMImplementation

#This function is used to create a successful
#svgDoc: String with the svg document
def createSvgResponse(svgDoc, extraDataXmlDoc= None):
    imp= DOMImplementation()
    xmlDoc= imp.createDocument(None, 'svgResponse', '')
    root= xmlDoc.documentElement
    #create the node where the svg data should be stored
    tempNode= xmlDoc.createElement('svgData')
    tempNode.appendChild(xmlDoc.createCDATASection(svgDoc))
    root.appendChild(tempNode)
    #add extra data
    if extraDataXmlDoc != None:
        extraInfoNode= xmlDoc.createElement('extraInfo')
        extraInfoNode.appendChild(extraDataXmlDoc.document)
        root.appendChild(extraInfoNode)
    return xmlDoc.toxml()
    