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
        
        #add xWordCellSpace * 2 to each position of the array
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
            size= data.fontObject.getsize(str(word))
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
    tableData= None #mtraix containing the text that should be displayed in the table
    lineThickness= 1
    lineColor= None
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

# returns a string with: 'rgb(number,number,number)'
def createColorRGBString(color):
    return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    
    
    
    