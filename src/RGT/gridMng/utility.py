from django.http import HttpResponse
from RGT import settings
from xml.dom.minidom import getDOMImplementation
import random
import string
import tempfile
import os
import subprocess
from io import BytesIO


#definition of the supported file to convert svg to image
CONVERT_SVG_TO_PNG= 'png'
CONVERT_SVG_TO_JPG= 'jpg'
CONVERT_SVG_TO_PDF= 'pdf'
imageErrorData= None

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

def randomStringGenerator(size= 14):
    return ''.join(random.choice(string.ascii_letters + string.digits) for letter in xrange(size))

def validateName(name):
    result= str(name.strip())
    if name == None or name == '':
        return HttpResponse(createXmlErrorResponse("Name can not be empty"))
    return result

#this is a prototype function, do not use or change it 
def convertSvgTo(svgData, fileType):
    if fileType != None and svgData != None:
        tempSvgFileName= randomStringGenerator(24)
        tempImageFileName= randomStringGenerator(24)
        tempDirPath= tempfile.gettempdir()
        mimeType= None
        fileExtention= None
        tempFileSvg= tempDirPath + '/' + tempSvgFileName + '.svg'
        tempImageFile= tempDirPath + '/' + tempImageFileName
        if fileType == CONVERT_SVG_TO_PNG:
            tempImageFile+= '.png'
            fileExtention= '.png'
            mimeType= 'image/png'
        elif fileType == CONVERT_SVG_TO_JPG:
            tempImageFile+= '.jpg'
            fileExtention= '.jpg'
            mimeType= 'image/jpg'
        elif fileType == CONVERT_SVG_TO_PDF:
            tempImageFile+= '.pdf'
            fileExtention= '.pdf'
            mimeType= 'application/pdf'    
        else:
            raise IOError('file type not supported');
        fo= open(tempFileSvg, 'w')
        fo.write(svgData);
        fo.close()
        try:
            #use batik to convert the file to something
            batikPath= settings.projectPath
            batikPath+= '/src/RGT/gridMng/batik/batik-rasterizer.jar'
            batikPath= '"' + batikPath + '"'
            subprocess.call('java -jar ' + batikPath + ' -d ' + tempImageFile + ' -m ' + mimeType + ' -dpi 300 ' + tempFileSvg, shell= True)
            #destroy the svg temp file
            os.remove(tempFileSvg)
            return (tempImageFile, mimeType, fileExtention)
        except:
            #remove the file if an error happens
            os.remove(tempFileSvg)
            raise
    else:
        if svgData == None:
            raise ValueError('svgData is None')
        if fileType == None:
            raise ValueError('fileType is None')

def getImageError():
    global imageErrorData
    if imageErrorData == None:
        fpInMemory= BytesIO()
        fp= open(settings.projectPath + '/src/RGT/gridMng/error/error.jpg', "rb")        
        #read the file and place it in memory
        try:
            byte= fp.read(1)
            while byte != '':
                fpInMemory.write(byte)
                byte= fp.read(1)
        finally:
            fp.close()
        imageErrorData= fpInMemory.getvalue()
    return imageErrorData

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