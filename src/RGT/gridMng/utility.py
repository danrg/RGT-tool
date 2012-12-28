from django.http import HttpResponse
from RGT import settings
from xml.dom.minidom import getDOMImplementation

from RGT.gridMng.hierarchical import hcluster, transpose, drawDendogram3

import base64
import random
import string
import tempfile
import os, sys
import subprocess
import traceback
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

def createFileResponse(fileData):
    response = HttpResponse(fileData.data, content_type= fileData.ContentType)
    if fileData.length != None:
        response['Content-Length']= fileData.length
    response['Content-Disposition'] = 'attachment; filename=' + fileData.fileName + '.' + fileData.fileExtention
    return response
    

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

#generate a table based on a grid    
def generateGridTable(gridObj):
    
    from RGT.gridMng.models import Ratings #can't be declared globally because it will generate an import error
    
    table= []
    header= []
    concernWeights= []
    
    if gridObj != None:
        i= 0;
        j= 0;
        concerns= gridObj.concerns_set.all()
        alternatives= gridObj.alternatives_set.all()
        nConcern= gridObj.concerns_set.all().count()
        nAlternatives= gridObj.alternatives_set.all().count()
        
        while i < nConcern:
            row= []
            if concerns[i].leftPole == None:
                row.append('')
            else:
                row.append(concerns[i].leftPole)
            while j < nAlternatives:
                ratio= Ratings.objects.filter(concern= concerns[i], alternative= alternatives[j])
                if len(ratio) >= 1:
                    ratio= ratio[0]
                    if ratio.rating != None:
                        row.append(ratio.rating)
                    else:
                        row.append('')
                else:
                    row.append('')
                j+= 1
            if concerns[i].rightPole == None:
                row.append('')
            else:
                row.append(concerns[i].rightPole)
            if concerns[i].weight != None:
                concernWeights.append(concerns[i].weight)
            else:
                concernWeights.append('')
            table.append(row)
            j= 0
            i+= 1
        concernWeights.reverse() #this is needed because the list will be poped during the template execution
        i=0;
        while i < nAlternatives:
            header.append(alternatives[i].name)
            i+= 1
    else:
        
        #create an empty table if no gridObj is passed
        defaultNConcerns= 3
        defaultNAlternatives= 2
        defaultWeightValue= 1.0
        
        table= [[""] * (defaultNAlternatives + 2) ] * defaultNConcerns
        header= [""] * defaultNAlternatives 
        concernWeights= [defaultWeightValue] * defaultNConcerns
        
    dic= {};
    dic['table']= table
    dic['tableHeader']= header
    dic['weights']= concernWeights
    return dic

#generate the dendogram
def createDendogram(gridObj):
 
    from RGT.gridMng.models import Ratings #can't be declared globally because it will generate an import error
 
    #lets create a matrix that the hierarchical module understands
    matrixFull= [] # this is the compleet matrix, it will be used to create the table in the picture
    matrixConcern= []
    matrixAlternatives= [] #matrix that will be transposed
    concerns= gridObj.concerns_set.all()
    alternatives= gridObj.alternatives_set.all()
    maxValueOfAlternative = -1 # this is to save time later on as i need to loop trough all the alternatives right now so i can check for max value
                        
    if len(concerns) > 1:
        for concernObj in concerns:
            row= []
            ratio= None
            weight= concernObj.weight
            if concernObj.leftPole != None:
                row.append(str(concernObj.leftPole))
                if len(alternatives) >= 1:
                    for alternativeObj in alternatives:
                        ratio= (Ratings.objects.get(concern= concernObj, alternative= alternativeObj)).rating
                        if ratio != None:
                            ratio*= weight
                            row.append(ratio)
                            if ratio > maxValueOfAlternative:
                                maxValueOfAlternative= ratio
                        else:
                            raise ValueError('Ratings must be complete in order to generate a dendrogram.')
                else:
                    raise ValueError('No alternatives were found.')
            else:
                raise ValueError('Concerns must be complete in order to generate a dendrogram.')
            matrixConcern.append(row)
            matrixAlternatives.append(row[1:])
            row= row[0:] #create new obj of row
            if concernObj.rightPole != None:
                row.append(str(concernObj.rightPole))
            else:
                raise ValueError('Concerns must be complete in order to generate a dendrogram.')
            matrixFull.append(row)
    else:
        raise ValueError('More than one concerns must be present in order to generate a dendrogram.')
    #lets transpose the matrix so we calculate the dendrogram for the alternatives
    matrixAlternatives= transpose(matrixAlternatives)
    i= 0;
    temp= [[]]
    while i < len(alternatives):
        if alternatives[i].name != None:
            matrixAlternatives[i].insert(0, str(alternatives[i].name))
            temp.append(str(alternatives[i].name))
            #print alternatives[i].name
            i+= 1;
        else:
            raise ValueError('Invalid alternative name: ' + alternatives[i].name)
    temp.append([])
    matrixFull.insert(0, temp)
    concenrClusters= hcluster(matrixConcern)
    alternativeClusters= hcluster(matrixAlternatives)
    img= drawDendogram3(concenrClusters, alternativeClusters, matrixFull, maxValueOfAlternative)
    try:
        if True:
            imgData= img.toxml()
            gridObj.dendogram= imgData
            gridObj.save()
            return imgData
        else:
            fp1= BytesIO()
            img.save(fp1, format= "PNG")
            imgData= fp1.getvalue()
            fp1.close()
            imgData= base64.b64encode(imgData)
            gridObj.dendogram= imgData
            gridObj.save()
            return imgData
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        raise Exception('Unknown error, couldn\'t create the dendogram')