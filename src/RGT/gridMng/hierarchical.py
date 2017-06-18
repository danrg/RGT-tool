'''
Created on Feb 17, 2012

@author: Gray
'''
from math import sqrt, floor
import sys

from RGT.XML.SVG.svgDOMImplementation import SvgDOMImplementation
from PIL import Image, ImageDraw, ImageFont #@UnresolvedImport
from RGT.settings import DENDROGRAM_FONT_LOCATION


#calculate the linkage of the distance matrix.
class MaxLinkageAlgorithm:
    """
    The calculateLinkage method compares all the distances found in row[rowNumber][colNumber] and returns the one that is the largest. colNumber are the numbers found in colNumbers
    matrix format= [    [[], [name1], [name2], [name3], ...]
                         [[name1], value1, value2, value3, ....]
                         [[name2], value1, value2, value3, ....]
                         [[name3], value1, value2, value3, ....]
                         [....]
                    ]
    
    rowNumber= int
    colNumbers= [int, int,...] -> the col number of a cell in the row of the matrix
    return int
    """

    @staticmethod
    def calculateLinkage(matrix, rowNumber, colNumbers):
        base = colNumbers.pop()
        if len(colNumbers) >= 1:
            return max(matrix[rowNumber][base], MaxLinkageAlgorithm.calculateLinkage(matrix, rowNumber, colNumbers))
        else:
            return matrix[rowNumber][base]

# create the distance matrix based on the euclidean distance (n dimensions)    
class EuclideanDistanceAlgorithm:
    @staticmethod
    def calculateDistance(matrix):
        r = 0;
        distanceMatrix = [[[]]];
        nRow = len(matrix);

        #create the distance matrix, format is:
        """
            [    [[], [name1], [name2], [name3], ...]
                 [[name1], value1, value2, value3, ....]
                 [[name2], value1, value2, value3, ....]
                 [[name3], value1, value2, value3, ....]
                 [....]
            ]
        """
        while r < nRow:
            columns = [[]]; # the columns that will be added to the distance matrix
            currentRow = matrix[r];
            nCol = len(matrix[r]);
            distance = 0;
            i = 0;
            j = 1; #first columns is a string
            #calculate the distance for all the elements of the r row of the matrix and add the result to the distance matrix
            while i < nRow:
                while j < nCol:
                    temp = (currentRow[j] - matrix[i][j]);
                    distance += temp * temp;
                    j += 1;
                i += 1;
                j = 1;
                columns.append(sqrt(distance));
                distance = 0;
            i = 0;
            distanceMatrix.append(columns);
            distanceMatrix[r + 1][0] = [matrix[r][0]];
            r += 1;
        r = 0;
        #add the names to the first column of each row
        while r < nRow:
            distanceMatrix[0].append([matrix[r][0]]);
            r += 1;

        return distanceMatrix


def hcluster(matrix, distanceAlgorithm=EuclideanDistanceAlgorithm(), linkageAlgorithm=MaxLinkageAlgorithm()):
    # create the distance matrix based on the euclidean distance (n dimensions)
    distanceMatrix = distanceAlgorithm.calculateDistance(matrix)
    #now lets make the cluster
    result = []; #each position in result represent the found cluster in step n

    maxSteps = 100;
    i = 0;

    while i < maxSteps:
        nRow = len(distanceMatrix);
        j = 1;
        bestDistances = None
        distance = sys.maxint;

        while j < nRow:
            k = 1 + j;
            while k < nRow:
                temp = distanceMatrix[j][k];
                if j != k and distance > temp:
                    distance = temp;
                    bestDistances = [(j, k)]
                elif j != k and distance == temp:
                    #we are only checking 1/2 of the matrix, so the results will be unique
                    bestDistances.append((j, k));
                k += 1;
            j += 1
        tempCluster = []
        yPositions = []
        #get the names of all the clusters that have the same distance
        for position in bestDistances:
            #to check if the cluster is already present we need to remove the array around it that is because we use  distanceMatrix[0][position[1]][0], so we can get the string
            if not distanceMatrix[0][position[1]][0] in tempCluster:
                tempCluster += distanceMatrix[0][position[1]]
                yPositions.append(position[1])
            if not distanceMatrix[position[0]][0][0] in tempCluster:
                tempCluster += distanceMatrix[position[0]][0]
                yPositions.append(position[0])
        result.append((tempCluster, distance))

        #now lets update the distance matrix
        j = 1;
        newCol = [[]];
        maxDistance = -1;
        yPositions.sort() # this list needs to be sorted because later on we wills start deleting stuff so the position of the deletion must be from smaller to bigger
        while j < nRow:
            if not j in yPositions:
                maxDistance = linkageAlgorithm.calculateLinkage(distanceMatrix, j, yPositions[:]);
                distanceMatrix[j].append(maxDistance);
                k = 0
                while k < len(yPositions):
                    del distanceMatrix[j][yPositions[k] - k];
                    k += 1
                newCol.append(maxDistance);
            j += 1;

        newCol.append(0.0);
        #newCol[0]= result[i]
        newCol[0] = result[i][
            0]; # result contains tuples, thus i right now i want result at position i and the 1st object in the tuple, that would be the array of names
        distanceMatrix.append(newCol);

        #delete the old columns that separately formed the new cluster
        j = 0
        while j < len(yPositions):
            #the y position can be used as x as 1/2 of distance matrix is a reflection of the other 1/2 
            del distanceMatrix[yPositions[j] - j];
            j += 1

        # now fix the first row of the matrix
        j = 0
        while j < len(yPositions):
            del distanceMatrix[0][yPositions[j] - j];
            j += 1
        distanceMatrix[0].append(result[i][0]);

        #check if we have merged all the clusters if so stop
        if len(distanceMatrix) == 2: # this is 2 because we have 1 extra row that identify the clusters 
            break;
        i += 1;

    return result;


def pcaCluster(matrix, distanceAlgorithm=EuclideanDistanceAlgorithm(), linkageAlgorithm=MaxLinkageAlgorithm()):
    # create the distance matrix based on the euclidean distance (n dimensions)
    distanceMatrix = distanceAlgorithm.calculateDistance(matrix)
    return distanceMatrix


def drawDendogram(clusters=[]):
    #cluster format is: [([element1, elemet2], distance), ([element1, elemet2, element3], distance), ......]

    #now lets first calculate the size of the image and stuff like that
    h = len(clusters[len(clusters) - 1][
        0]) + 2 * 100 # get the total number of elements of the last 'cluster' as it should contain all the elements
    w = 1200
    #depth= len(clusters)
    #scaling= float(w - 150)/depth
    f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, 15)
    # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    #draw.line((0,h/2,10,h/2),fill=(255,0,0))
    #lets draw stuff now

    #lets first draw all the individual items, the last sub-cluster should contain all of them
    allClusters = [] # format is ([item1, item2,...], positionX, positionY)
    i = 0;
    while i < len(clusters[len(clusters) - 1][0]):
        allClusters.append(((clusters[len(clusters) - 1][0])[i], 10, 30 * (i + 1)))
        i += 1
        #now draw the initial clusters
    temp = []
    for cluster in allClusters:
        draw.text((cluster[1], cluster[2]), cluster[0], font=f, fill=(0, 0, 0));
        # now reset the y position to the middle of the word and the x to the end of the word, this is the point where the line will start
        (width, height) = f.getsize(cluster[0])
        temp.append(( cluster[0], cluster[1] + width + 3, cluster[2] + (height / 2) ))
    allClusters = temp
    #ok now lets start drawing the combined clusters
    i = 0
    xPositionNewCluster = 0; # the xPosition of a new cluster will be fix and based on the previous run
    while i < len(clusters):
        cluster = clusters[i]
        mainClusterSet = set(cluster[0])
        subSetClusters = []
        j = 0
        #find from which sub-clusters is the main cluster composed of
        while j < len(allClusters):
            temp = (allClusters[j])[
                0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
            if type(temp) is str:
                temp = [temp]
            if set(temp).issubset(mainClusterSet):
                subSetClusters.append(allClusters[j])
                if (len(subSetClusters) >= len(cluster[0])):
                    break;
            j += 1;
            #now draw the lines of the old clusters to the new cluster
        #assumption, because we created the initial clusters from the last cluster(where we have all the clusters in 1) the position of the sub-clusters are ideal, in terms that they are next to each other after each round
        #xPositionNewCluster= 0
        yPositionNewCluster = 0
        temp = 0 #will be used as the biggest y
        temp2 = 0 #will be used as the smallest y
        j = 0
        while j < len(subSetClusters):
            if j == 0:
                temp = (subSetClusters[j])[2]
                temp2 = (subSetClusters[j])[2]
                if i == 0:
                    xPositionNewCluster = (subSetClusters[j])[1]
                    #xPositionNewCluster= (subSetClusters[j])[1]
            else:
                if (subSetClusters[j])[2] > temp:
                    temp = (subSetClusters[j])[2]
                if (subSetClusters[j])[2] < temp2:
                    temp2 = (subSetClusters[j])[1]
                    #if (subSetClusters[j])[1] > xPositionNewCluster:
                    #    xPositionNewCluster= (subSetClusters[j])[1]
            j += 1
        xPositionNewCluster += 50
        yPositionNewCluster = temp2 + (temp - temp2) / 2

        for subCluser in subSetClusters:
            draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255, 0, 0))
            draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255, 0, 0))

            # now remove the old clusters from allClusters
            allClusters.remove(subCluser)
            #now add the new cluster to allClusters
        allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
        i += 1
        #lets save the image
    return img


def transpose(lists):
    if not lists: return []
    return map(lambda *row: list(row), *lists)


