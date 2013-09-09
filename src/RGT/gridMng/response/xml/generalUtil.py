from xml.dom.minidom import DOMImplementation
from xml.dom.minidom import getDOMImplementation


def createXmlGridIdNode(gridId):
    imp = DOMImplementation()
    xmlDoc = imp.createDocument(None, 'usid', None)
    root = xmlDoc.documentElement
    root.appendChild(xmlDoc.createTextNode(gridId))
    return root


def createXmlIterationNumberNode(iteration):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "iteration", None)
    topElement = doc.documentElement
    topElement.appendChild(doc.createTextNode(str(iteration)))
    return topElement


def createXmlNumberOfResponseNode(nResponsesSent):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "nResponses", None)
    topElement = doc.documentElement
    topElement.appendChild(doc.createTextNode(str(nResponsesSent)))
    return topElement