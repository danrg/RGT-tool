from django.http import HttpResponse
from RGT import settings
from RGT.gridMng.response.xml.htmlResponseUtil import createXmlErrorResponse
from RGT.gridMng.hierarchical import hcluster, transpose, drawDendogram3
from RGT.XML.SVG.svgDOMImplementation import SvgDOMImplementation
from RGT.settings import DENDROGRAM_FONT_LOCATION
from PIL import ImageFont #@UnresolvedImport
from types import StringType, UnicodeType

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
            imgData= img.toxml('utf-8')
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
    
    xLeftPoleCellOffset= 5 #in pixels, space between the start of the picture and the left pole
    xRightPoleWordOffset= 5
    
    xWordCellSpace= 5 #space between a word and the right and left line of the cell (in pixels)
    yWordCellSpace= 5 #space between the biggest word and the top and bottom line of the cell (in pixels)
    
    xTableOffSet= 5 #the x offset of the start point of the table from the end of the biggest left pole word. Start point is x= 0 (in pixels)
    yTableOffset= 5 #the y offset of the start point of the table. Start point is y= 0 (in pixels)
    
    tableLineThickness= 1 #in pixels
    tableLineColor= (60, 179, 113) #value in rbg
    tableCellWordColor= (60, 179, 113) #value in rbg
    tableHeaderCellWordColor= (255, 255, 255) #value in rbg
    
    tableHeaderLinearColor1= (141,179,235)
    tableHeaderLinearColor2= (95,144,227)
    
    leftAndRightPoleTextColor= (255, 255, 255)
    leftAndRightPoleBackgroundColor= (141,179,235)
    
    totalWeightBackgroundColor= (141,179,235)
    totalWeightTextColor= (255, 255, 255)
    
    minLeftAndRightPoleCellWidth= 50 #in pixels, min size of the cell of a pole
    xOffSetLeftAndRightPoleWordToCell= 15 #in pixels, min space between the inside of the pole cell and the word
    
    yTotalWeightCellOffset= 5 #in pixels, space between the end of the table and the start of the total weight cell
    
    totalWeightFontSize= 20
    fTotalWeight= ImageFont.truetype(DENDROGRAM_FONT_LOCATION, totalWeightFontSize)
    
    ###shadow settings###
    shadowXOffset= 3 #value in pixels
    shadowYOffset= 3 #value in pixels
    shadowBlurSize= 4 #how big the bluer should be
    
    fontName= 'arial'
    
    if gridObj != None:
        concerns= gridObj.concerns_set.all()
        alternatives= gridObj.alternatives_set.all()
        nConcerns= len(concerns)
        nAlternatives= len(alternatives)
        tData= __TableData___()
        alternativeNames= []
        concernNames= [] #list of tulips, position 0 contains the left pole, position 1 contains the right pole: [('a', 'b'), ('c', 'd'), ......]
        tableData= [] #matrix
        maxWordHeight= 0
        colWidths= [None for x in xrange(nAlternatives + 1)]
        isFirstRunDone= False
        maxWidthLeftAndRightConcern= minLeftAndRightPoleCellWidth
        totalWeight= 0.0
        
        ##########Pre-processing##########
        colN= 0
        for concernObj in concerns:
            concernNames.append((concernObj.leftPole, concernObj.rightPole))
            size= f.getsize(concernObj.leftPole)
            xTotalConcernCellOffset= 2 * xOffSetLeftAndRightPoleWordToCell
            #left pole
            if size[0] + xTotalConcernCellOffset > maxWidthLeftAndRightConcern:
                maxWidthLeftAndRightConcern= size[0]
            size= f.getsize(concernObj.rightPole)
            #right pole
            if size[0] + xTotalConcernCellOffset > maxWidthLeftAndRightConcern:
                maxWidthLeftAndRightConcern= size[0]   
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
            #weight
            totalWeight+= concernObj.weight
            size= f.getsize(str(concernObj.weight))
            if size[0] > colWidths[nAlternatives]:
                colWidths[nAlternatives]= size[0]
            if size[1] > maxWordHeight:
                maxWordHeight= size[1] 
            row.append(str(concernObj.weight)) 
                  
            isFirstRunDone= True
            tableData.append(row)
            row= []
        
        #add the weight to the alternative names and calculate its size       
        size= f.getsize('weight')
        if size[0] > colWidths[nAlternatives]:
            colWidths[nAlternatives]= size[0]
        if size[1] > maxWordHeight:
            maxWordHeight= size[1]
        
        #add xWordCellSpace * 2 to each position of the array (in place)
        colWidths[:] = [x + (xWordCellSpace * 2) for x in colWidths]
        
        #create a copy of the alternativeNames and append weight to the new copy
        alternativeNamesCopy= alternativeNames[:]
        alternativeNamesCopy.append('weight')
        tableData.insert(0, alternativeNamesCopy)
        ########## End pre-processing##########
        
        ##########create the table##########
        cellHeight= maxWordHeight + (yWordCellSpace *2)
        tData.cellHeight= cellHeight
        tData.cellWidths= colWidths
        tData.lineThickness= tableLineThickness
        tData.nCols= nAlternatives + 1
        tData.nRows= nConcerns + 1 #plus 1 as we have added the table header
        tData.xTableOffSet= xTableOffSet + maxWidthLeftAndRightConcern + xLeftPoleCellOffset + 2 * xOffSetLeftAndRightPoleWordToCell + (tableLineThickness / 2)
        tData.yTableOffSet= yTableOffset
        tData.tableData= tableData
        tData.xWordCellSpace= xWordCellSpace
        tData.yWordCellSpace= yWordCellSpace
        tData.fontObject= f
        tData.fontName= fontName
        tData.fontSize= fontSize
        tData.tableLineColor= tableLineColor
        tData.tableCellWordColor= tableCellWordColor
        tData.tableHeaderCellWordColor= tableHeaderCellWordColor
        
        imp= SvgDOMImplementation()
        xmlDoc= imp.createSvgDocument()
        root= xmlDoc.documentElement
        root.setXmlns('http://www.w3.org/2000/svg')
        root.setVersion('1.1')
        gNodeTable= __createSvgTable__(tData)
        ########## end create the table##########
        
        globalDefNode= xmlDoc.createDefsNode()
        root.appendChild(globalDefNode)
        ##########create first row (header) linear gradient##########
        tempNode= xmlDoc.createLinearGradientNode('0%', '0%', '0%', '100%')
        tempNode.appendChild(xmlDoc.createStopNode('0%', createColorRGBString(tableHeaderLinearColor1), 1))
        tempNode.appendChild(xmlDoc.createStopNode('100%', createColorRGBString(tableHeaderLinearColor2), 1))
        tempNode.setId('tableHeaderGradient')
        globalDefNode.appendChild(tempNode)
        ########## end create first row (header) linear gradient##########
        
        ##########create the shadow filter ##########
        filterNode= xmlDoc.createFilterNode()
        filterNode.setId('shadow1')
        filterNode.setX(0)
        filterNode.setY(0)
        filterNode.setWidth('150%')
        filterNode.setHeight('150%')
        tempNode= xmlDoc.createFeOffsetNode()
        tempNode.setDx(shadowXOffset)
        tempNode.setDy(shadowYOffset)
        tempNode.setResult('offOut')
        tempNode.setIn('SourceGraphic')
        filterNode.appendChild(tempNode)
        tempNode= xmlDoc.createFeGaussianBlurNode()
        tempNode.setResult('blurOut')
        tempNode.setIn('offOut')
        tempNode.setStdDeviation(shadowBlurSize)
        filterNode.appendChild(tempNode)
        tempNode= xmlDoc.createFeBlendNode()
        tempNode.setIn('SourceGraphic')
        tempNode.setIn2('blurOut')
        tempNode.setMode('normal')
        filterNode.appendChild(tempNode)
        globalDefNode.appendChild(filterNode)
        ########## end create the shadow filter ##########
        
        ##########create the rectangle to place behind the table 1st row##########
        tempNode= xmlDoc.createRectNode(xTableOffSet + maxWidthLeftAndRightConcern + xLeftPoleCellOffset + 2 * xOffSetLeftAndRightPoleWordToCell, yTableOffset, tableLineThickness + cellHeight, (tableLineThickness * (nAlternatives + 1))  + sum(colWidths))
        tempNode.setFill('url(#tableHeaderGradient)')
        root.appendChild(tempNode)
        ######### end #create the rectangle to place behind the table 1st row##########
        
        #add the shadow to the rectangle of the table (main body)
        for node in gNodeTable.getElementsByTagName('rect'):
            node.setFilter('url(#shadow1)')
            
        ##########add the left pole words##########
        i= 0
        poleNode= xmlDoc.createGNode()
        poleNode.setId('polesGroup')
        tableWidth= sum(colWidths) + ((nAlternatives + 2) * tableLineThickness)
        while i < nConcerns:
            
            ######add the rect for the background of the poles######

            #left pole
            x= xLeftPoleCellOffset
            y= yTableOffset + ((i + 1) * tableLineThickness) + ((i + 1) * cellHeight) + (tableLineThickness / 2)
            height= cellHeight
            width= maxWidthLeftAndRightConcern + (2 * xOffSetLeftAndRightPoleWordToCell)
            tempNode= xmlDoc.createRectNode(x, y, height, width)
            tempNode.setFill(createColorRGBString(leftAndRightPoleBackgroundColor))
            tempNode.setFilter('url(#shadow1)')
            poleNode.appendChild(tempNode)
            #right pole
            x= xLeftPoleCellOffset + maxWidthLeftAndRightConcern + (2 * xOffSetLeftAndRightPoleWordToCell) + xTableOffSet + tableWidth + xRightPoleWordOffset
            tempNode= xmlDoc.createRectNode(x, y, height, width)
            tempNode.setFill(createColorRGBString(leftAndRightPoleBackgroundColor))
            tempNode.setFilter('url(#shadow1)')
            poleNode.appendChild(tempNode)
            ###### end add the rect for the background of the pole######
            
            #left
            size= f.getsize(concernNames[i][0])
            x= xLeftPoleCellOffset + (maxWidthLeftAndRightConcern / 2) + xOffSetLeftAndRightPoleWordToCell - (size[0]/2)
            y= yTableOffset + ((i + 1) * tableLineThickness) + ((i + 1) * cellHeight) + (tableLineThickness/2) + (cellHeight/2) + (size[1]/2) - 5
            tempNode= xmlDoc.createSvgTextNode(x, y, concernNames[i][0])
            tempNode.setFontFamily(fontName)
            tempNode.setFontSize(str(fontSize) + 'px')
            tempNode.setFill(createColorRGBString(leftAndRightPoleTextColor))
            poleNode.appendChild(tempNode)
            #right
            size= f.getsize(concernNames[i][1])
            x= xLeftPoleCellOffset  + maxWidthLeftAndRightConcern + (2 * xOffSetLeftAndRightPoleWordToCell) + xTableOffSet + tableWidth + xTableOffSet + (maxWidthLeftAndRightConcern / 2) + xOffSetLeftAndRightPoleWordToCell - (size[0]/2)
            y= yTableOffset + ((i + 1) * tableLineThickness) + ((i + 1) * cellHeight) + (tableLineThickness/2) + (cellHeight/2) + (size[1]/2) - 5
            tempNode= xmlDoc.createSvgTextNode(x, y, concernNames[i][1])
            tempNode.setFontFamily(fontName)
            tempNode.setFontSize(str(fontSize) + 'px')
            tempNode.setFill(createColorRGBString(leftAndRightPoleTextColor))
            poleNode.appendChild(tempNode)
            
            i+= 1
        root.appendChild(poleNode)
        ########## end add the left pole words##########
        
        ########## add the total weight ##########
        
        ########## add the rect of the total weight background ##########
        weightNode= xmlDoc.createGNode()
        totalWeightText= 'Total weight: ' + str(totalWeight)
        size= fTotalWeight.getsize(totalWeightText)
        x= xLeftPoleCellOffset
        # (nConcerns + 2), nConcerns + 1 for headers and + 1 for the outside top and button line thickness
        y= yTableOffset + ((nConcerns + 1) * cellHeight) + ((nConcerns + 2) * tableLineThickness) + yTotalWeightCellOffset
        height= size[1] + 10
        width= size[0] + 10
        tempNode= xmlDoc.createRectNode(x, y, height, width)
        tempNode.setFill(createColorRGBString(totalWeightBackgroundColor))
        tempNode.setFilter('url(#shadow1)')
        weightNode.appendChild(tempNode)
        ########## end add the rect of the total weight background ##########
        
        x+= (width / 2) - (size[0] / 2) - 3
        y+= (height /2) + (size[1] / 2) - 3
        tempNode= xmlDoc.createSvgTextNode(x, y, totalWeightText)
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(totalWeightFontSize) + 'px')
        tempNode.setFill(createColorRGBString(totalWeightTextColor))
        weightNode.appendChild(tempNode)
        
        root.appendChild(weightNode)
        ########## end add the total weight ##########
        
        root.appendChild(gNodeTable)
        return xmlDoc.toxml('utf-8')