#this function will have the percentage rule, size (width) will also be based on the amount of cluster
def drawDendogram2(clustersConcern=[], clustersAlternative=[], matrix=[[]], maxMatrixCellValue=1):
    #cluster format is: [([element1, elemet2], distance), ([element1, elemet2, element3], distance), ......]

    #########################
    ###changeable settings###
    #########################

    f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, 15)

    imageBackgroundColor = (255, 255, 255) #value in rbg

    ###table settings###
    xWordTableOffset = 10 #value in pixel, offset of the longest word of the left side of the table in relation to the left of the picture
    xWordToTableOffset = 5 #value in pixel, offset of a word (left or right) to the table, example: word1 <--xWordToTableOffset--> |table| <--xWordToTableOffset--> word2
    yTableTopOffset = 10
    ###color settings###
    tableLineColor = (60, 179, 113) #value in rbg
    tableWordColor = (70, 130, 180) #value in rbg
    tableCellWordColor = (60, 179, 113) #value in rbg
    tableToAlternativesConnectionLineColor = (188, 143, 143) #value in rbg

    ###dendogram settings###

    ###color settings###
    concernDendogramLineColor = (255, 0, 0) #value in rbg
    alternativeDendogramLineColor = (255, 0, 0) #value in rbg
    ###ruler settings###
    baseRulerStep = 25 #base amount of pixels between every 10 steps of the rule example: |10 |20 |30.....|100 = |10 <--25pixels--> |20 <--25pixels--> |30 ......
    xOffsetLineToRuler = 20 # amount in pixels, this amount is used set the X start position that the ruler starts example : concern1 <-xOffsetWordToLine-> <---xOffsetLineToRuler---> |100  |90  |80....
    xOffsetWordToLine = 5 # amount in pixel, offset of where to start drawing the initial line from the word example : concern1 <-xOffsetWordToLine-> <---xOffsetLineToRuler---> |100  |90  |80....
    rulerVerticalLineSize = 5 #value in pixel
    rulerStepIncrease = 20 #value in pixel, this value is used with the number of initial clusters in a dendogram to calculate the final size of each rule step, equation is (nInitialClusters * rulerStepIncrease) + baseRulerStep
    ###specific settings###
    yConcernRulerOffset = 10 #value in pixel, offset from the ceiling of the picture to the top of the percentage numbers
    yAlternativeRulerOffset = 10 #value in pixel, off from the bottom of the table to the top of the percentage numbers
    yConcerPercentageToRulerOffset = 3 #value in pixel, distance between the percentage number and the ruler
    yAlternativePercentageToRulerOffset = 3 #value in pixel, distance between the percentage number and the ruler
    ###color settings###
    concernRulerColor = (255, 0, 0) #value in rbg
    concernRulerPerncetageColor = (255, 0, 0)# value in rbg
    alternativeRulerColor = (255, 0, 0) #value in rbg
    alternativeRulerPerncetageColor = (255, 0, 0)# value in rbg
    alternativeWordColor = (244, 164, 96) #value in rbg

    ###########################
    ###unchangeable settings###
    ###########################

    tableLineThickness = 1 #do not change this value

    ######################
    ###global variables###
    ######################

    concernClusterSimilarity = []
    alternativeClusterSimilarity = []
    dicMatrixConcernToWordEndPosition = {} #this is use to map words in the table that was drawn to where the last pixel is of the left, we need this to map the words of the concern dendogram
    cellAlternativesXPositions = {} #middle position of the cell that corresponds to the given alternative
    percentageWordSize = f.getsize(str(100))

    ###table variables###
    ###word variables###
    leftConcernMaxWordWidth = -1
    rightConcernMaxWordWidth = -1
    leftConcernMaxWordHeight = -1
    rightConcernMaxWordHeight = -1
    rightConcenrMaxX = -1
    alternativeMaxWordWidth = -1
    alternativeMaxWordHeight = -1
    ###cells variables###
    tableCellWidth = -1
    tableCellHeight = -1 #@UnusedVariable
    yTableBottom = -1 #@UnusedVariable
    ###ruler variables###
    xConcernRulerStartPoint = -1 #@UnusedVariable
    xAlternativeRulerStartPoint = -1 #@UnusedVariable
    concernRulerLength = -1 #@UnusedVariable
    alternativeRulerLength = -1 #@UnusedVariable
    nConcernRulerSteps = -1 #@UnusedVariable
    nAlternativRulerSteps = -1 #@UnusedVariable

    ################
    #pre-processing#
    ################


    #find the min similarity of the concern
    for cluster in clustersConcern:
        concernClusterSimilarity.append(100 * (1 - (cluster[1] / ((len(matrix) - 1) * (maxMatrixCellValue - 1)))))
        #find the min similarity of the alternatives
    for cluster in clustersAlternative:
        alternativeClusterSimilarity.append(
            100 * (1 - (cluster[1] / ((len(matrix[0]) - 2) * (maxMatrixCellValue - 1)))))

    #calculate the ruler step size
    concernRulerStep = (len(clustersConcern) * rulerStepIncrease) + baseRulerStep
    alternativeRulerStep = (len(clustersAlternative) * rulerStepIncrease) + baseRulerStep

    #find the max word width of the left and right side of the table and the size of the cells
    for row in matrix:
        maxValue = max(row[1: len(row) - 1])
        #the first row is special as it only contains the names of the alternatives, thus skip it
        if type(maxValue) != str:
            if tableCellWidth < maxValue:
                tableCellWidth = maxValue
            size = f.getsize(row[0])
            if size[0] > leftConcernMaxWordWidth:
                leftConcernMaxWordWidth = size[0]
            if size[1] > leftConcernMaxWordHeight:
                leftConcernMaxWordHeight = size[1]
            size = f.getsize(row[len(row) - 1])
            if size[0] > rightConcernMaxWordWidth:
                rightConcernMaxWordWidth = size[0]
            if size[1] > rightConcernMaxWordHeight:
                rightConcernMaxWordHeight = size[1]

    (tableCellWidth, tableCellHeight) = f.getsize(str(tableCellWidth))
    #the height of the cell should be a little bigger then the max word height
    if rightConcernMaxWordHeight > leftConcernMaxWordHeight:
        if rightConcernMaxWordHeight > tableCellHeight:
            tableCellHeight = rightConcernMaxWordHeight
    else:
        if leftConcernMaxWordHeight > tableCellHeight:
            tableCellHeight = leftConcernMaxWordHeight
    tableCellWidth += 4
    tableCellHeight += 4

    for word in matrix[0]:
        if type(word) == str:
            temp = f.getsize(word)
            if temp[1] > alternativeMaxWordHeight:
                alternativeMaxWordHeight = temp[1]


                #####--->>>>       #TODO calculate the max height of a word

    #determine the number of steps the concern ruler has
    temp = int(min(concernClusterSimilarity))
    if 100 > temp >= 90:
        temp = 1
    elif 90 > temp >= 80:
        temp = 2
    elif 80 > temp >= 70:
        temp = 3
    elif 70 > temp >= 60:
        temp = 4
    elif 60 > temp >= 50:
        temp = 5
    elif 50 > temp >= 40:
        temp = 6
    elif 40 > temp >= 30:
        temp = 7
    elif 30 > temp >= 20:
        temp = 8
    elif 20 > temp >= 10:
        temp = 9
    elif 10 > temp >= 0:
        temp = 10
    concernRulerLength = temp * concernRulerStep
    nConcernRulerSteps = temp

    #determine the number of steps the alternative ruler has
    temp = int(min(alternativeClusterSimilarity))
    if 100 > temp >= 90:
        temp = 1
    elif 90 > temp >= 80:
        temp = 2
    elif 80 > temp >= 70:
        temp = 3
    elif 70 > temp >= 60:
        temp = 4
    elif 60 > temp >= 50:
        temp = 5
    elif 50 > temp >= 40:
        temp = 6
    elif 40 > temp >= 30:
        temp = 7
    elif 30 > temp >= 20:
        temp = 8
    elif 20 > temp >= 10:
        temp = 9
    elif 10 > temp >= 0:
        temp = 10
    alternativeRulerLength = temp * alternativeRulerStep
    nAlternativRulerSteps = temp

    #find the max width of the words in the alternative dendogram
    for word in matrix[0]:
        #again the first row is special so skip it
        if word != []:
            size = f.getsize(word)
            if size[0] > alternativeMaxWordWidth:
                alternativeMaxWordWidth = size[0]

    #determine the width and height of the picture
    h = yTableTopOffset + (tableCellHeight * len(matrix)) + yAlternativeRulerOffset + (
        (len(matrix[0]) - 2) * tableCellHeight) + (alternativeMaxWordHeight * (len(matrix[0]) - 2)) + \
        percentageWordSize[1] + yConcernRulerOffset + 10


    w = xWordTableOffset + (xWordToTableOffset * 2) + (
        (len(matrix[0]) - 2) * tableCellWidth) + leftConcernMaxWordWidth + percentageWordSize[0]
    if rightConcernMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + concernRulerLength > alternativeMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + alternativeRulerLength:
        w += rightConcernMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + concernRulerLength
    else:
        w += alternativeMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + alternativeRulerLength

        #create new matrix based on the order of the concern and alternative clusters
    tempMatrix = [None] * len(matrix)
    concernIndexToName = {}
    alternativeIndexToName = {}
    concernNameToIndex = {}
    alternativeNameToIndex = {}
    i = 1
    firstRow = [[]]

    #create the map of the old matrix to the new matrix
    while i < len(matrix):
        concernIndexToName[i] = (matrix[i][0], matrix[i][len(matrix[0]) - 1])
        i += 1
    i = 1
    while i < (len(matrix[0]) - 1):
        alternativeIndexToName[i] = matrix[0][i]
        i += 1

    i = 0
    temp = clustersConcern[len(clustersConcern) - 1][0]
    while i < len(temp):
        concernNameToIndex[temp[i]] = i + 1
        i += 1
    i = 0
    temp = clustersAlternative[len(clustersAlternative) - 1][0]
    nCol = len(clustersAlternative[len(clustersAlternative) - 1][0])
    while i < len(temp):
        alternativeNameToIndex[temp[
            i]] = nCol - i #nCol - i is to invert the position of the alternative so the line that we will draw from the table to the alternative names will look good, also the result of the equation is the index for the new table, no correction is needed as the values of the alternatives start at index 1
        firstRow.append(temp[i])
        i += 1
    firstRow.append([])
    i = 1
    j = 1

    #create the new matrix
    while i < len(matrix):
        tempRow = [None] * len(matrix[0])
        while j < len(matrix[0]) - 1:
            index = alternativeNameToIndex[alternativeIndexToName[j]]
            tempRow.insert(index, matrix[i][j])
            tempRow.pop(index + 1)
            if i == 1:
                cellAlternativesXPositions[alternativeIndexToName[j]] = ((index - 1) * tableCellWidth) + (
                    tableCellWidth / 2) + xWordTableOffset + xWordToTableOffset + leftConcernMaxWordWidth
            j += 1
        tempRow.insert(0, matrix[i][0])
        tempRow.pop(1)
        tempCalculcation = len(matrix[i]) - 1
        tempRow.insert(tempCalculcation, matrix[i][tempCalculcation])
        tempRow.pop(tempCalculcation + 1)
        temp = concernIndexToName[i]
        index = -1
        if concernNameToIndex.has_key(temp[0]):
            index = concernNameToIndex[temp[0]]
        else:
            index = concernNameToIndex[temp[1]]
        tempMatrix.insert(index, tempRow)
        tempMatrix.pop(index + 1)
        i += 1
        j = 1
    tempMatrix.insert(0, firstRow)
    tempMatrix.pop(1)
    #print tempMatrix
    matrix = tempMatrix

    #######end pre-processing #########

    #depth= len(clustersConcern)
    #scaling= float(w - 150)/depth

    # Create a new image with a white background
    img = Image.new('RGB', (w, h), imageBackgroundColor)
    draw = ImageDraw.Draw(img)
    #lets draw stuff now

    ################
    ###table draw###
    ################

    yTableStartPosition = yTableTopOffset + percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset
    xtableStartPosition = xWordToTableOffset + xWordTableOffset + leftConcernMaxWordWidth
    draw.line([(xtableStartPosition, yTableStartPosition),
               (xtableStartPosition + ( tableCellWidth * (len(matrix[0]) - 2)), yTableStartPosition)],
              fill=tableLineColor, width=tableLineThickness)
    #remember to add + tableLineThickness to the start position to account for the line thickness, that also goes for the right, left and bottom

    #now lets drawn the table row by row
    i = 1;
    j = 0;
    while i < len(matrix):
        row = matrix[i]
        #draw the left word
        wordSize = f.getsize(row[0])
        #draw.text((xtableStartPosition - xWordToTableOffset - wordSize[0], yTableStartPosition + (((i - 1) * tableCellHeight) + ((tableCellHeight/2) - (wordSize[1]/2))) ), row[0], font= f, fill= tableWordColor)
        draw.text((xtableStartPosition - xWordToTableOffset - wordSize[0],
                   yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight / 2) ),
                  row[0], font=f, fill=tableWordColor)
        while j < len(row) - 2:
            if j == 0:
                #draw the left line
                draw.line([(xtableStartPosition, yTableStartPosition + ( (i - 1) * tableCellHeight)),
                           ( xtableStartPosition, yTableStartPosition + ( i * tableCellHeight) )], fill=tableLineColor,
                          width=tableLineThickness)
                #draw the values of the cells
            cell = row[j + 1]
            wordSize = f.getsize(str(cell))
            #xCellValue= xtableStartPosition + (tableCellWidth * j) + (tableCellWidth / 2) - (wordSize[0] / 2)
            #xCellValue= xtableStartPosition + ((j * tableCellWidth) + ((tableCellWidth/2) - (wordSize[0]/2)))
            #yCellValue= yTableStartPosition + (tableCellHeight * (i - 1)) + (tableCellHeight / 2) - (wordSize[1] / 2)
            #yCellValue= yTableStartPosition + (( (i- 1) * tableCellHeight) + ((tableCellHeight/2) - (wordSize[1]/2)))
            xCellValue = xtableStartPosition + (j * tableCellWidth) + floor((tableCellWidth - wordSize[0]) / 2)
            yCellValue = yTableStartPosition + ((i - 1) * tableCellHeight) + floor((tableCellHeight - wordSize[1]) / 2)
            draw.text((xCellValue, yCellValue), str(cell), font=f, fill=tableCellWordColor)
            #draw.line( [(xtableStartPosition + (j * tableCellWidth), yTableStartPosition + ((i-1) * tableCellHeight)), (xtableStartPosition + (j * tableCellWidth) + wordSize[0], yTableStartPosition + ((i-1) * tableCellHeight))], fill= (0,0,0), width= tableLineThickness)
            #diagonal
            #draw.line( [(xCellValue, yCellValue),(xCellValue + wordSize[0], yCellValue +  wordSize[1])], fill= (0,0,0), width= tableLineThickness)
            #draw.line( [(xtableStartPosition + ( j * tableCellWidth ), yTableStartPosition + ( (i-1) * tableCellHeight)), (xtableStartPosition + ( (j+1) * tableCellWidth ), yTableStartPosition + ( (i-1) * tableCellHeight))], fill= (0,0,0), width= tableLineThickness)
            #draw.line( [(xtableStartPosition + ( j * tableCellWidth ), yTableStartPosition + ( i * tableCellHeight)), (xtableStartPosition + ( (j+1) * tableCellWidth ), yTableStartPosition + ( i * tableCellHeight))], fill= tableLineColor, width= tableLineThickness)
            if j == len(row) - 3:
                #draw right line
                draw.line([(xtableStartPosition + ( (j + 1) * tableCellWidth),
                            yTableStartPosition + ( (i - 1) * tableCellHeight)), (
                               xtableStartPosition + ( (j + 1) * tableCellWidth),
                               yTableStartPosition + (i * tableCellHeight) )], fill=tableLineColor,
                          width=tableLineThickness)
            j += 1
            #draw the right word
        wordSize = f.getsize(row[len(row) - 1])
        draw.text((xtableStartPosition + (tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness,
                   yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight / 2) ),
                  row[len(row) - 1], font=f, fill=tableWordColor)
        dicMatrixConcernToWordEndPosition[row[0]] = (
            wordSize[0] + xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness,
            yTableStartPosition + (tableCellHeight * (i - 1)) + (wordSize[1] / 2) )
        dicMatrixConcernToWordEndPosition[row[len(row) - 1]] = dicMatrixConcernToWordEndPosition[row[0]]
        if rightConcenrMaxX < xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness + rightConcernMaxWordWidth:
            rightConcenrMaxX = xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness + rightConcernMaxWordWidth
        j = 0
        i += 1
        #draw the bottom line
    yTableBottom = yTableStartPosition + (tableCellHeight * (len(matrix) - 1) )
    draw.line([(xtableStartPosition, yTableBottom ),
               (xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ), yTableBottom )], fill=tableLineColor,
              width=tableLineThickness)

    ####### end table draw #########

    ############################
    ###Concern dendogram draw###
    ############################

    #lets first draw all the individual items, the last sub-cluster should contain all of them
    allClusters = [] # format is ([item1, item2,...], positionX, positionY)
    i = 0;
    while i < len(clustersConcern[len(clustersConcern) - 1][0]):
        temp = clustersConcern[len(clustersConcern) - 1][0]
        wordEndPosition = dicMatrixConcernToWordEndPosition[temp[i]]
        #save the positions we want
        allClusters.append((temp[i], wordEndPosition[0], wordEndPosition[1]))
        i += 1

    xConcernRulerStartPoint = rightConcenrMaxX + xOffsetWordToLine + xOffsetLineToRuler
    #now reset all the x to the max word length + an offset
    temp = []
    for cluster in allClusters:
        newX = xConcernRulerStartPoint #xOffsetWordToLine + cluster[1] + (rightConcenrMaxX - cluster[1]) + xOffsetLineToRuler
        draw.line([(cluster[1] + xOffsetWordToLine, cluster[2]), ( newX, cluster[2])], fill=concernDendogramLineColor)
        temp.append((cluster[0], newX, cluster[2]))
    allClusters = temp;
    #now lets draw the ruler
    draw.line([(xConcernRulerStartPoint, percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset),
               (xConcernRulerStartPoint + concernRulerLength,
                percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset)], fill=concernRulerColor)
    i = 0
    #draw the markers of the ruler
    while i <= nConcernRulerSteps:
        percentage = str(100 - (i * 10))
        draw.text(
            ( xConcernRulerStartPoint + (concernRulerStep * i) - (f.getsize(percentage)[0] / 2), yConcernRulerOffset ),
            text=percentage, fill=concernRulerPerncetageColor, font=f)
        draw.line([(xConcernRulerStartPoint + (concernRulerStep * i),
                    percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset), (
                       (xConcernRulerStartPoint + (concernRulerStep * i)), percentageWordSize[
                                                                               1] + yConcernRulerOffset + yConcerPercentageToRulerOffset + rulerVerticalLineSize)],
                  fill=concernRulerColor)
        i += 1

    #ok now lets start drawing the combined clustersConcern
    i = 0
    xPositionNewCluster = 0; # the xPosition of a new cluster will be fix and based on the previous run
    while i < len(clustersConcern):
        cluster = clustersConcern[i]
        mainClusterSet = set(cluster[0])
        subSetClusters = []
        j = 0
        #find from which sub-clustersConcern is the main cluster composed of
        while j < len(allClusters):
            temp = (allClusters[j])[
                0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
            if type(temp) is str:
                temp = [temp]
            if set(temp).issubset(mainClusterSet):
                subSetClusters.append(allClusters[j])
                if (len(subSetClusters) >= len(cluster[0])):
                    break;
            j += 1;
            #now draw the lines of the old clustersConcern to the new cluster
        #assumption, because we created the initial clustersConcern from the last cluster(where we have all the clustersConcern in 1) the position of the sub-clustersConcern are ideal, in terms that they are next to each other after each round
        #xPositionNewCluster= 0
        yPositionNewCluster = 0
        temp = 0 #will be used as the biggest y
        temp2 = 0 #will be used as the smallest y
        j = 0
        while j < len(subSetClusters):
            if j == 0:
                temp = (subSetClusters[j])[2]
                temp2 = (subSetClusters[j])[2]
                if i == 0:
                    xPositionNewCluster = (subSetClusters[j])[1]
                    #xPositionNewCluster= (subSetClusters[j])[1]
            else:
                if (subSetClusters[j])[2] > temp:
                    temp = (subSetClusters[j])[2]
                if (subSetClusters[j])[2] < temp2:
                    temp2 = (subSetClusters[j])[1]
                    #if (subSetClusters[j])[1] > xPositionNewCluster:
                    #    xPositionNewCluster= (subSetClusters[j])[1]
            j += 1
            #calculate the offset from the beginning of the ruler that xPositionNewCluster should be
        #assumption, ruler starts from 100 thus: |100 |90 |80......
        # concernRulerStep/10 -> every step = 10% thus this calculation give us the amount of pixels that 1% represents. 100 - concernClusterSimilarity[i] -> this calculation gives us the percentage that a percentage is away from 100%.
        xPositionNewCluster = (
                                  (concernRulerStep / 10) * (
                                      100 - concernClusterSimilarity[i]) ) + xConcernRulerStartPoint
        yPositionNewCluster = temp2 + (temp - temp2) / 2

        for subCluser in subSetClusters:
            draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, yPositionNewCluster)],
                      fill=concernDendogramLineColor)
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255,0,0))
            #draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255,0,0))

            # now remove the old clustersConcern from allClusters
            allClusters.remove(subCluser)
            #now add the new cluster to allClusters
        allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
        i += 1

    ####### end concern dendogram draw #########

    ################################
    ###Alternative dendogram draw###
    ################################

    allClusters = [] # format is ([item1, item2,...], positionX, positionY)
    i = 0;
    while i < len(clustersAlternative[len(clustersAlternative) - 1][0]):
        allClusters.append(((clustersAlternative[len(clustersAlternative) - 1][0])[i],
                            xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ) + xWordToTableOffset,
                            yTableStartPosition + (tableCellHeight * len(matrix)) + (
                                tableCellHeight * (i)) + yAlternativeRulerOffset + percentageWordSize[
                                1] + yAlternativePercentageToRulerOffset ))
        i += 1
        #now draw the initial clustersAlternative
    temp = []
    maxWordLength = -1
    for cluster in allClusters:
        draw.text((cluster[1], cluster[2]), cluster[0], font=f, fill=alternativeWordColor);
        # now reset the y position to the middle of the word and the x to the end of the word, this is the point where the line will start
        (width, height) = f.getsize(cluster[0])
        temp.append(( cluster[0], cluster[1] + width, cluster[2] + (height / 2) ))
        if maxWordLength < width:
            maxWordLength = width
            #draw the lines that connect the table with the alternative names
        draw.line([(cellAlternativesXPositions[cluster[0]], yTableBottom + 1),
                   (cellAlternativesXPositions[cluster[0]], cluster[2] + (height / 2))],
                  fill=tableToAlternativesConnectionLineColor)
        draw.line([(cellAlternativesXPositions[cluster[0]], cluster[2] + (height / 2)),
                   (cluster[1] - 2, cluster[2] + (height / 2))], fill=tableToAlternativesConnectionLineColor)
    allClusters = temp
    xAlternativeRulerStartPoint = maxWordLength + xOffsetWordToLine + xOffsetLineToRuler + xtableStartPosition + (
        tableCellWidth * (len(matrix[0]) - 2) )
    yAlternativeRulerStartPoint = yAlternativeRulerOffset + percentageWordSize[
        1] + yAlternativePercentageToRulerOffset + yTableBottom
    #now reset all the x to the max word length + an offset
    temp = []
    for cluster in allClusters:
        newX = xAlternativeRulerStartPoint
        draw.line([(cluster[1] + xOffsetWordToLine, cluster[2]), ( newX, cluster[2])],
                  fill=alternativeDendogramLineColor)
        temp.append((cluster[0], newX, cluster[2]))
    allClusters = temp;
    #now lets draw the ruler
    draw.line([(xAlternativeRulerStartPoint, yAlternativeRulerStartPoint),
               (xAlternativeRulerStartPoint + alternativeRulerLength, yAlternativeRulerStartPoint)],
              fill=alternativeRulerColor)
    i = 0
    #draw the markers of the ruler
    while i <= nAlternativRulerSteps:
        percentage = str(100 - (i * 10))
        wordSize = f.getsize(percentage)
        draw.text((xAlternativeRulerStartPoint + (alternativeRulerStep * i) - (wordSize[0] / 2),
                   yAlternativeRulerStartPoint - yAlternativePercentageToRulerOffset - wordSize[1]), text=percentage,
                  fill=alternativeRulerPerncetageColor, font=f)
        draw.line([(xAlternativeRulerStartPoint + (alternativeRulerStep * i), yAlternativeRulerStartPoint), (
            (xAlternativeRulerStartPoint + (alternativeRulerStep * i)),
            yAlternativeRulerStartPoint + rulerVerticalLineSize)], fill=alternativeRulerColor)
        i += 1

    #ok now lets start drawing the combined clustersAlternative
    i = 0
    xPositionNewCluster = 0; # the xPosition of a new cluster will be fixed and based on the previous run
    while i < len(clustersAlternative):
        cluster = clustersAlternative[i]
        mainClusterSet = set(cluster[0])
        subSetClusters = []
        j = 0
        #find from which sub-clustersConcern is the main cluster composed of
        while j < len(allClusters):
            temp = (allClusters[j])[
                0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
            if type(temp) is str:
                temp = [temp]
            if set(temp).issubset(mainClusterSet):
                subSetClusters.append(allClusters[j])
                if (len(subSetClusters) >= len(cluster[0])):
                    break;
            j += 1;
            #now draw the lines of the old clustersAlternative to the new cluster
        #assumption, because we created the initial clustersAlternative from the last cluster(where we have all the clustersAlternative in 1) the position of the sub-clustersAlternative are ideal, in terms that they are next to each other after each round
        #xPositionNewCluster= 0
        yPositionNewCluster = 0
        temp = 0 #will be used as the biggest y
        temp2 = 0 #will be used as the smallest y
        j = 0
        while j < len(subSetClusters):
            if j == 0:
                temp = (subSetClusters[j])[2]
                temp2 = (subSetClusters[j])[2]
                if i == 0:
                    xPositionNewCluster = (subSetClusters[j])[1]
                    #xPositionNewCluster= (subSetClusters[j])[1]
            else:
                if (subSetClusters[j])[2] > temp:
                    temp = (subSetClusters[j])[2]
                if (subSetClusters[j])[2] < temp2:
                    temp2 = (subSetClusters[j])[1]
                    #if (subSetClusters[j])[1] > xPositionNewCluster:
                    #    xPositionNewCluster= (subSetClusters[j])[1]
            j += 1
            #calculate the offset from the beginning of the ruler that xPositionNewCluster should be
        #assumption, ruler starts from 100 thus: |100 |90 |80......
        # alternativeRulerStep/10 -> every step = 10% thus this calculation give us the amount of pixels that 1% represents. 100 - concernClusterSimilarity[i] -> this calculation gives us the percentage that a percentage is away from 100%.
        xPositionNewCluster = ((alternativeRulerStep / 10) * (
            100 - alternativeClusterSimilarity[i]) ) + xAlternativeRulerStartPoint
        yPositionNewCluster = temp2 + (temp - temp2) / 2

        for subCluser in subSetClusters:
            draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, yPositionNewCluster)],
                      fill=alternativeDendogramLineColor)
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255,0,0))
            #draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255,0,0))

            # now remove the old clustersConcern from allClusters
            allClusters.remove(subCluser)
            #now add the new cluster to allClusters
        allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
        i += 1

    ####### end alternative dendogram draw #########

    #lets return the image
    return img

