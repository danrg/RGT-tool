from django.http import HttpResponse
from RGT import settings
from RGT.gridMng.response.xml.htmlResponseUtil import createXmlErrorResponse
from RGT.gridMng.hierarchical import hcluster, transpose, drawDendogram3
from RGT.XML.SVG.svgDOMImplementation import SvgDOMImplementation
from RGT.settings import DENDROGRAM_FONT_LOCATION
from PIL import ImageFont #@UnresolvedImport

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
            #old code used to transform the png image to a string so the browser could display it
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

def convertGridTableToSvg(gridObj= None):
    from RGT.gridMng.models import Ratings
    
    ###########settings###########
    fontSize= 30
    f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, fontSize)
    xWordCellSpace= 5 #space between a word and the right and left line of the cell (in pixels)
    yWordCellSpace= 5 #space between the biggest word and the top and bottom line of the cell (in pixels)
    
    xTableOffSet= 5 #the x offset of the start point of the table. Start point is x= 0 (in pixels)
    yTableOffset= 5 #the y offset of the start point of the table. Start point is y= 0 (in pixels)
    
    tableLineThickness= 1 #in pixels
    
    if gridObj != None:
        concerns= gridObj.concerns_set.all()
        alternatives= gridObj.alternatives_set.all()
        nConcerns= len(concerns)
        nAlternatives= len(alternatives)
        tData= __TableData___()
        alternativeNames= []
        concernNames= [] #list of tulips, position 0 contains the left pole, position 1 contains the right pole: [('a', 'b'), ('c', 'd'), ......]
        ratioValues= [] #matrix
        maxWordHeight= 0
        colWidths= [None for x in xrange(nAlternatives)]
        isFirstRunDone= False
        
        ##########Pre-processing##########
        colN= 0
        for concernObj in concerns:
            concernNames.append((concernObj.leftPole, concernObj.rightPole))
            row= []
            for alternativeObj in alternatives:
                # we only need to run this code ones for all the alternatives
                if not isFirstRunDone:
                    alternativeNames.append(alternativeObj.name)
                    size= f.getsize(alternativeObj.name)
                    if size[1] > maxWordHeight:
                        maxWordHeight= size[1]
                    if size[0] > colWidths[colN]:
                        colWidths[colN]= size[0]
                #process the rating info
                ratingObj= Ratings.objects.filter(concern= concernObj, alternative= alternativeObj)
                if len(ratingObj) >= 1:
                    ratingObj= ratingObj[0]
                    row.append(ratingObj.rating)
                    #check to see if the rating text size 
                    if ratingObj.rating != None:
                        size= f.getsize(str(ratingObj.rating))
                        if size[0] > colWidths[colN]:
                            colWidths[colN]= size[0]
                        if size[1] > maxWordHeight:
                            maxWordHeight= size[1]            
                colN+= 1
            colN= 0          
            isFirstRunDone= True
            ratioValues.append(row)
            row= []
        
        #add xWordCellSpace * 2 to each position of the array
        colWidths[:] = [x + (xWordCellSpace * 2) for x in colWidths]
        
        ##########End pre-processing##########
        tData.cellHeight= maxWordHeight + (yWordCellSpace *2)
        tData.cellWidths= colWidths
        tData.lineThickness= tableLineThickness
        tData.nCols= nAlternatives
        tData.nRows= nConcerns
        tData.xTableOffSet= xTableOffSet
        tData.yTableOffSet= yTableOffset
        
        imp= SvgDOMImplementation()
        xmlDoc= imp.createSvgDocument()
        root= xmlDoc.documentElement
        root.setXmlns('http://www.w3.org/2000/svg')
        root.setVersion('1.1')
        gNode= __createSvgTable__(tData)
        root.appendChild(gNode)
        return xmlDoc.toxml()
                
                

#lineColor: tulip (r,b,g)
#return is a g node containing the code for the table
def __createSvgTable__(data):
    
    imp= SvgDOMImplementation()
    xmlDoc= imp.createSvgDocument()
    nvl= data.nCols - 1 #number vertical lines
    nhl= data.nRows - 1 #number horizontal lines
    previousX= 0
    previousY= 0
    mainGnode= xmlDoc.createGNode()
    mainGnode.setId('svgGridTableGroup')
    #create the main body of the table
    tableWidth= (data.nCols * data.lineThickness) + sum(data.cellWidths)
    tableHeight= (data.nRows * data.lineThickness) + (data.nRows * data.cellHeight)
    tempNode= xmlDoc.createRectNode(data.xTableOffSet, data.yTableOffSet, tableHeight, tableWidth)
    tempNode.setFill('none')
    tempNode.setStroke('black')
    mainGnode.appendChild(tempNode)
    #create the dividing lines in the table
    previousX+= data.xTableOffSet
    previousY+= data.yTableOffSet
    #create the vertical lines
    i= 0
    while i < nvl:
        cw= data.cellWidths[i]
        x= previousX + cw + data.lineThickness
        tempNode= xmlDoc.createLineNode(x, data.yTableOffSet, x, data.yTableOffSet + tableHeight)
        tempNode.setStroke('black')
        mainGnode.appendChild(tempNode)
        previousX= x
        i+= 1
    
    #create the horizontal lines
    i= 0
    while i < nhl:
        y= previousY + data.cellHeight + data.lineThickness
        tempNode= xmlDoc.createLineNode(data.xTableOffSet, y, data.xTableOffSet + tableWidth, y) 
        tempNode.setStroke('black')
        i+= 1
        previousY= y
        mainGnode.appendChild(tempNode)
    
    return mainGnode
    
    
    

#place holder for the variables used in __createSvgTable__
class __TableData___(object):
    
    cellWidths= None #array with the cells width
    cellHeight= None
    nCols= None
    nRows= None
    lineThickness= 1
    lineColor= None
    xTableOffSet= 0
    yTableOffSet= 0
    
    
    
    
    