#data should be an object of the ResultAlternativeConcernTableData class
def convertAlternativeConcernSessionResultToSvg(data):
    
    ########### Settings ###########
    fontSize= 30
    f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, fontSize)
    
    newWordFontSize= 20
    newWordF= ImageFont.truetype(DENDROGRAM_FONT_LOCATION, newWordFontSize)
    newWord= 'new'
    newWordColor= (243, 178, 126)
    
    headerColor= (255, 255, 255)
    headerFontSize= 30
    headerFontName= 'ariel'
    headerConcern= 'Concern'
    headerAlternative= 'Alternative'
    fHeader= ImageFont.truetype(DENDROGRAM_FONT_LOCATION, headerFontSize)
    
    yHeaderOffset= 10;
    
    fontSize
    
    fontName= 'arial'
    
    xWordCellSpace= 5 #space between a word and the right and left line of the cell (in pixels)
    yWordCellSpace= 5 #space between the biggest word and the top and bottom line of the cell (in pixels)
    
    concernTableYOffset= 5 #offset from the top element. In pixels
    alternativeTableYOffset= 5 #offset from the top element. In pixels
    
    concernTableXOffset= 5 #offset from the right element. In pixels
    alternativeTableXOffset= 40 #offset from the right element. In pixels

    xNewWordOffset= 5 #offset of the new word from the most left element. In pixels
    
    tableLineThickness= 1 #in pixels
    tableLineColor= (202, 217, 237) #value in rbg
    tableCellWordColor= (0, 0, 0) #value in rbg
    tableHeaderCellWordColor= (185, 187, 189) #value in rbg
    
    concernTableHeaderBackground= (232, 234, 237)
    alternativeTableHeaderBackground= (232, 234, 237)
    
    tableBackgroundColor1= (214, 233, 246)
    tableBackgroundColor2= (189, 209, 247)
    
    shadowXOffset= 3 #value in pixels
    shadowYOffset= 3 #value in pixels
    shadowBlurSize= 4 #how big the bluer should be
    
    ########### End settings ###########
    
    tempData= __TableData___()
    alternativeTableData= []
    concernTableData= []
    alternativeTableHeader= ['name', 'times cited']
    concernTableHeader= ['left', 'right', 'times cited']
    concernsNRows= len(data.concerns) + 1 #+1 because of the header
    alternativesNRows= len(data.alternatives) + 1 #+1 because of the header 
    concernsNCols= len(concernTableHeader)
    alternativesNCols= len(alternativeTableHeader)
    concernCellWidths= [0 for x in xrange(concernsNCols)] #@UnusedVariable
    alternativeCellWidths= [0 for x in xrange(alternativesNCols)] #@UnusedVariable
    concernCellHeight= 0
    alternativeCellHeight= 0
    concernTableTotalXOffset= 0
    alternativeTableTotalXOffset= 0
    hasNewConcerns= False
    newWordSize= newWordF.getsize(newWord)
    headerMaxHeight= 0
    concernTableTotalYOffset= 0
    alternativeTableTotalYOffset= 0
    
    #################### Pre-processing ####################
    
    #create the correct format for the table data
    
    #concern
    i= 1
    j= 0
    concernTableData.append(concernTableHeader)
    while i < concernsNRows:
        row= []
        row.append(data.concerns[i - 1][0])
        row.append(data.concerns[i - 1][1])
        row.append(data.concerns[i - 1][2])
        if data.concerns[i - 1][5] == True:
            hasNewConcerns= True 
        concernTableData.append(row)
        #calculate the cell height and width
        while j < concernsNCols:
            word= row[j]
            if type(word) != StringType and type(word) != UnicodeType:
                word= str(word)
            size= f.getsize(word)
            if size[0] > concernCellWidths[j]:
                concernCellWidths[j]= size[0]
            
            if size[1] > concernCellHeight:
                concernCellHeight= size[1]
            j+= 1
        j= 0
        i+= 1
    
    #alternative
    i= 1
    j= 0
    alternativeTableData.append(alternativeTableHeader)
    while i < alternativesNRows:
        row= []
        row.append(data.alternatives[i - 1][0])
        row.append(data.alternatives[i - 1][1])
        alternativeTableData.append(row)
        #calculate the cell height and width
        while j < alternativesNCols:
            word= row[j]
            if type(word) != StringType and type(word) != UnicodeType:
                word= str(word)
            size= f.getsize(word)
            if size[0] > alternativeCellWidths[j]:
                alternativeCellWidths[j]= size[0]
            
            if size[1] > alternativeCellHeight:
                alternativeCellHeight= size[1]
            j+= 1
        j= 0
        i+= 1
    
    #check if the header word sizes
    
    #concern
    i= 0
    while i < concernsNCols:
        size= f.getsize(concernTableData[0][i])
        if size[0] > concernCellWidths[i]:
            concernCellWidths[i]= size[0]
        if size[1] > concernCellHeight:
            concernCellHeight= size[1]
        i+= 1
    
    #alternative
    i= 0
    while i < alternativesNCols:
        size= f.getsize(alternativeTableData[0][i])
        if size[0] > alternativeCellWidths[i]:
            alternativeCellWidths[i]= size[0]
        if size[1] > alternativeCellHeight:
            alternativeCellHeight= size[1]
        i+= 1
    
    #calculate the max height of the headers
    size= fHeader.getsize(headerConcern)
    if size[1] > headerMaxHeight:
        headerMaxHeight= size[1]
    size= fHeader.getsize(headerAlternative)
    if size[1] > headerMaxHeight:
        headerMaxHeight= size[1]
    #add xWordCellSpace * 2 to each position of the array (in place)
    concernCellWidths[:] = [x + (xWordCellSpace * 2) for x in concernCellWidths]
    alternativeCellWidths[:] = [x + (xWordCellSpace * 2) for x in alternativeCellWidths]
    
    concernTableTotalXOffset+= concernTableXOffset
    alternativeTableTotalXOffset+= concernTableTotalXOffset + sum(concernCellWidths) + ((concernsNCols + 1) * tableLineThickness)  + alternativeTableXOffset
    if hasNewConcerns:
        alternativeTableTotalXOffset+= xNewWordOffset + newWordSize[0]
        
    #calculate the total y offset for the alternative and concern table
    concernTableTotalYOffset= yHeaderOffset + headerMaxHeight + concernTableYOffset
    alternativeTableTotalYOffset= yHeaderOffset + headerMaxHeight + alternativeTableYOffset
    
    #################### End pre-processing ####################
    
    imp= SvgDOMImplementation()
    xmlDoc= imp.createSvgDocument()
    root= xmlDoc.documentElement
    root.setXmlns('http://www.w3.org/2000/svg')
    root.setVersion('1.1')
    
    globalDefNode= xmlDoc.createDefsNode()
    root.appendChild(globalDefNode)
    
    ##########create the shadow filter ##########
    filterNode= xmlDoc.createFilterNode()
    filterNode.setId('shadow1')
    filterNode.setX(0)
    filterNode.setY(0)
    filterNode.setWidth('150%')
    filterNode.setHeight('150%')
    tempNode= xmlDoc.createFeOffsetNode()
    tempNode.setDx(shadowXOffset)
    tempNode.setDy(shadowYOffset)
    tempNode.setResult('offOut')
    tempNode.setIn('SourceGraphic')
    filterNode.appendChild(tempNode)
    tempNode= xmlDoc.createFeGaussianBlurNode()
    tempNode.setResult('blurOut')
    tempNode.setIn('offOut')
    tempNode.setStdDeviation(shadowBlurSize)
    filterNode.appendChild(tempNode)
    tempNode= xmlDoc.createFeBlendNode()
    tempNode.setIn('SourceGraphic')
    tempNode.setIn2('blurOut')
    tempNode.setMode('normal')
    filterNode.appendChild(tempNode)
    globalDefNode.appendChild(filterNode)
    ########## end create the shadow filter ##########
    
    ########## Create the glow filter ##########
    filterNode= xmlDoc.createFilterNode()
    filterNode.setId('glow1')
    filterNode.setFilterUnits('userSpaceOnUse')
    filterNode.setX(0)
    filterNode.setY(0)
    filterNode.setWidth(400)
    filterNode.setHeight(400)
    tempNode= xmlDoc.createFeGaussianBlurNode()
    tempNode.setIn('SourceGraphic')
    tempNode.setStdDeviation(25)
    filterNode.appendChild(tempNode)
    globalDefNode.appendChild(filterNode)
    ########## End create the glow filter ##########
    
    ########## Create the headers of the concerns and alternative tables ##########
    
    headerGroup= xmlDoc.createGNode()
    headerGroup.setId('headerGroup')
    #concern
    tempNode= xmlDoc.createSvgTextNode(concernTableXOffset, yHeaderOffset + headerMaxHeight - 5, headerConcern)
    tempNode.setFontFamily(headerFontName)
    tempNode.setFontSize(str(headerFontSize) + 'px')
    tempNode.setColor(createColorRGBString(headerColor))
    headerGroup.appendChild(tempNode)
    
    #alternative
    tempNode= xmlDoc.createSvgTextNode(alternativeTableTotalXOffset, yHeaderOffset + headerMaxHeight - 5, headerAlternative)
    tempNode.setFontFamily(headerFontName)
    tempNode.setFontSize(str(headerFontSize) + 'px')
    tempNode.setColor(createColorRGBString(headerColor))
    headerGroup.appendChild(tempNode)
    
    ########## End Create the headers of the concerns and alternative tables ##########
    
    #################### Create the background of the header tables ####################
    
    #concern
    concernTableHeaderBackgroundGround= xmlDoc.createGNode()
    concernTableHeaderBackgroundGround.setId('concernTableHeaderBackgroundGround')
    tempNode= xmlDoc.createRectNode(concernTableTotalXOffset, concernTableTotalYOffset, concernCellHeight + tableLineThickness, sum(concernCellWidths) + (concernsNCols * tableLineThickness) )
    tempNode.setFill(createColorRGBString(concernTableHeaderBackground))
    concernTableHeaderBackgroundGround.appendChild(tempNode)
    
    #alternative
    alternativeTableHeaderBackgroundGround= xmlDoc.createGNode()
    alternativeTableHeaderBackgroundGround.setId('alternativeTableHeaderBackgroundGround')
    tempNode= xmlDoc.createRectNode(alternativeTableTotalXOffset, alternativeTableTotalYOffset, alternativeCellHeight + tableLineThickness, sum(alternativeCellWidths) + (alternativesNCols * tableLineThickness))
    tempNode.setFill(createColorRGBString(alternativeTableHeaderBackground))
    alternativeTableHeaderBackgroundGround.appendChild(tempNode)
    
    #################### End create the background of the header tables ####################
    
    #################### Create the background of the data part of the tables ####################
    
    #concern
    i= 1
    concernTableDataBackgrounGroup= xmlDoc.createGNode()
    concernTableDataBackgrounGroup.setId('concernTableDataBackgrounGroup')
    while i < concernsNRows:
        x= concernTableTotalXOffset
        y= concernTableTotalYOffset + (i * concernCellHeight) + (i * tableLineThickness) + tableLineThickness/2
        tempNode= xmlDoc.createRectNode(x, y, concernCellHeight + tableLineThickness, sum(concernCellWidths) + tableLineThickness * concernsNCols)
        if i % 2 == 0:
            tempNode.setFill(createColorRGBString(tableBackgroundColor2))
        else:
            tempNode.setFill(createColorRGBString(tableBackgroundColor1))
        concernTableDataBackgrounGroup.appendChild(tempNode)
        i+= 1
        
    #alternative
    i= 1
    alternativeTableDataBackgrounGroup= xmlDoc.createGNode()
    alternativeTableDataBackgrounGroup.setId('alternativeTableDataBackgrounGroup')
    while i < alternativesNRows:
        x= alternativeTableTotalXOffset
        y= alternativeTableTotalYOffset + (i * alternativeCellHeight) + (i * tableLineThickness) + tableLineThickness/2
        tempNode= xmlDoc.createRectNode(x, y, alternativeCellHeight + tableLineThickness, sum(alternativeCellWidths) + tableLineThickness * alternativesNCols)
        if i % 2 == 0:
            tempNode.setFill(createColorRGBString(tableBackgroundColor2))
        else:
            tempNode.setFill(createColorRGBString(tableBackgroundColor1))
        alternativeTableDataBackgrounGroup.appendChild(tempNode)
        i+= 1
    
    #################### End create the background of the data part of the tables ####################
    
    #################### Add the 'new' word next to the tables ####################
    
    #concern
    concernNewWordGroup= xmlDoc.createGNode()
    concernNewWordGroup.setId('concernNewWordGroup')
    i= 1
    x= concernTableTotalXOffset + sum(concernCellWidths) + (concernsNCols + 1) * tableLineThickness + xNewWordOffset
    while i < concernsNRows:
        if data.concerns[i - 1][5] == True:
            y= concernTableTotalYOffset + (i * concernCellHeight) + concernCellHeight / 2 + newWordSize[1] /2 - 5
            tempNode= xmlDoc.createSvgTextNode(x, y, newWord)
            tempNode.setFontFamily(fontName)
            tempNode.setFontSize( str(newWordFontSize) + 'px')
            tempNode.setFill('none')
            tempNode.setStroke(createColorRGBString(newWordColor))
            tempNode.setStrokeWidth(1)
            tempNode.setFilter('url(#shadow1)')
            concernNewWordGroup.appendChild(tempNode)
        i+= 1
        
    #alternative
    alternativeNewWordGroup= xmlDoc.createGNode()
    alternativeNewWordGroup.setId('alternativeNewWordGroup')
    i= 1
    x= alternativeTableTotalXOffset + sum(alternativeCellWidths) + (alternativesNCols + 1) * tableLineThickness + xNewWordOffset
    while i < alternativesNRows:
        if data.alternatives[i - 1][2] == True:
            y= alternativeTableTotalYOffset + (i * alternativeCellHeight) + alternativeCellHeight / 2 + newWordSize[1] /2 - 5
            tempNode= xmlDoc.createSvgTextNode(x, y, newWord)
            tempNode.setFontFamily(fontName)
            tempNode.setFontSize( str(newWordFontSize) + 'px')
            tempNode.setFill('none')
            tempNode.setStroke(createColorRGBString(newWordColor))
            tempNode.setStrokeWidth(1)
            tempNode.setFilter('url(#shadow1)')
            alternativeNewWordGroup.appendChild(tempNode)
        i+= 1
    
    
    #################### End add the 'new' word next to the tables ####################
    
    tempData.fontSize= fontSize
    tempData.fontObject= f
    tempData.fontName= fontName
    tempData.lineThickness= tableLineThickness
    tempData.tableLineColor= tableLineColor
    tempData.tableCellWordColor= tableCellWordColor
    tempData.tableHeaderCellWordColor= tableHeaderCellWordColor
    tempData.yWordCellSpace= yWordCellSpace
    tempData.xWordCellSpace= xWordCellSpace
    
    
    tempData.cellHeight= concernCellHeight
    tempData.cellWidths= concernCellWidths
    tempData.nCols= concernsNCols
    tempData.nRows= concernsNRows
    tempData.tableData= concernTableData
    tempData.yTableOffSet= concernTableTotalYOffset
    tempData.xTableOffSet= concernTableTotalXOffset
    
    xmlConcernTable= __createSvgTable__(tempData)
    
    root.appendChild(concernTableHeaderBackgroundGround)
    root.appendChild(concernTableDataBackgrounGroup)
    root.appendChild(concernNewWordGroup)
    root.appendChild(xmlConcernTable)
    
    tempData.cellHeight= alternativeCellHeight
    tempData.cellWidths= alternativeCellWidths
    tempData.nCols= alternativesNCols
    tempData.nRows= alternativesNRows
    tempData.tableData= alternativeTableData
    tempData.yTableOffSet= alternativeTableTotalYOffset
    tempData.xTableOffSet= alternativeTableTotalXOffset
    
    xmlAlternativeTable= __createSvgTable__(tempData)
    
    root.appendChild(headerGroup)
    root.appendChild(alternativeTableHeaderBackgroundGround)
    root.appendChild(alternativeTableDataBackgrounGroup)
    root.appendChild(alternativeNewWordGroup)
    root.appendChild(xmlAlternativeTable)
    
    return xmlDoc.toxml('utf-8')