#this is much of the original code to create 1 dendogram, start variables declaration are missing
"""
#lets first draw all the individual items, the last sub-cluster should contain all of them
allClusters= [] # format is ([item1, item2,...], positionX, positionY)
i= 0;
while i <  len(clustersConcern[len(clustersConcern) - 1][0]):
    allClusters.append(((clustersConcern[len(clustersConcern) - 1][0])[i], 10, yOffsetWordToWord * (i + 1)))
    i+= 1
#now draw the initial clustersConcern
temp= []
maxWordLength= -1
for cluster in allClusters:
    draw.text((cluster[1], cluster[2]), cluster[0], font= f, fill=(0,0,0));
    # now reset the y position to the middle of the word and the x to the end of the word, this is the point where the line will start
    (width, height)= f.getsize(cluster[0])
    temp.append(( cluster[0], cluster[1] + width, cluster[2] + (height/2) ))
    if maxWordLength < width:
        maxWordLength= width
allClusters= temp
xConcernRulerStartPoint= maxWordLength + xOffsetWordToLine + xOffsetLineToRuler
#now reset all the x to the max word length + an offset
temp= []
for cluster in allClusters:
    newX= xOffsetWordToLine + cluster[1] + (maxWordLength - cluster[1] - 10) + xOffsetLineToRuler
    draw.line([(cluster[1] + xOffsetWordToLine, cluster[2]), ( newX , cluster[2])], fill=(255,0,0))
    temp.append((cluster[0], newX, cluster[2]))
allClusters= temp;
#now lets draw the ruler
temp= int(min(concernClusterSimilarity))
if 100 > temp >= 90:
    temp= 1
elif 90 > temp >= 80:
    temp= 2
elif 80 > temp >= 70:
    temp= 3
elif 70 > temp >= 60:
    temp= 4
elif 60 > temp >= 50:
    temp= 5
elif 50 > temp >= 40:
    temp= 6
elif 40 > temp >= 30:
    temp= 7
elif 30 > temp >= 20:
    temp= 8
elif 20 > temp >= 10:
    temp= 9
elif 10 > temp >= 0:
    temp= 10
concernRulerLength= temp * concernRulerStep
#draw the entire ruler
draw.line( [(xConcernRulerStartPoint, 5), (xConcernRulerStartPoint + concernRulerLength, 5)], fill=(255,0,0))
i= 0
#draw the markers of the ruler
while i <= temp:
    draw.line( [ (xConcernRulerStartPoint + (concernRulerStep * i) , 5), ( (xConcernRulerStartPoint + (concernRulerStep * i)), 5 + rulerVerticalLineSize) ], fill=(255,0,0))
    i+= 1

#ok now lets start drawing the combined clustersConcern
i= 0
xPositionNewCluster= 0; # the xPosition of a new cluster will be fix and based on the previous run
while i < len(clustersConcern):
    cluster= clustersConcern[i]
    mainClusterSet= set(cluster[0])
    subSetClusters= []
    j= 0
    #find from which sub-clustersConcern is the main cluster composed of
    while j < len(allClusters):
        temp= (allClusters[j])[0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
        if type(temp) is str:
            temp= [temp]
        if set(temp).issubset(mainClusterSet):
            subSetClusters.append(allClusters[j])
            if(len(subSetClusters) >= len(cluster[0])):
                break;
        j+= 1;
    #now draw the lines of the old clustersConcern to the new cluster
    #assumption, because we created the initial clustersConcern from the last cluster(where we have all the clustersConcern in 1) the position of the sub-clustersConcern are ideal, in terms that they are next to each other after each round
    #xPositionNewCluster= 0
    yPositionNewCluster= 0
    temp=  0 #will be used as the biggest y
    temp2= 0 #will be used as the smallest y
    j= 0
    while j < len(subSetClusters):
        if j == 0:
            temp= (subSetClusters[j])[2]
            temp2= (subSetClusters[j])[2]
            if i == 0:
                xPositionNewCluster= (subSetClusters[j])[1]
            #xPositionNewCluster= (subSetClusters[j])[1]
        else:
            if (subSetClusters[j])[2] > temp:
                temp= (subSetClusters[j])[2]
            if (subSetClusters[j])[2] < temp2:
                temp2= (subSetClusters[j])[1]
            #if (subSetClusters[j])[1] > xPositionNewCluster:
            #    xPositionNewCluster= (subSetClusters[j])[1]
        j+= 1
    #calculate the offset from the beginning of the ruler that xPositionNewCluster should be
    #assumption, ruler starts from 100 thus: |100 |90 |80......
    # concernRulerStep/10 -> every step = 10% thus this calculation give us the amount of pixels that 1% represents. 100 - concernClusterSimilarity[i] -> this calculation gives us the percentage that a percentage is away from 100%.
    xPositionNewCluster= ( (concernRulerStep/10) * ( 100 - concernClusterSimilarity[i]) ) + xConcernRulerStartPoint
    yPositionNewCluster= temp2 + (temp - temp2)/2

    for subCluser in subSetClusters:
        draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, yPositionNewCluster)], fill=(255,0,0))
        #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255,0,0))
        #draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255,0,0))

        # now remove the old clustersConcern from allClusters
        allClusters.remove(subCluser)
    #now add the new cluster to allClusters
    allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
    i+= 1
"""

