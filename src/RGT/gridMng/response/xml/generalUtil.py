from xml.dom.minidom import DOMImplementation

def createXmlGridIdNode(gridId):
    imp= DOMImplementation()
    xmlDoc= imp.createDocument(None, 'usid', None)
    root= xmlDoc.documentElement
    root.appendChild(xmlDoc.createTextNode(gridId))
    return root