#meanData, rangeData and stdData should be objects of the resultRatingWeightTableData class
def convertRatingWeightSessionResultToSvg(meanData, rangeData, stdData): 
    
    ###########settings###########
    fontSize= 30
    headerFontSize= 45
    f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, fontSize)
    fHeader= ImageFont.truetype(DENDROGRAM_FONT_LOCATION, headerFontSize)
    
    fontName= 'arial'
    
    meanTableYOffset= 5 #offset from the button of the header. In pixels
    rangeTableYOffset= 5 #offset from the button of the header. In pixels
    stdTableYOffset= 5 #offset from the button of the header. In pixels
    
    meanTableXOffset= 5 #offset from the biggest left concern to the table and the offset from the table to the right concern. In pixels
    rangeTableXOffset= 5 #offset from the biggest left concern to the table and the offset from the table to the right concern. In pixels
    stdTableXOffset= 5 #offset from the biggest left concern to the table and the offset from the table to the right concern. In pixels
    
    tableHeaderLinearColor1= (141,179,235)
    tableHeaderLinearColor2= (95,144,227)
    
    xWordCellSpace= 5 #space between a word and the right and left line of the cell (in pixels)
    yWordCellSpace= 5 #space between the biggest word and the top and bottom line of the cell (in pixels)
    
    meanHeaderYOffset= 10 #offset from the top of the header to the bottom of the element above it. In pixels
    rangeHeaderYOffset= 10 #offset from the top of the header to the bottom of the element above it. In pixels
    stdHeaderYOffset= 10 #offset from the top of the header to the bottom of the element above it. In pixels
    
    meanLeftConcernWordOffset= 5
    rangeLeftConcernWordOffset= 5
    stdLeftConcernWordOffset= 5
    meanRightConcernWordOffset= 5
    rangeRightConcernWordOffset= 5
    stdRightConcernWordOffset= 5
    
    tableLineThickness= 1 #in pixels
    tableLineColor= (60, 179, 113) #value in rbg
    tableCellWordColor= (60, 179, 113) #value in rbg
    tableHeaderCellWordColor= (255, 255, 255) #value in rbg
    
    ##############end##############
    
    tempData= __TableData___()
    rangeTableData= []
    meanTableData= []
    stdTableData= []
    
    tempData.nRows= len(meanData.tableData) + 1 #it is + 1 for the table header
    tempData.nCols= len(meanData.tableHeader)
    
    rangeColWidths= [0 for x in xrange(tempData.nCols)] #@UnusedVariable
    meanColWidths= [0 for x in xrange(tempData.nCols)] #@UnusedVariable
    stdColWidths= [0 for x in xrange(tempData.nCols)] #@UnusedVariable
    rangeCellHeight= 0
    meanCellHeight= 0
    stdCellHeight= 0
    meanTableYTotalOffset= 0 #@UnusedVariable
    rangeTableYTotalOffset= 0 #@UnusedVariable
    stdTableYTotalOffset= 0 #@UnusedVariable
    meanTableXTotalOffset= 0 #@UnusedVariable
    rangeTableXTotalOffset= 0 #@UnusedVariable
    stdTableXTotalOffset= 0 #@UnusedVariable
    meanHeaderSize= None #@UnusedVariable
    rangeHeaderSize= None #@UnusedVariable
    stdHeaderSize= None #@UnusedVariable
    meanTablesize= None #tulip (width, height) #@UnusedVariable
    rangeTablesize= None #tulip (width, height) #@UnusedVariable
    stdTablesize= None #tulip (width, height) #@UnusedVariable
    meanLeftConcernWordMaxWidth= 0
    rangeLeftConcernWordMaxWidth= 0
    stdLeftConcernWordMaxWidth= 0
    
    tempData.tableLineColor= tableLineColor
    tempData.lineThickness= tableLineThickness
    tempData.tableCellWordColor= tableCellWordColor
    tempData.tableHeaderCellWordColor= tableHeaderCellWordColor
    tempData.fontName= fontName
    tempData.fontObject= f
    tempData.fontSize= fontSize
    
    ####################Pre-processing####################
    
    #create the correct format for the __createSvgTable__ of the tables data
    i= 0
    j= 0
    while i < tempData.nRows - 1:
        rowMean= []
        rowRange= []
        rowStd= []
        while j < tempData.nCols:
            rowMean.append(meanData.tableData[i][j][0])
            rowRange.append(rangeData.tableData[i][j][0])
            rowStd.append(stdData.tableData[i][j][0])
            
            size= None
            
            if type(rowMean[j]) != StringType or type(rowMean[j]) != UnicodeType:
                size= f.getsize(str(rowMean[j]))
            else:
                size= f.getsize(rowMean[j])
                
            if size[0] > meanColWidths[j]:
                meanColWidths[j]= size[0]
            if size[1] > meanCellHeight:
                meanCellHeight= size[1]
            
            if type(rowRange[j]) != StringType or type(rowRange[j]) != UnicodeType:
                size= f.getsize(str(rowRange[j]))
            else:
                size= f.getsize(rowRange[j])
                
            if size[0] > rangeColWidths[j]:
                rangeColWidths[j]= size[0]
            if size[1] > rangeCellHeight:
                rangeCellHeight= size[1]
                
            if type(rowStd[j]) != StringType or type(rowStd[j]) != UnicodeType:
                size= f.getsize(str(rowStd[j]))
            else:
                size= f.getsize(rowStd[j])
                
            if size[0] > stdColWidths[j]:
                stdColWidths[j]= size[0]
            if size[1] > stdCellHeight:
                stdCellHeight= size[1]
            
            
            j+= 1
        rangeTableData.append(rowRange)
        meanTableData.append(rowMean)
        stdTableData.append(rowStd)
        j= 0
        i+= 1
    
    #add the table header to the table data and check the sizes
    i= 0
    
    while i < tempData.nCols:
        
        size= f.getsize(meanData.tableHeader[i])
        if size[0] > meanColWidths[i]:
            meanColWidths[i]= size[0]
        if size[1] > meanCellHeight:
            meanCellHeight= size[1]
        
        size= f.getsize(rangeData.tableHeader[i])
        if size[0] > rangeColWidths[i]:
            rangeColWidths[i]= size[0]
        if size[1] > rangeCellHeight:
            rangeCellHeight= size[1]
        
        size= f.getsize(stdData.tableHeader[i])
        if size[0] > stdColWidths[i]:
            stdColWidths[i]= size[0]
        if size[1] > stdCellHeight:
            stdCellHeight= size[1]
        
        i+= 1
    
    #add xWordCellSpace * 2 to each position of the array (in place)
    meanColWidths[:] = [x + (xWordCellSpace * 2) for x in meanColWidths]
    rangeColWidths[:] = [x + (xWordCellSpace * 2) for x in rangeColWidths]
    stdColWidths[:] = [x + (xWordCellSpace * 2) for x in stdColWidths]
    
    #add the extra space to the cell height
    meanCellHeight+= 2 * yWordCellSpace
    rangeCellHeight+= 2 * yWordCellSpace
    stdCellHeight+= 2 * yWordCellSpace
    
    #calculate the size of the hear words
    meanHeaderSize= fHeader.getsize(meanData.header)
    rangeHeaderSize= fHeader.getsize(rangeData.header)
    stdHeaderSize= fHeader.getsize(stdData.header)
    
    #calculate the height and width of the tables
    
    height= (tempData.nRows + 1) * tableLineThickness + (tempData.nRows * meanCellHeight)
    width= (tempData.nCols + 1) * tableLineThickness + sum(meanColWidths)
    meanTablesize= (width, height)
    
    height= 0
    width= 0
    
    height= (tempData.nRows + 1) * tableLineThickness + (tempData.nRows * rangeCellHeight)
    width= (tempData.nCols + 1) * tableLineThickness + sum(rangeColWidths)
    rangeTablesize= (width, height)
    
    height= 0
    width= 0
    
    height= (tempData.nRows + 1) * tableLineThickness + (tempData.nRows * stdCellHeight)
    width= (tempData.nCols + 1) * tableLineThickness + sum(stdColWidths)
    stdTablesize= (width, height)
    
    #calculate max width of the left concern
    i= 0
    while i < len(meanData.concerns):
        size= f.getsize(meanData.concerns[i][0])
        if size[0] > meanLeftConcernWordMaxWidth:
            meanLeftConcernWordMaxWidth= size[0]
        
        size= f.getsize(rangeData.concerns[i][0])
        if size[0] > rangeLeftConcernWordMaxWidth:
            rangeLeftConcernWordMaxWidth= size[0]
        
        size= f.getsize(stdData.concerns[i][0])
        if size[0] > stdLeftConcernWordMaxWidth:
            stdLeftConcernWordMaxWidth= size[0]
        
        i+= 1
    
    #calculate the offset of each table
    
    #y offset
    meanTableYTotalOffset= meanHeaderSize[1] + meanHeaderYOffset + meanTableYOffset
    rangeTableYTotalOffset= rangeHeaderSize[1] + rangeHeaderYOffset + rangeTableYOffset + meanTableYTotalOffset + meanTablesize[1]
    stdTableYTotalOffset= stdHeaderSize[1] + stdHeaderYOffset + stdTableYOffset + rangeTableYTotalOffset + rangeTablesize[1]
    
    #x offset
    meanTableXTotalOffset= meanLeftConcernWordMaxWidth + meanTableXOffset + meanLeftConcernWordOffset
    rangeTableXTotalOffset= rangeLeftConcernWordMaxWidth + rangeTableXOffset + rangeLeftConcernWordOffset
    stdTableXTotalOffset= stdLeftConcernWordMaxWidth + stdTableXOffset + stdLeftConcernWordOffset
    
    ####################End pre-processing####################
    
    #add the table header
    meanTableData.insert(0, meanData.tableHeader)   
    rangeTableData.insert(0, rangeData.tableHeader) 
    stdTableData.insert(0, stdData.tableHeader)
    
    #create xml doc
    imp= SvgDOMImplementation()
    xmlDoc= imp.createSvgDocument()
    root= xmlDoc.documentElement
    root.setXmlns('http://www.w3.org/2000/svg')
    root.setVersion('1.1')
    tempNode= None #@UnusedVariable
    globalDefNode= xmlDoc.createDefsNode()
    root.appendChild(globalDefNode)
    meanTableDataGroup= xmlDoc.createGNode()
    meanTableDataGroup.setId('meanTableDataGroup')
    rangeTableDataGroup= xmlDoc.createGNode()
    rangeTableDataGroup.setId('rangeTableDataGroup')
    stdTableDataGroup= xmlDoc.createGNode()
    stdTableDataGroup.setId('stdTableDataGroup')
    
    ########## create first row (header) linear gradient ##########
    tempNode= xmlDoc.createLinearGradientNode('0%', '0%', '0%', '100%')
    tempNode.appendChild(xmlDoc.createStopNode('0%', createColorRGBString(tableHeaderLinearColor1), 1))
    tempNode.appendChild(xmlDoc.createStopNode('100%', createColorRGBString(tableHeaderLinearColor2), 1))
    tempNode.setId('tableHeaderGradient')
    globalDefNode.appendChild(tempNode)
    ########## end create first row (header) linear gradient ##########
    
    ########## create the svg tables##########
    tempData.tableData= meanTableData
    tempData.cellHeight= meanCellHeight
    tempData.cellWidths= meanColWidths
    tempData.yTableOffSet= meanTableYTotalOffset
    tempData.xTableOffSet= meanTableXTotalOffset
    xmlTableMean= __createSvgTable__(tempData)
    
    tempData.tableData= rangeTableData
    tempData.cellHeight= rangeCellHeight
    tempData.cellWidths= rangeColWidths
    tempData.yTableOffSet= rangeTableYTotalOffset
    tempData.xTableOffSet= rangeTableXTotalOffset
    xmlTableRange= __createSvgTable__(tempData)
    
    tempData.tableData= stdTableData
    tempData.cellHeight= stdCellHeight
    tempData.cellWidths= stdColWidths
    tempData.yTableOffSet= stdTableYTotalOffset
    tempData.xTableOffSet= stdTableXTotalOffset
    xmlTableStd= __createSvgTable__(tempData)
    ########## end create the svg tables ##########
    
    ########## create the background of the table headers ##########
    meanTableHeaderBackgroundGroup= xmlDoc.createGNode()
    meanTableHeaderBackgroundGroup.setId('meanTableHeaderBackgroundGroup')
    rangeTableHeaderBackgroundGroup= xmlDoc.createGNode()
    rangeTableHeaderBackgroundGroup.setId('rangeTableHeaderBackgroundGroup')
    stdTableHeaderBackgroundGroup= xmlDoc.createGNode()
    stdTableHeaderBackgroundGroup.setId('stdTableHeaderBackgroundGroup')
    i= 0
    while i < len(meanData.tableHeader):
        #calculate the total length of cols from 0 to i for all 3 tables
        n1= 0
        n2= 0
        n3= 0
        j= 0
        while j < i:
            n1+= meanColWidths[j] 
            n2+= rangeColWidths[j] 
            n3+= stdColWidths[j]
            j+= 1
        #mean
        x= meanTableXTotalOffset + (tableLineThickness/2) + n1 + i * tableLineThickness
        y= meanTableYTotalOffset + (tableLineThickness/2)
        tempNode= xmlDoc.createRectNode(x, y, meanCellHeight + tableLineThickness, meanColWidths[i] + tableLineThickness)
        tempNode.setFill('url(#tableHeaderGradient)')
        meanTableHeaderBackgroundGroup.appendChild(tempNode)
        #range
        x= rangeTableXTotalOffset + (tableLineThickness/2) + n2 + i * tableLineThickness
        y= rangeTableYTotalOffset + (tableLineThickness/2)
        tempNode= xmlDoc.createRectNode(x, y, rangeCellHeight + tableLineThickness, rangeColWidths[i] + tableLineThickness)
        tempNode.setFill('url(#tableHeaderGradient)')
        rangeTableHeaderBackgroundGroup.appendChild(tempNode)
        #std
        x= stdTableXTotalOffset + (tableLineThickness/2) + n2 + i * tableLineThickness
        y= stdTableYTotalOffset + (tableLineThickness/2)
        tempNode= xmlDoc.createRectNode(x, y, stdCellHeight + tableLineThickness, stdColWidths[i] + tableLineThickness)
        tempNode.setFill('url(#tableHeaderGradient)')
        stdTableHeaderBackgroundGroup.appendChild(tempNode)
        
        i+= 1
    ########## end create the background of the table headers ##########
    
    ########## create the background of the rating cells ##########
    i= 0
    j= 0
    
    rangeTableBackground= xmlDoc.createGNode()
    rangeTableBackground.setId('rangeTableRateBackgroundGroup')
    stdTableBackground= xmlDoc.createGNode()
    stdTableBackground.setId('stdTableRateBackgroundGroup')
    while i < tempData.nRows - 1:
        while j < tempData.nCols:
            n1= 0
            n2= 0
            k= 0
            while k < j:
                n1+= rangeColWidths[k]
                n2+= stdColWidths[k]
                k+= 1
            #range table
            color= rangeData.tableData[i][j][1]
            tempNode= xmlDoc.createRectNode(tableLineThickness * j + n1 + rangeTableXTotalOffset, rangeTableYTotalOffset + ( (i + 1) * tableLineThickness) + ( (i + 1) * rangeCellHeight), rangeCellHeight + tableLineThickness, rangeColWidths[j] + tableLineThickness)
            if color != None:
                tempNode.setFill(createColorRGBString(rangeData.tableData[i][j][1]))
            else:
                tempNode.setFill(createColorRGBString((255, 255, 255)))
            rangeTableBackground.appendChild(tempNode)
            #std table
            color= stdData.tableData[i][j][1]
            tempNode= xmlDoc.createRectNode(tableLineThickness * j + n2 + stdTableXTotalOffset, stdTableYTotalOffset + ( (i + 1) * tableLineThickness) + ( (i + 1) * stdCellHeight), stdCellHeight + tableLineThickness, stdColWidths[j] + tableLineThickness)
            if color != None:
                tempNode.setFill(createColorRGBString(stdData.tableData[i][j][1]))
            else:
                tempNode.setFill(createColorRGBString((255, 255, 255)))
            stdTableBackground.appendChild(tempNode)
            j+= 1
        j= 0
        i+= 1
    ########## end create the background of the rating cells ##########
    
    ########## create the left and right concerns ##########
    i= 0
    meanConcernGroup= xmlDoc.createGNode()
    meanConcernGroup.setId('meanTableConcernGroup')
    rangeConcernGroup= xmlDoc.createGNode()
    rangeConcernGroup.setId('rangeTableConcernGroup')
    stdConcernGroup= xmlDoc.createGNode()
    stdConcernGroup.setId('stdTableConcernGroup')
    while i < len(meanData.concerns):
        #mean
        size= f.getsize(meanData.concerns[i][0])
        y= meanTableYTotalOffset + (i + 1) * meanCellHeight + ((i + 1) * tableLineThickness )  +  (meanCellHeight / 2) + (size[1]/2) - 5
        tempNode= xmlDoc.createSvgTextNode(meanLeftConcernWordOffset, y, meanData.concerns[i][0])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        meanConcernGroup.appendChild(tempNode)
        tempNode= xmlDoc.createSvgTextNode(meanTableXTotalOffset + meanTablesize[0] + meanRightConcernWordOffset, y, meanData.concerns[i][1])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        meanConcernGroup.appendChild(tempNode)
        #range
        size= f.getsize(rangeData.concerns[i][0])
        y= rangeTableYTotalOffset + (i + 1) * rangeCellHeight + ((i + 1) * tableLineThickness )  +  (rangeCellHeight / 2) + (size[1]/2) - 5
        tempNode= xmlDoc.createSvgTextNode(rangeLeftConcernWordOffset, y, rangeData.concerns[i][0])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        rangeConcernGroup.appendChild(tempNode)
        tempNode= xmlDoc.createSvgTextNode(rangeTableXTotalOffset + rangeTablesize[0] + rangeRightConcernWordOffset, y, rangeData.concerns[i][1])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        rangeConcernGroup.appendChild(tempNode)
        #std
        size= f.getsize(stdData.concerns[i][0])
        y= stdTableYTotalOffset + (i + 1) * stdCellHeight + ((i + 1) * tableLineThickness )  +  (stdCellHeight / 2) + (size[1]/2) - 5
        tempNode= xmlDoc.createSvgTextNode(stdLeftConcernWordOffset, y, stdData.concerns[i][0])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        stdConcernGroup.appendChild(tempNode)
        tempNode= xmlDoc.createSvgTextNode(stdTableXTotalOffset + stdTablesize[0] + stdRightConcernWordOffset, y, stdData.concerns[i][1])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize( str(fontSize) + 'px')
        stdConcernGroup.appendChild(tempNode)
        
        i+= 1
    ######### end #create the left and right concerns ##########
    
    ######### create the final document #########
    #add the header
    tempNode= xmlDoc.createSvgTextNode(meanTableXTotalOffset, meanHeaderYOffset + meanHeaderSize[1] - 7, meanData.header)
    tempNode.setFontFamily(fontName)
    tempNode.setFontSize(str(headerFontSize) + 'px')
    meanTableDataGroup.appendChild(tempNode)
    #add the different elements of the mean table
    meanTableDataGroup.appendChild(meanTableHeaderBackgroundGroup)
    meanTableDataGroup.appendChild(meanConcernGroup)
    #add the mean table
    meanTableDataGroup.appendChild(xmlTableMean)
    
    #add the header
    tempNode= xmlDoc.createSvgTextNode(rangeTableXTotalOffset, meanTableYTotalOffset + meanTablesize[1] + rangeHeaderYOffset + rangeHeaderSize[1] - 7, rangeData.header)
    tempNode.setFontFamily(fontName)
    tempNode.setFontSize(str(headerFontSize) + 'px')
    rangeTableDataGroup.appendChild(tempNode)
    #add the different elements of the range table
    rangeTableDataGroup.appendChild(rangeTableHeaderBackgroundGroup)
    rangeTableDataGroup.appendChild(rangeConcernGroup)
    rangeTableDataGroup.appendChild(rangeTableBackground)
    #add the std table
    rangeTableDataGroup.appendChild(xmlTableRange)
    
    #add the headers
    tempNode= xmlDoc.createSvgTextNode(stdTableXTotalOffset, rangeTableYTotalOffset + rangeTablesize[1] + stdHeaderYOffset + stdHeaderSize[1] - 7, stdData.header)
    tempNode.setFontFamily(fontName)
    tempNode.setFontSize(str(headerFontSize) + 'px')
    stdTableDataGroup.appendChild(tempNode)
    #add the different elements of the std table
    stdTableDataGroup.appendChild(stdTableHeaderBackgroundGroup)
    stdTableDataGroup.appendChild(stdConcernGroup)
    stdTableDataGroup.appendChild(stdTableBackground)
    #add the std table
    stdTableDataGroup.appendChild(xmlTableStd)
    
    #add the data to the document
    root.appendChild(meanTableDataGroup)
    root.appendChild(rangeTableDataGroup)
    root.appendChild(stdTableDataGroup)
    
    return xmlDoc.toxml('utf-8')

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
    tableBodyGroupNode= xmlDoc.createGNode()
    tableBodyGroupNode.setId('svgGridTableBody')
    tempNode= xmlDoc.createRectNode(data.xTableOffSet, data.yTableOffSet, tableHeight, tableWidth)
    tempNode.setFill('none')
    tempNode.setStroke(createColorRGBString(data.tableLineColor))
    tempNode.setStrokeWidth(data.lineThickness)
    tableBodyGroupNode.appendChild(tempNode)
    #create the dividing lines in the table
    previousX+= data.xTableOffSet
    previousY+= data.yTableOffSet
    #create the vertical lines
    i= 0
    while i < nvl:
        cw= data.cellWidths[i]
        x= previousX + cw + data.lineThickness
        tempNode= xmlDoc.createLineNode(x, data.yTableOffSet, x, data.yTableOffSet + tableHeight)
        tempNode.setStroke(createColorRGBString(data.tableLineColor))
        tempNode.setStrokeWidth(data.lineThickness)
        tableBodyGroupNode.appendChild(tempNode)
        previousX= x
        i+= 1
    
    #create the horizontal lines
    i= 0
    while i < nhl:
        y= previousY + data.cellHeight + data.lineThickness
        tempNode= xmlDoc.createLineNode(data.xTableOffSet, y, data.xTableOffSet + tableWidth, y) 
        tempNode.setStroke(createColorRGBString(data.tableLineColor))
        tempNode.setStrokeWidth(data.lineThickness)
        i+= 1
        previousY= y
        tableBodyGroupNode.appendChild(tempNode)
    
    mainGnode.appendChild(tableBodyGroupNode)
    #place the text inside the table
    tableCellTextGroupNode= xmlDoc.createGNode()
    tableCellTextGroupNode.setId('svgGridTableCellText')
    i= 0
    j= 0
    
    while i < data.nRows:
        yTotalTableTextOffSet= ((i+ 1) * data.cellHeight) - (data.cellHeight/2)
        if i > 0:
            yTotalTableTextOffSet+= i * data.lineThickness
        # use the floor of data.lineThickness/2, this will cause an error of around 0.5 pixels in the placement
        yTotalTableTextOffSet+= data.lineThickness/2
        while j < data.nCols:
            xTableTextOffSet= 0 # sum of all the cols lenght up to j - 1
            xTotalTableTextOffSet= 0
            if j > 0:
                colPos= 0
                while colPos < j:
                    xTableTextOffSet+= data.cellWidths[colPos]
                    colPos+= 1
                xTotalTableTextOffSet= xTableTextOffSet + (data.lineThickness * j)
            # use the floor of data.lineThickness/2, this will cause an error of around 0.5 pixels in the placement
            xTotalTableTextOffSet+= data.lineThickness/2
            word= data.tableData[i][j]
            if word == None:
                word= ''
            if type(word) != StringType and type(word) != UnicodeType:
                word= str(word)
            size= data.fontObject.getsize(word)
            #word is center aligned
            x= data.xTableOffSet + xTotalTableTextOffSet + data.xWordCellSpace + (data.cellWidths[j] / 2) - (size[0]/2) - 5 
            # -5 is used to correct the placement of the text
            y= data.yTableOffSet + yTotalTableTextOffSet + (size[1]/2) - 5
            tempNode= xmlDoc.createSvgTextNode(x, y, word)
            tempNode.setFontFamily(data.fontName)
            tempNode.setFontSize(str(data.fontSize) + 'px')
            #first row is the header of the table and it has some different settings
            if i == 0:
                tempNode.setFill(createColorRGBString(data.tableHeaderCellWordColor))
            else:
                tempNode.setFill(createColorRGBString(data.tableCellWordColor))
            tableCellTextGroupNode.appendChild(tempNode)
            j+= 1
        j= 0
        i+= 1
    mainGnode.appendChild(tableCellTextGroupNode)
    return mainGnode
    
    
    

#place holder for the variables used in __createSvgTable__
class __TableData___(object):
    
    cellWidths= None #array with the cells width
    cellHeight= None
    nCols= None
    nRows= None
    tableData= None #matrix containing the text that should be displayed in the table
    lineThickness= 1
    xTableOffSet= 0
    yTableOffSet= 0
    xWordCellSpace= 5
    yWordCellSpace= 5
    fontObject= None
    fontName= None
    fontSize= None # in pixels
    tableLineColor= None #tulip, value in rbg
    tableCellWordColor= None #tulip, value in rbg
    tableHeaderCellWordColor= None #tulip, value in rbg

#class used as input to the functions that convert the result to a svg image
class SessionResultImageConvertionData(object):
    
    tableHeader= None #list with the table header (first col)
    tableData= None #matrix with the data of the table
    header= None #string that is used a header for the entire table
    concerns= None

# returns a string with: 'rgb(number,number,number)'
def createColorRGBString(color):
    return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    
    
    
    