#prototype function that will be used to create an image using xml      
def drawDendogram3(clustersConcern=[], clustersAlternative=[], matrix=[[]], maxMatrixCellValue=1):
    # from RGT.gridMng.utility import createColorRGBString

    #cluster format is: [([element1, elemet2], distance), ([element1, elemet2, element3], distance), ......]

    #########################
    ########Important########
    #########################
    #Svg In SVG, text is positioned (unlike the <rect> element) with its lower left corner
    #at the coordinates specified in the x and y attributes.
    #Because all of the code was originaly create as to make a png ping and later on we switched to
    #svg the text y should be + height of the text - 4 as this provides the best results of aligment


    #########################
    ###changeable settings###
    #########################

    #f= ImageFont.truetype("arial.ttf", 15)

    fontSize = 15;
    try:
        f = ImageFont.truetype(DENDROGRAM_FONT_LOCATION, fontSize) #
    except:
        print("wtf")

    fontName = 'arial'  #this variable is used by the client to know which font it should use when creating the picture
    useShadow = True

    ###shadow settings###
    shadowXOffset = 3 #value in pixels
    shadowYOffset = 3 #value in pixels
    shadowBlurSize = 4 #how big the bluer should be

    ###table settings###
    xWordTableOffset = 10 #value in pixel, offset of the longest word of the left side of the table in relation to the left of the picture
    xWordToTableOffset = 5 #value in pixel, offset of a word (left or right) to the table, example: word1 <--xWordToTableOffset--> |table| <--xWordToTableOffset--> word2
    yTableTopOffset = 10
    ###color settings###
    tableLineColor = (60, 179, 113) #value in rbg
    tableWordColor = (70, 130, 180) #value in rbg
    tableCellWordColor = (60, 179, 113) #value in rbg
    tableToAlternativesConnectionLineColor = (188, 143, 143) #value in rbg

    ###dendogram settings###

    ###color settings###
    concernDendogramLineColor = (255, 0, 0) #value in rbg
    alternativeDendogramLineColor = (255, 0, 0) #value in rbg
    ###ruler settings###
    baseRulerStep = 25 #base amount of pixels between every 10 steps of the rule example: |10 |20 |30.....|100 = |10 <--25pixels--> |20 <--25pixels--> |30 ......
    xOffsetLineToRuler = 20 # amount in pixels, this amount is used set the X start position that the ruler starts example : concern1 <-xOffsetWordToLine-> <---xOffsetLineToRuler---> |100  |90  |80....
    xOffsetWordToLine = 5 # amount in pixel, offset of where to start drawing the initial line from the word example : concern1 <-xOffsetWordToLine-> <---xOffsetLineToRuler---> |100  |90  |80....
    rulerVerticalLineSize = 5 #value in pixel
    rulerStepIncrease = 20 #value in pixel, this value is used with the number of initial clusters in a dendogram to calculate the final size of each rule step, equation is (nInitialClusters * rulerStepIncrease) + baseRulerStep
    ###specific settings###
    yConcernRulerOffset = 10 #value in pixel, offset from the ceiling of the picture to the top of the percentage numbers
    yAlternativeRulerOffset = 10 #value in pixel, off from the bottom of the table to the top of the percentage numbers
    yConcerPercentageToRulerOffset = 3 #value in pixel, distance between the percentage number and the ruler
    yAlternativePercentageToRulerOffset = 3 #value in pixel, distance between the percentage number and the ruler
    ###color settings###
    concernRulerColor = (255, 0, 0) #value in rbg
    concernRulerPerncetageColor = (255, 0, 0)# value in rbg
    alternativeRulerColor = (255, 0, 0) #value in rbg
    alternativeRulerPerncetageColor = (255, 0, 0)# value in rbg
    alternativeWordColor = (244, 164, 96) #value in rbg

    ###########################
    ###unchangeable settings###
    ###########################

    tableLineThickness = 1 #do not change this value

    ######################
    ###global variables###
    ######################

    concernClusterSimilarity = []
    alternativeClusterSimilarity = []
    dicMatrixConcernToWordEndPosition = {} #this is use to map words in the table that was drawn to where the last pixel is of the left, we need this to map the words of the concern dendogram
    cellAlternativesXPositions = {} #middle position of the cell that corresponds to the given alternative
    percentageWordSize = f.getsize(str(100))
    #impl= getDOMImplementation()
    impl = SvgDOMImplementation()
    #xmlDoc= impl.createDocument(None, "gridVisualization", None)
    xmlDoc = impl.createSvgDocument()
    #topElement= xmlDoc.documentElement
    root = xmlDoc.documentElement

    ###table variables###
    ###word variables###
    leftConcernMaxWordWidth = -1
    rightConcernMaxWordWidth = -1
    leftConcernMaxWordHeight = -1
    rightConcernMaxWordHeight = -1
    rightConcenrMaxX = -1
    alternativeMaxWordWidth = -1
    alternativeMaxWordHeight = -1
    ###cells variables###
    tableCellWidth = -1
    tableCellHeight = -1 #@UnusedVariable
    yTableBottom = -1 #@UnusedVariable
    ###ruler variables###
    xConcernRulerStartPoint = -1 #@UnusedVariable
    xAlternativeRulerStartPoint = -1 #@UnusedVariable
    concernRulerLength = -1 #@UnusedVariable
    alternativeRulerLength = -1 #@UnusedVariable
    nConcernRulerSteps = -1 #@UnusedVariable
    nAlternativRulerSteps = -1 #@UnusedVariable

    ##xml variables##
    shadowFilterId = "shadow1"

    ################
    #pre-processing#
    ################

    #print alternativeClusterSimilarity

    #find the min similarity of the concern
    for cluster in clustersConcern:
        #print cluster
        if cluster[1] != 0:
            concernClusterSimilarity.append(100 * (1 - (cluster[1] / ((len(matrix) - 1) * (maxMatrixCellValue - 1)))))
        else:
            concernClusterSimilarity.append(100)

    #print concernClusterSimilarity
    #find the min similarity of the alternatives
    for cluster in clustersAlternative:
        if cluster[1] != 0:
            alternativeClusterSimilarity.append(
                100 * (1 - (cluster[1] / ((len(matrix[0]) - 2) * (maxMatrixCellValue - 1)))))
        else:
            alternativeClusterSimilarity.append(100)




    #calculate the ruler step size
    concernRulerStep = (len(clustersConcern) * rulerStepIncrease) + baseRulerStep
    alternativeRulerStep = (len(clustersAlternative) * rulerStepIncrease) + baseRulerStep

    #find the max word width of the left and right side of the table and the size of the cells
    for row in matrix:
        #maxValue= max(row[1: len(row)-1])
        #the first row is special as it only contains the names of the alternatives, thus skip it
        if type(row[1]) != str:
            i = 1
            while i < len(row) - 2:
                col = row[i]
                (tempCellWidth, tempCellHeight) = f.getsize(str(col))
                if tableCellWidth < tempCellWidth:
                    tableCellWidth = tempCellWidth
                if tableCellHeight < tempCellHeight:
                    tableCellHeight = tempCellHeight
                i += 1
            size = f.getsize(row[0])
            if size[0] > leftConcernMaxWordWidth:
                leftConcernMaxWordWidth = size[0]
            if size[1] > leftConcernMaxWordHeight:
                leftConcernMaxWordHeight = size[1]
            size = f.getsize(row[len(row) - 1])
            if size[0] > rightConcernMaxWordWidth:
                rightConcernMaxWordWidth = size[0]
            if size[1] > rightConcernMaxWordHeight:
                rightConcernMaxWordHeight = size[1]

    #(tableCellWidth, tableCellHeight)= f.getsize(str(tableCellWidth))
    #the height of the cell should be a little bigger then the max word height
    if rightConcernMaxWordHeight > leftConcernMaxWordHeight:
        if rightConcernMaxWordHeight > tableCellHeight:
            tableCellHeight = rightConcernMaxWordHeight
    else:
        if leftConcernMaxWordHeight > tableCellHeight:
            tableCellHeight = leftConcernMaxWordHeight
    tableCellWidth += 4
    tableCellHeight += 4

    for word in matrix[0]:
        if type(word) == str:
            temp = f.getsize(word)
            if temp[1] > alternativeMaxWordHeight:
                alternativeMaxWordHeight = temp[1]


                #####--->>>>       #TODO calculate the max height of a word

    #determine the number of steps the concern ruler has
    temp = int(min(concernClusterSimilarity))
    if 100 >= temp >= 90:
        temp = 1
    elif 90 > temp >= 80:
        temp = 2
    elif 80 > temp >= 70:
        temp = 3
    elif 70 > temp >= 60:
        temp = 4
    elif 60 > temp >= 50:
        temp = 5
    elif 50 > temp >= 40:
        temp = 6
    elif 40 > temp >= 30:
        temp = 7
    elif 30 > temp >= 20:
        temp = 8
    elif 20 > temp >= 10:
        temp = 9
    elif 10 > temp >= 0:
        temp = 10
    concernRulerLength = temp * concernRulerStep
    nConcernRulerSteps = temp

    #determine the number of steps the alternative ruler has
    temp = int(min(alternativeClusterSimilarity))
    if 100 >= temp >= 90:
        temp = 1
    elif 90 > temp >= 80:
        temp = 2
    elif 80 > temp >= 70:
        temp = 3
    elif 70 > temp >= 60:
        temp = 4
    elif 60 > temp >= 50:
        temp = 5
    elif 50 > temp >= 40:
        temp = 6
    elif 40 > temp >= 30:
        temp = 7
    elif 30 > temp >= 20:
        temp = 8
    elif 20 > temp >= 10:
        temp = 9
    elif 10 > temp >= 0:
        temp = 10
    alternativeRulerLength = temp * alternativeRulerStep
    nAlternativRulerSteps = temp

    #find the max width of the words in the alternative dendogram
    for word in matrix[0]:
        #again the first row is special so skip it
        if word != []:
            size = f.getsize(word)
            if size[0] > alternativeMaxWordWidth:
                alternativeMaxWordWidth = size[0]

    #determine the width and height of the picture
    h = yTableTopOffset + (tableCellHeight * len(matrix)) + yAlternativeRulerOffset + (
        (len(matrix[0]) - 2) * tableCellHeight) + (alternativeMaxWordHeight * (len(matrix[0]) - 2)) + \
        percentageWordSize[1] + yConcernRulerOffset + 10


    w = xWordTableOffset + (xWordToTableOffset * 2) + (
        (len(matrix[0]) - 2) * tableCellWidth) + leftConcernMaxWordWidth + percentageWordSize[0]
    if rightConcernMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + concernRulerLength > alternativeMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + alternativeRulerLength:
        w += rightConcernMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + concernRulerLength
    else:
        w += alternativeMaxWordWidth + xOffsetWordToLine + xOffsetLineToRuler + alternativeRulerLength

        #create new matrix based on the order of the concern and alternative clusters
    tempMatrix = [None] * len(matrix)
    concernIndexToName = {}
    alternativeIndexToName = {}
    concernNameToIndex = {}
    alternativeNameToIndex = {}
    i = 1
    firstRow = [[]]

    #create the map of the old matrix to the new matrix
    while i < len(matrix):
        concernIndexToName[i] = (matrix[i][0], matrix[i][len(matrix[0]) - 1])
        i += 1
    i = 1
    while i < (len(matrix[0]) - 1):
        alternativeIndexToName[i] = matrix[0][i]
        i += 1

    i = 0
    temp = clustersConcern[len(clustersConcern) - 1][0]
    while i < len(temp):
        concernNameToIndex[temp[i]] = i + 1
        i += 1
    i = 0
    temp = clustersAlternative[len(clustersAlternative) - 1][0]
    nCol = len(clustersAlternative[len(clustersAlternative) - 1][0])
    while i < len(temp):
        alternativeNameToIndex[temp[
            i]] = nCol - i #nCol - i is to invert the position of the alternative so the line that we will draw from the table to the alternative names will look good, also the result of the equation is the index for the new table, no correction is needed as the values of the alternatives start at index 1
        firstRow.append(temp[i])
        i += 1
    firstRow.append([])
    i = 1
    j = 1

    #create the new matrix
    while i < len(matrix):
        tempRow = [None] * len(matrix[0])
        while j < len(matrix[0]) - 1:
            index = alternativeNameToIndex[alternativeIndexToName[j]]
            tempRow.insert(index, matrix[i][j])
            tempRow.pop(index + 1)
            if i == 1:
                cellAlternativesXPositions[alternativeIndexToName[j]] = ((index - 1) * tableCellWidth) + (
                    tableCellWidth / 2) + xWordTableOffset + xWordToTableOffset + leftConcernMaxWordWidth
            j += 1
        tempRow.insert(0, matrix[i][0])
        tempRow.pop(1)
        tempCalculcation = len(matrix[i]) - 1
        tempRow.insert(tempCalculcation, matrix[i][tempCalculcation])
        tempRow.pop(tempCalculcation + 1)
        temp = concernIndexToName[i]
        index = -1
        if concernNameToIndex.has_key(temp[0]):
            index = concernNameToIndex[temp[0]]
        else:
            index = concernNameToIndex[temp[1]]
        tempMatrix.insert(index, tempRow)
        tempMatrix.pop(index + 1)
        i += 1
        j = 1
    tempMatrix.insert(0, firstRow)
    tempMatrix.pop(1)
    #print tempMatrix
    matrix = tempMatrix

    #######end pre-processing #########

    #depth= len(clustersConcern)
    #scaling= float(w - 150)/depth

    #set the svg image size
    root.setWidth(str(w) + 'px')
    root.setHeight(str(h) + 'px')
    root.setXmlns('http://www.w3.org/2000/svg')
    root.setVersion('1.1')
    #root.setViewBox('0 0 ' + str(w) + ' ' + str(h))

    #add shadow
    if useShadow:
        defNode = xmlDoc.createDefsNode()
        filterNode = xmlDoc.createFilterNode()
        filterNode.setId(shadowFilterId)
        filterNode.setX(0)
        filterNode.setY(0)
        filterNode.setWidth('150%')
        filterNode.setHeight('150%')
        tempNode = xmlDoc.createFeOffsetNode()
        tempNode.setDx(shadowXOffset)
        tempNode.setDy(shadowYOffset)
        tempNode.setResult('offOut')
        tempNode.setIn('SourceGraphic')
        filterNode.appendChild(tempNode)
        tempNode = xmlDoc.createFeGaussianBlurNode()
        tempNode.setResult('blurOut')
        tempNode.setIn('offOut')
        tempNode.setStdDeviation(shadowBlurSize)
        filterNode.appendChild(tempNode)
        tempNode = xmlDoc.createFeBlendNode()
        tempNode.setIn('SourceGraphic')
        tempNode.setIn2('blurOut')
        tempNode.setMode('normal')
        filterNode.appendChild(tempNode)
        defNode.appendChild(filterNode)
        root.appendChild(defNode)

    #        # define the global properties of the image
    #        propertiesNode= xmlDoc.createElement('properties')
    #        #image width
    #        tempNode= xmlDoc.createElement('width');
    #        tempNode.appendChild(xmlDoc.createTextNode(str(w)))
    #        propertiesNode.appendChild(tempNode)
    #        #image height
    #        tempNode= xmlDoc.createElement('height')
    #        tempNode.appendChild(xmlDoc.createTextNode(str(h)))
    #        propertiesNode.appendChild(tempNode)
    #        #global shadow
    #        if useGlobalShadow:
    #            shadowNode= xmlDoc.createElement('shadow')
    #            shadowXOffSetNode= xmlDoc.createElement('xOffSet')
    #            shadowYOffSetNode= xmlDoc.createElement('yOffSet')
    #            shadowBlurSizeNode= xmlDoc.createElement('blurSize')
    #
    #            shadowXOffSetNode.appendChild(xmlDoc.createTextNode(str(shadowXOffset)))
    #            shadowYOffSetNode.appendChild(xmlDoc.createTextNode(str(shadowYOffset)))
    #            shadowBlurSizeNode.appendChild(xmlDoc.createTextNode(str(shadowBlurSize)))
    #
    #            shadowNode.appendChild(shadowXOffSetNode)
    #            shadowNode.appendChild(shadowYOffSetNode)
    #            shadowNode.appendChild(shadowBlurSizeNode)
    #
    #            propertiesNode.appendChild(shadowNode)
    #
    #        topElement.appendChild(propertiesNode)


    #define the main node for the table
    #tableGroupNode= xmlDoc.createElement('dendogramTable')
    tableGroupNode = xmlDoc.createGNode()
    if useShadow:
        tableGroupNode.setFilter('url(#' + shadowFilterId + ')')
    tempNode = None
    #lets draw stuff now

    ################
    ###table draw###
    ################

    yTableStartPosition = yTableTopOffset + percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset
    xtableStartPosition = xWordToTableOffset + xWordTableOffset + leftConcernMaxWordWidth
    #tableGroupNode.appendChild(__createXmlLineNode__(xmlDoc, xtableStartPosition, yTableStartPosition, xtableStartPosition + ( tableCellWidth * (len(matrix[0]) - 2)), yTableStartPosition, tableLineColor, tableLineThickness))
    tempNode = xmlDoc.createLineNode(xtableStartPosition, yTableStartPosition,
                                     xtableStartPosition + ( tableCellWidth * (len(matrix[0]) - 2)),
                                     yTableStartPosition)
    tempNode.setStyle('stroke:' + createColorRGBString(tableLineColor))
    tempNode.setStrokeWidth(tableLineThickness)
    tableGroupNode.appendChild(tempNode)
    #draw.line([(xtableStartPosition, yTableStartPosition), (xtableStartPosition + ( tableCellWidth * (len(matrix[0]) - 2)), yTableStartPosition)], fill= tableLineColor, width= tableLineThickness)
    #remember to add + tableLineThickness to the start position to account for the line thickness, that also goes for the right, left and bottom

    #now lets drawn the table row by row
    i = 1;
    j = 0;
    while i < len(matrix):
        row = matrix[i]
        #draw the left word
        wordSize = f.getsize(row[0])
        tempNode = xmlDoc.createSvgTextNode(xtableStartPosition - xWordToTableOffset - wordSize[0], (
                                                                                                        yTableStartPosition + (
                                                                                                            tableCellHeight * (
                                                                                                                i - 1)) - (
                                                                                                            wordSize[
                                                                                                                1] / 2) + (
                                                                                                            tableCellHeight / 2)) + (
                                                                                                        wordSize[
                                                                                                            1] - 4),
                                            row[0])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(fontSize) + 'px')
        tempNode.setStyle('fill:' + createColorRGBString(tableWordColor))
        tableGroupNode.appendChild(tempNode)
        #tableGroupNode.appendChild(__createXmlTextNode__(xmlDoc, xtableStartPosition - xWordToTableOffset - wordSize[0], yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight/2), row[0], wordSize[0], wordSize[1], fontName, fontSize, tableWordColor))
        #draw.text((xtableStartPosition - xWordToTableOffset - wordSize[0], yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight/2) ), row[0], font= f, fill= tableWordColor)
        while j < len(row) - 2:
            if j == 0:
                #draw the left line
                tempNode = xmlDoc.createLineNode(xtableStartPosition,
                                                 yTableStartPosition + ( (i - 1) * tableCellHeight),
                                                 xtableStartPosition, yTableStartPosition + ( i * tableCellHeight))
                tempNode.setStrokeWidth(tableLineThickness)
                tempNode.setStyle('stroke:' + createColorRGBString(tableLineColor))
                tableGroupNode.appendChild(tempNode)
                #tableGroupNode.appendChild(__createXmlLineNode__(xmlDoc, xtableStartPosition, yTableStartPosition + ( (i - 1) * tableCellHeight), xtableStartPosition, yTableStartPosition + ( i * tableCellHeight), tableLineColor, tableLineThickness))
                #draw.line([(xtableStartPosition , yTableStartPosition + ( (i - 1) * tableCellHeight)), ( xtableStartPosition, yTableStartPosition + ( i * tableCellHeight) )], fill= tableLineColor, width= tableLineThickness)
            #draw the values of the cells
            cell = row[j + 1]
            wordSize = f.getsize(str(cell))
            xCellValue = xtableStartPosition + (j * tableCellWidth) + floor((tableCellWidth - wordSize[0]) / 2)
            yCellValue = yTableStartPosition + ((i - 1) * tableCellHeight) + floor((tableCellHeight - wordSize[1]) / 2)
            tempNode = xmlDoc.createSvgTextNode(xCellValue, yCellValue + (wordSize[1] - 4), str(cell))
            tempNode.setFontFamily(fontName)
            tempNode.setFontSize(str(fontSize) + 'px')
            tempNode.setStyle('fill:' + createColorRGBString(tableCellWordColor))
            tableGroupNode.appendChild(tempNode)
            #tableGroupNode.appendChild(__createXmlTextNode__(xmlDoc, xCellValue, yCellValue, str(cell), wordSize[0], wordSize[1], fontName, fontSize, tableCellWordColor))
            #draw.text((xCellValue, yCellValue), str(cell), font= f, fill= tableCellWordColor)
            if j == len(row) - 3:
                #draw right line
                tempNode = xmlDoc.createLineNode(xtableStartPosition + ( (j + 1) * tableCellWidth),
                                                 yTableStartPosition + ( (i - 1) * tableCellHeight),
                                                 xtableStartPosition + ( (j + 1) * tableCellWidth),
                                                 yTableStartPosition + (i * tableCellHeight))
                tempNode.setStrokeWidth(tableLineThickness)
                tempNode.setStyle('stroke:' + createColorRGBString(tableLineColor))
                tableGroupNode.appendChild(tempNode)
                #tableGroupNode.appendChild(__createXmlLineNode__(xmlDoc, xtableStartPosition + ( (j + 1) * tableCellWidth), yTableStartPosition + ( (i - 1) * tableCellHeight), xtableStartPosition + ( (j + 1) * tableCellWidth), yTableStartPosition + (i * tableCellHeight), tableLineColor, tableLineThickness))
                #draw.line([(xtableStartPosition + ( (j + 1) * tableCellWidth), yTableStartPosition + ( (i - 1) * tableCellHeight)), ( xtableStartPosition + ( (j + 1) * tableCellWidth), yTableStartPosition + (i * tableCellHeight) )], fill= tableLineColor, width= tableLineThickness)
            j += 1
            #draw the right word
        wordSize = f.getsize(row[len(row) - 1])
        tempNode = xmlDoc.createSvgTextNode(
            xtableStartPosition + (tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness,
            (yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight / 2)) + (
                wordSize[1] - 4), row[len(row) - 1])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(fontSize) + 'px')
        tempNode.setStyle('fill:' + createColorRGBString(tableWordColor))
        tableGroupNode.appendChild(tempNode)
        #tableGroupNode.appendChild(__createXmlTextNode__(xmlDoc, xtableStartPosition + (tableCellWidth * (len(row) - 2)) +  xWordToTableOffset + tableLineThickness, yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight/2), row[len(row) - 1], wordSize[0], wordSize[1], fontName, fontSize, tableWordColor))
        #draw.text( ( xtableStartPosition + (tableCellWidth * (len(row) - 2)) +  xWordToTableOffset + tableLineThickness, yTableStartPosition + (tableCellHeight * (i - 1)) - (wordSize[1] / 2) + (tableCellHeight/2) ), row[len(row) - 1], font= f, fill= tableWordColor)
        dicMatrixConcernToWordEndPosition[row[0]] = (
            wordSize[0] + xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness,
            yTableStartPosition + (tableCellHeight * (i - 1)) + (wordSize[1] / 2) )
        dicMatrixConcernToWordEndPosition[row[len(row) - 1]] = dicMatrixConcernToWordEndPosition[row[0]]
        if rightConcenrMaxX < xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness + rightConcernMaxWordWidth:
            rightConcenrMaxX = xtableStartPosition + (
                tableCellWidth * (len(row) - 2)) + xWordToTableOffset + tableLineThickness + rightConcernMaxWordWidth
        j = 0
        i += 1
        #draw the bottom line
    yTableBottom = yTableStartPosition + (tableCellHeight * (len(matrix) - 1) )
    tempNode = xmlDoc.createLineNode(xtableStartPosition, yTableBottom,
                                     xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ), yTableBottom)
    tempNode.setStrokeWidth(tableLineThickness)
    tempNode.setStyle('stroke:' + createColorRGBString(tableLineColor))
    tableGroupNode.appendChild(tempNode)
    #tableGroupNode.appendChild(__createXmlLineNode__(xmlDoc, xtableStartPosition, yTableBottom, xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ), yTableBottom, tableLineColor, tableLineThickness))
    #draw.line([(xtableStartPosition, yTableBottom ), (xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ) , yTableBottom )], fill= tableLineColor, width= tableLineThickness)

    #topElement.appendChild(tableGroupNode)
    root.appendChild(tableGroupNode)

    ####### end table draw #########

    ############################
    ###Concern dendogram draw###
    ############################

    #dendogramConcernsGroup= xmlDoc.createElement('dendogramConcerns')
    dendogramConcernsGroup = xmlDoc.createGNode()
    if useShadow:
        dendogramConcernsGroup.setFilter('url(#' + shadowFilterId + ')')

    #lets first draw all the individual items, the last sub-cluster should contain all of them
    allClusters = [] # format is ([item1, item2,...], positionX, positionY)
    i = 0;
    while i < len(clustersConcern[len(clustersConcern) - 1][0]):
        temp = clustersConcern[len(clustersConcern) - 1][0]
        wordEndPosition = dicMatrixConcernToWordEndPosition[temp[i]]
        #save the positions we want
        allClusters.append((temp[i], wordEndPosition[0], wordEndPosition[1]))
        i += 1

    xConcernRulerStartPoint = rightConcenrMaxX + xOffsetWordToLine + xOffsetLineToRuler
    #now reset all the x to the max word length + an offset
    temp = []
    for cluster in allClusters:
        newX = xConcernRulerStartPoint #xOffsetWordToLine + cluster[1] + (rightConcenrMaxX - cluster[1]) + xOffsetLineToRuler
        tempNode = xmlDoc.createLineNode(cluster[1] + xOffsetWordToLine, cluster[2], newX, cluster[2])
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(concernDendogramLineColor))
        dendogramConcernsGroup.appendChild(tempNode)
        #dendogramConcernsGroup.appendChild(__createXmlLineNode__(xmlDoc, cluster[1] + xOffsetWordToLine, cluster[2], newX, cluster[2], concernDendogramLineColor, 1))
        #draw.line([(cluster[1] + xOffsetWordToLine, cluster[2]), ( newX , cluster[2])], fill= concernDendogramLineColor)
        temp.append((cluster[0], newX, cluster[2]))
    allClusters = temp;
    #now lets draw the ruler
    tempNode = xmlDoc.createLineNode(xConcernRulerStartPoint,
                                     percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset,
                                     xConcernRulerStartPoint + concernRulerLength,
                                     percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset)
    tempNode.setStrokeWidth(1)
    tempNode.setStyle('stroke:' + createColorRGBString(concernDendogramLineColor))
    dendogramConcernsGroup.appendChild(tempNode)
    #dendogramConcernsGroup.appendChild(__createXmlLineNode__(xmlDoc, xConcernRulerStartPoint, percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset, xConcernRulerStartPoint + concernRulerLength, percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset, concernRulerColor, 1))
    #draw.line( [(xConcernRulerStartPoint, percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset), (xConcernRulerStartPoint + concernRulerLength, percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset)], fill= concernRulerColor)
    i = 0
    #draw the markers of the ruler
    while i <= nConcernRulerSteps:
        percentage = str(100 - (i * 10))
        wordSize = f.getsize(percentage)
        tempNode = xmlDoc.createSvgTextNode(xConcernRulerStartPoint + (concernRulerStep * i) - (wordSize[0] / 2),
                                            yConcernRulerOffset + (wordSize[1] - 4), percentage)
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(fontSize) + 'px')
        tempNode.setStyle('fill:' + createColorRGBString(concernRulerPerncetageColor))
        dendogramConcernsGroup.appendChild(tempNode)
        #dendogramConcernsGroup.appendChild(__createXmlTextNode__(xmlDoc, xConcernRulerStartPoint + (concernRulerStep * i) -  (wordSize[0] / 2), yConcernRulerOffset, percentage, wordSize[0], wordSize[1], fontName, fontSize, concernRulerPerncetageColor))
        #draw.text(( xConcernRulerStartPoint + (concernRulerStep * i) -  (f.getsize(percentage)[0] / 2) , yConcernRulerOffset ), text= percentage, fill= concernRulerPerncetageColor, font= f)
        tempNode = xmlDoc.createLineNode(xConcernRulerStartPoint + (concernRulerStep * i),
                                         percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset,
                                         xConcernRulerStartPoint + (concernRulerStep * i), percentageWordSize[
                                                                                               1] + yConcernRulerOffset + yConcerPercentageToRulerOffset + rulerVerticalLineSize)
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(concernRulerColor))
        dendogramConcernsGroup.appendChild(tempNode)
        #dendogramConcernsGroup.appendChild(__createXmlLineNode__(xmlDoc, xConcernRulerStartPoint + (concernRulerStep * i), percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset, xConcernRulerStartPoint + (concernRulerStep * i), percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset + rulerVerticalLineSize, concernRulerColor, 1))
        #draw.line( [ (xConcernRulerStartPoint + (concernRulerStep * i) , percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset), ( (xConcernRulerStartPoint + (concernRulerStep * i)), percentageWordSize[1] + yConcernRulerOffset + yConcerPercentageToRulerOffset + rulerVerticalLineSize) ], fill= concernRulerColor)
        i += 1

    #ok now lets start drawing the combined clustersConcern
    i = 0
    xPositionNewCluster = 0; # the xPosition of a new cluster will be fix and based on the previous run
    while i < len(clustersConcern):
        cluster = clustersConcern[i]
        mainClusterSet = set(cluster[0])
        subSetClusters = []
        j = 0
        #find from which sub-clustersConcern is the main cluster composed of
        while j < len(allClusters):
            temp = (allClusters[j])[
                0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
            if type(temp) is str:
                temp = [temp]
            if set(temp).issubset(mainClusterSet):
                subSetClusters.append(allClusters[j])
                if (len(subSetClusters) >= len(cluster[0])):
                    break;
            j += 1;
            #now draw the lines of the old clustersConcern to the new cluster
        #assumption, because we created the initial clustersConcern from the last cluster(where we have all the clustersConcern in 1) the position of the sub-clustersConcern are ideal, in terms that they are next to each other after each round
        #xPositionNewCluster= 0
        yPositionNewCluster = 0
        temp = 0 #will be used as the biggest y
        temp2 = 0 #will be used as the smallest y
        j = 0
        while j < len(subSetClusters):
            if j == 0:
                temp = (subSetClusters[j])[2]
                temp2 = (subSetClusters[j])[2]
                if i == 0:
                    xPositionNewCluster = (subSetClusters[j])[1]
                    #xPositionNewCluster= (subSetClusters[j])[1]
            else:
                if (subSetClusters[j])[2] > temp:
                    temp = (subSetClusters[j])[2]
                if (subSetClusters[j])[2] < temp2:
                    temp2 = (subSetClusters[j])[2]
                    #if (subSetClusters[j])[1] > xPositionNewCluster:
                    #    xPositionNewCluster= (subSetClusters[j])[1]
            j += 1
            #calculate the offset from the beginning of the ruler that xPositionNewCluster should be
        #assumption, ruler starts from 100 thus: |100 |90 |80......
        # concernRulerStep/10 -> every step = 10% thus this calculation give us the amount of pixels that 1% represents. 100 - concernClusterSimilarity[i] -> this calculation gives us the percentage that a percentage is away from 100%.
        xPositionNewCluster = int(
            ( (concernRulerStep / 10.0) * ( 100 - concernClusterSimilarity[i]) ) + xConcernRulerStartPoint)
        yPositionNewCluster = temp2 + (temp - temp2) / 2

        for subCluser in subSetClusters:
            tempNode = xmlDoc.createLineNode(subCluser[1], subCluser[2], xPositionNewCluster, yPositionNewCluster)
            tempNode.setStrokeWidth(1)
            tempNode.setStyle('stroke:' + createColorRGBString(concernDendogramLineColor))
            dendogramConcernsGroup.appendChild(tempNode)
            #dendogramConcernsGroup.appendChild(__createXmlLineNode__(xmlDoc, subCluser[1], subCluser[2], xPositionNewCluster, yPositionNewCluster, concernDendogramLineColor, 1))
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, yPositionNewCluster)], fill= concernDendogramLineColor)
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255,0,0))
            #draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255,0,0))

            # now remove the old clustersConcern from allClusters
            allClusters.remove(subCluser)
            #now add the new cluster to allClusters
        allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
        i += 1
        #topElement.appendChild(dendogramConcernsGroup)
    root.appendChild(dendogramConcernsGroup)
    ####### end concern dendogram draw #########

    ################################
    ###Alternative dendogram draw###
    ################################

    #dendogramAlternativesGroup= xmlDoc.createElement('dendogramAlternative')
    dendogramAlternativesGroup = xmlDoc.createGNode()
    if useShadow:
        dendogramAlternativesGroup.setFilter('url(#' + shadowFilterId + ')')

    allClusters = [] # format is ([item1, item2,...], positionX, positionY)
    i = 0;
    while i < len(clustersAlternative[len(clustersAlternative) - 1][0]):
        allClusters.append(((clustersAlternative[len(clustersAlternative) - 1][0])[i],
                            xtableStartPosition + (tableCellWidth * (len(matrix[0]) - 2) ) + xWordToTableOffset,
                            yTableStartPosition + (tableCellHeight * len(matrix)) + (
                                tableCellHeight * (i)) + yAlternativeRulerOffset + percentageWordSize[
                                1] + yAlternativePercentageToRulerOffset ))
        i += 1
        #now draw the initial clustersAlternative
    temp = []
    maxWordLength = -1
    for cluster in allClusters:
        (width, height) = f.getsize(cluster[0])
        tempNode = xmlDoc.createSvgTextNode(cluster[1], cluster[2] + (wordSize[1] - 4), cluster[0])
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(fontSize) + 'px')
        tempNode.setStyle('fill:' + createColorRGBString(alternativeWordColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlTextNode__(xmlDoc, cluster[1], cluster[2], cluster[0], width, height, fontName, fontSize, alternativeWordColor))
        #draw.text((cluster[1], cluster[2]), cluster[0], font= f, fill= alternativeWordColor );
        # now reset the y position to the middle of the word and the x to the end of the word, this is the point where the line will start
        temp.append(( cluster[0], cluster[1] + width, cluster[2] + (height / 2) ))
        if maxWordLength < width:
            maxWordLength = width
            #draw the lines that connect the table with the alternative names
        tempNode = xmlDoc.createLineNode(cellAlternativesXPositions[cluster[0]], yTableBottom + 1,
                                         cellAlternativesXPositions[cluster[0]], cluster[2] + (height / 2))
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(tableToAlternativesConnectionLineColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, cellAlternativesXPositions[cluster[0]], yTableBottom + 1, cellAlternativesXPositions[cluster[0]], cluster[2] + (height/2), tableToAlternativesConnectionLineColor, 1))
        #draw.line([(cellAlternativesXPositions[cluster[0]] , yTableBottom + 1), (cellAlternativesXPositions[cluster[0]], cluster[2] + (height/2))], fill= tableToAlternativesConnectionLineColor)
        tempNode = xmlDoc.createLineNode(cellAlternativesXPositions[cluster[0]], cluster[2] + (height / 2),
                                         cluster[1] - 2, cluster[2] + (height / 2))
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(tableToAlternativesConnectionLineColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, cellAlternativesXPositions[cluster[0]],  cluster[2] + (height/2), cluster[1] - 2,  cluster[2] + (height/2), tableToAlternativesConnectionLineColor, 1))
        #draw.line([(cellAlternativesXPositions[cluster[0]] , cluster[2] + (height/2)), (cluster[1] - 2, cluster[2] + (height/2))], fill= tableToAlternativesConnectionLineColor)
    allClusters = temp
    xAlternativeRulerStartPoint = maxWordLength + xOffsetWordToLine + xOffsetLineToRuler + xtableStartPosition + (
        tableCellWidth * (len(matrix[0]) - 2) )
    yAlternativeRulerStartPoint = yAlternativeRulerOffset + percentageWordSize[
        1] + yAlternativePercentageToRulerOffset + yTableBottom
    #now reset all the x to the max word length + an offset
    temp = []
    for cluster in allClusters:
        newX = xAlternativeRulerStartPoint
        tempNode = xmlDoc.createLineNode(cluster[1] + xOffsetWordToLine, cluster[2], newX, cluster[2])
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(alternativeDendogramLineColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, cluster[1] + xOffsetWordToLine, cluster[2], newX, cluster[2], alternativeDendogramLineColor, 1))
        #draw.line([(cluster[1] + xOffsetWordToLine, cluster[2]), ( newX , cluster[2])], fill= alternativeDendogramLineColor)
        temp.append((cluster[0], newX, cluster[2]))
    allClusters = temp;
    #now lets draw the ruler
    newX = xAlternativeRulerStartPoint
    tempNode = xmlDoc.createLineNode(xAlternativeRulerStartPoint, yAlternativeRulerStartPoint,
                                     xAlternativeRulerStartPoint + alternativeRulerLength, yAlternativeRulerStartPoint)
    tempNode.setStrokeWidth(1)
    tempNode.setStyle('stroke:' + createColorRGBString(alternativeRulerColor))
    dendogramAlternativesGroup.appendChild(tempNode)
    #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, xAlternativeRulerStartPoint, yAlternativeRulerStartPoint, xAlternativeRulerStartPoint + alternativeRulerLength, yAlternativeRulerStartPoint, alternativeRulerColor, 1))
    #draw.line( [(xAlternativeRulerStartPoint, yAlternativeRulerStartPoint), (xAlternativeRulerStartPoint + alternativeRulerLength, yAlternativeRulerStartPoint)], fill= alternativeRulerColor)
    i = 0
    #draw the markers of the ruler
    while i <= nAlternativRulerSteps:
        percentage = str(100 - (i * 10))
        wordSize = f.getsize(percentage)
        tempNode = xmlDoc.createSvgTextNode(
            xAlternativeRulerStartPoint + (alternativeRulerStep * i) - (wordSize[0] / 2),
            yAlternativeRulerStartPoint - yAlternativePercentageToRulerOffset - wordSize[1] + (wordSize[1] - 4),
            percentage)
        tempNode.setFontFamily(fontName)
        tempNode.setFontSize(str(fontSize) + 'px')
        tempNode.setStyle('fill:' + createColorRGBString(alternativeRulerPerncetageColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlTextNode__(xmlDoc, xAlternativeRulerStartPoint + (alternativeRulerStep * i) -  (wordSize[0] / 2), yAlternativeRulerStartPoint -  yAlternativePercentageToRulerOffset - wordSize[1], percentage, wordSize[0], wordSize[1], fontName, fontSize, alternativeRulerPerncetageColor))
        #draw.text(( xAlternativeRulerStartPoint + (alternativeRulerStep * i) -  (wordSize[0] / 2) , yAlternativeRulerStartPoint -  yAlternativePercentageToRulerOffset - wordSize[1]), text= percentage, fill= alternativeRulerPerncetageColor, font= f)
        tempNode = xmlDoc.createLineNode(xAlternativeRulerStartPoint + (alternativeRulerStep * i),
                                         yAlternativeRulerStartPoint,
                                         xAlternativeRulerStartPoint + (alternativeRulerStep * i),
                                         yAlternativeRulerStartPoint + rulerVerticalLineSize)
        tempNode.setStrokeWidth(1)
        tempNode.setStyle('stroke:' + createColorRGBString(alternativeRulerColor))
        dendogramAlternativesGroup.appendChild(tempNode)
        #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, xAlternativeRulerStartPoint + (alternativeRulerStep * i), yAlternativeRulerStartPoint, xAlternativeRulerStartPoint + (alternativeRulerStep * i), yAlternativeRulerStartPoint + rulerVerticalLineSize, alternativeRulerColor, 1))
        #draw.line( [ (xAlternativeRulerStartPoint + (alternativeRulerStep * i) , yAlternativeRulerStartPoint), ( (xAlternativeRulerStartPoint + (alternativeRulerStep * i)), yAlternativeRulerStartPoint + rulerVerticalLineSize) ], fill= alternativeRulerColor)
        i += 1

    #ok now lets start drawing the combined clustersAlternative
    i = 0
    xPositionNewCluster = 0; # the xPosition of a new cluster will be fixed and based on the previous run
    while i < len(clustersAlternative):
        cluster = clustersAlternative[i]
        mainClusterSet = set(cluster[0])
        subSetClusters = []
        j = 0
        #find from which sub-clustersConcern is the main cluster composed of
        while j < len(allClusters):
            temp = (allClusters[j])[
                0] #this is needed because if you have a long string like 'java' when you call set it will generate a set for each letter so the set will be (j,a,v,a) instead of (java)
            if type(temp) is str:
                temp = [temp]
            if set(temp).issubset(mainClusterSet):
                subSetClusters.append(allClusters[j])
                if (len(subSetClusters) >= len(cluster[0])):
                    break;
            j += 1;
            #now draw the lines of the old clustersAlternative to the new cluster
        #assumption, because we created the initial clustersAlternative from the last cluster(where we have all the clustersAlternative in 1) the position of the sub-clustersAlternative are ideal, in terms that they are next to each other after each round
        #xPositionNewCluster= 0
        yPositionNewCluster = 0
        temp = 0 #will be used as the biggest y
        temp2 = 0 #will be used as the smallest y
        j = 0
        while j < len(subSetClusters):
            if j == 0:
                temp = (subSetClusters[j])[2]
                temp2 = (subSetClusters[j])[2]
                if i == 0:
                    xPositionNewCluster = (subSetClusters[j])[1]
                    #xPositionNewCluster= (subSetClusters[j])[1]
            else:
                if (subSetClusters[j])[2] > temp:
                    temp = (subSetClusters[j])[2]
                if (subSetClusters[j])[2] < temp2:
                    temp2 = (subSetClusters[j])[2]
                    #if (subSetClusters[j])[1] > xPositionNewCluster:
                    #    xPositionNewCluster= (subSetClusters[j])[1]
            j += 1
            #calculate the offset from the beginning of the ruler that xPositionNewCluster should be
        #assumption, ruler starts from 100 thus: |100 |90 |80......
        # alternativeRulerStep/10 -> every step = 10% thus this calculation give us the amount of pixels that 1% represents. 100 - concernClusterSimilarity[i] -> this calculation gives us the percentage that a percentage is away from 100%.
        xPositionNewCluster = int(
            ( (alternativeRulerStep / 10.0) * ( 100 - alternativeClusterSimilarity[i]) ) + xAlternativeRulerStartPoint)
        yPositionNewCluster = temp2 + (temp - temp2) / 2

        for subCluser in subSetClusters:
            tempNode = xmlDoc.createLineNode(subCluser[1], subCluser[2], xPositionNewCluster, yPositionNewCluster)
            tempNode.setStrokeWidth(1)
            tempNode.setStyle('stroke:' + createColorRGBString(alternativeDendogramLineColor))
            dendogramAlternativesGroup.appendChild(tempNode)
            #dendogramAlternativesGroup.appendChild(__createXmlLineNode__(xmlDoc, subCluser[1], subCluser[2], xPositionNewCluster, yPositionNewCluster, alternativeDendogramLineColor, 1))
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, yPositionNewCluster)], fill= alternativeDendogramLineColor)
            #draw.line([(subCluser[1], subCluser[2]), (xPositionNewCluster, subCluser[2])], fill=(255,0,0))
            #draw.line((xPositionNewCluster, subCluser[2], xPositionNewCluster, yPositionNewCluster), fill=(255,0,0))

            # now remove the old clustersConcern from allClusters
            allClusters.remove(subCluser)
            #now add the new cluster to allClusters
        allClusters.append((cluster[0], xPositionNewCluster, yPositionNewCluster))
        i += 1
        #topElement.appendChild(dendogramAlternativesGroup)
    root.appendChild(dendogramAlternativesGroup)
    ####### end alternative dendogram draw #########

    #lets return the image
    return xmlDoc

