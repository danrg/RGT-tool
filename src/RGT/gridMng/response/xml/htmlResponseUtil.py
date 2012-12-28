from xml.dom.minidom import getDOMImplementation

def createXmlSuccessResponse(htmlData, extraData= None):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "site", None)
    topElement= doc.documentElement
    htmlNode= doc.createElement('htmlData')
    htmlNode.appendChild(doc.createTextNode(htmlData))
    topElement.appendChild(htmlNode)
    
    #add the extra data
    if extraData:
        extraNode= doc.createElement('extra')
        if not isinstance(extraData, list):
            extraNode.appendChild(extraData)  
        else:
            for data in extraData:
                extraNode.appendChild(data)
        topElement.appendChild(extraNode)
                
    return doc.toxml()

def createXmlErrorResponse(errorData):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "site", None)
    topElement= doc.documentElement
    errorNode= doc.createElement('error')
    errorNode.appendChild(doc.createTextNode(errorData))
    topElement.appendChild(errorNode)
    return doc.toxml()

#data is a dictionary, key would be the the 'value' used in the comboBox and the value would be the displaying element in the comboBox
def createXmlForComboBox(data):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "comboxData", None)
    topElement= doc.documentElement
    for key in data:
        elementNode= doc.createElement('element')
        valueNode= doc.createElement('value')
        displayNode= doc.createElement('display')
        valueNode.appendChild(doc.createTextNode(str(key)))
        displayNode.appendChild(doc.createTextNode(str(data[key])))
        elementNode.appendChild(valueNode)
        elementNode.appendChild(displayNode)
        topElement.appendChild(elementNode)
    return topElement

def createXmlForIterationNumber(iteration):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "iteration", None)
    topElement= doc.documentElement
    topElement.appendChild(doc.createTextNode(str(iteration)))
    return topElement

def createXmlForNumberOfResponseSent(nResponsesSent):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "nResponses", None)
    topElement= doc.documentElement
    topElement.appendChild(doc.createTextNode(str(nResponsesSent)))
    return topElement

# Create a dateTime tag that is returned to participant (along with the XmlSuccessResponse),
# in order to show the time that he sent the response.
def createDateTimeTag(data):
    impl= getDOMImplementation()
    doc= impl.createDocument(None, "dateTimeData", None)
    topElement= doc.documentElement
    dateTimeNode = doc.createElement('dateTime')
    dateTimeNode.appendChild(doc.createTextNode(str(data)))
    topElement.appendChild(dateTimeNode)
    return topElement