#prototype function that will be used to create an image using xml
def getSimilarities(clustersConcern=[], clustersAlternative=[], matrix=[[]], maxMatrixCellValue=1, which="concern"):
    #cluster format is: [([element1, elemet2], distance), ([element1, elemet2, element3], distance), ......]


    concernClusterSimilarity = []
    alternativeClusterSimilarity = []

    #print alternativeClusterSimilarity

    #find the min similarity of the concern
    if (which == "concern"):
        for i in range(1, len(clustersConcern)):
            for j in range(1, len(clustersConcern[i])):
                clustersConcern[i][j] = int(
                    round((100 * (1 - (clustersConcern[i][j] / ((len(matrix) - 1) * (maxMatrixCellValue - 1))))), 0))

        return clustersConcern

        # if cluster[1] != 0:
        #     concernClusterSimilarity.append(100 * (1 - (cluster[1] / ((len(matrix) - 1) * (maxMatrixCellValue - 1)))))
        # else:
        #     concernClusterSimilarity.append(100)
    else:
        for i in range(1, len(clustersAlternative)):
            for j in range(1, len(clustersAlternative[i])):
                clustersAlternative[i][j] = int(
                    round((100 * (1 - (clustersAlternative[i][j] / ((len(matrix[0]) - 2) * (maxMatrixCellValue - 1))))),
                          0))

        return clustersAlternative

        #find the min similarity of the alternatives
        # for cluster in clustersAlternative:
        #     # if cluster[1] != 0:
        #     #     alternativeClusterSimilarity.append(100 * (1 - (cluster[1] / ((len(matrix[0]) - 2) * (maxMatrixCellValue - 1)))))
        #     # else:
        #     #     alternativeClusterSimilarity.append(100)


## returns a string with: 'rgb(number,number,number)'
#def createColorRGBString(color):
#    return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'

#""" 
#color is a tulp with 4 positions, (red, blue, green, alpha)
#"""
#def __createXmlLineNode__(xmlDoc, startX, startY, endX, endY, color=(0,0,0,100), width= 1):
#    
#    lineNode= xmlDoc.createElement('line') #main node
#    startXNode= xmlDoc.createElement('startX')
#    startYNode= xmlDoc.createElement('startY')
#    endXNode= xmlDoc.createElement('endX')
#    endYNode= xmlDoc.createElement('endY')
#    widthNode= xmlDoc.createElement('width')
#    
#    widthNode.appendChild(xmlDoc.createTextNode(str(width)))
#    startXNode.appendChild(xmlDoc.createTextNode(str(startX)))
#    startYNode.appendChild(xmlDoc.createTextNode(str(startY)))
#    endXNode.appendChild(xmlDoc.createTextNode(str(endX)))
#    endYNode.appendChild(xmlDoc.createTextNode(str(endY)))
#    colorNode= __createXmlColorNode__(xmlDoc, color)
#    
#    lineNode.appendChild(widthNode)
#    lineNode.appendChild(startXNode)
#    lineNode.appendChild(startYNode)
#    lineNode.appendChild(endXNode)
#    lineNode.appendChild(endYNode)
#    lineNode.appendChild(colorNode)
#    
#    return lineNode
#
#def __createXmlTextNode__(xmlDoc, topLeftX, topLeftY, text, width, height, fontName, fontSize, fontFillColor=(0,0,0,100)):
#    
#    textNode= xmlDoc.createElement('text') #main node
#    topLeftXNode= xmlDoc.createElement('x')
#    topLeftYNode= xmlDoc.createElement('y')
#    textValueNode= xmlDoc.createElement('textValue')
#    widthNode= xmlDoc.createElement('width')
#    heightNode= xmlDoc.createElement('height')
#    fontNode= __createXmlFontNode__(xmlDoc, fontName, fontSize, fontFillColor)
#    
#    topLeftXNode.appendChild(xmlDoc.createTextNode(str(topLeftX)))
#    topLeftYNode.appendChild(xmlDoc.createTextNode(str(topLeftY)))
#    textValueNode.appendChild(xmlDoc.createTextNode(text))
#    widthNode.appendChild(xmlDoc.createTextNode(str(width)))
#    heightNode.appendChild(xmlDoc.createTextNode(str(height)))
#    
#    textNode.appendChild(topLeftXNode)
#    textNode.appendChild(topLeftYNode)
#    textNode.appendChild(textValueNode)
#    textNode.appendChild(widthNode)
#    textNode.appendChild(heightNode)
#    textNode.appendChild(fontNode)
#    
#    return textNode
#
#def __createXmlFontNode__ (xmlDoc, fontName, fontSize, fontFillColor):
#    
#    fontNode= xmlDoc.createElement('font') #main node
#    nameNode= xmlDoc.createElement('name')
#    sizeNode= xmlDoc.createElement('size')
#    fillNode= xmlDoc.createElement('fill')
#    
#    nameNode.appendChild(xmlDoc.createTextNode(fontName))
#    sizeNode.appendChild(xmlDoc.createTextNode(str(fontSize)))
#    fillNode.appendChild(__createXmlColorNode__(xmlDoc ,fontFillColor))
#    
#    fontNode.appendChild(nameNode)
#    fontNode.appendChild(sizeNode)
#    fontNode.appendChild(fillNode)
#    
#    return fontNode
#    
#    
#""" 
#color is a tulp with 4 positions, (red, blue, green, alpha)
#"""
#def __createXmlColorNode__(xmlDoc, color= (0,0,0,100)):
#    
#    colorNode= xmlDoc.createElement('color') #main node
#    redNode= xmlDoc.createElement('red')
#    blueNode= xmlDoc.createElement('blue')
#    greenNode= xmlDoc.createElement('green')
#    alphaNode= xmlDoc.createElement('alpha')
#    
#    redNode.appendChild(xmlDoc.createTextNode(str(color[0])))
#    blueNode.appendChild(xmlDoc.createTextNode(str(color[1])))
#    greenNode.appendChild(xmlDoc.createTextNode(str(color[2])))
#    if len(color) >= 4:    
#        alphaNode.appendChild(xmlDoc.createTextNode(str(color[3])))
#    else:
#        alphaNode.appendChild(xmlDoc.createTextNode('100'))
#    
#    colorNode.appendChild(redNode)
#    colorNode.appendChild(blueNode)
#    colorNode.appendChild(greenNode)
#    colorNode.appendChild(alphaNode)
#    
#    return colorNode
    
