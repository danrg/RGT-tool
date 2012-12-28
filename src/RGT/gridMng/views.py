from django.shortcuts import render_to_response, render
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.template import loader
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.utils.timezone import utc
from datetime import datetime
from RGT.gridMng.models import Grid
from RGT.gridMng.models import Alternatives
from RGT.gridMng.models import Concerns
from RGT.gridMng.models import Ratings
from RGT.gridMng.models import Facilitator
from RGT.gridMng.utility import createXmlErrorResponse, createXmlSuccessResponse, randomStringGenerator, validateName, convertSvgTo, getImageError,\
    createDateTimeTag

from RGT.gridMng.session.state import State
from RGT.gridMng.template.showGridsData import ShowGridsData
from RGT.gridMng.template.gridTableData import GridTableData
from RGT.gridMng.template.createMyGridBaseData import CreateMyGridBaseData
from RGT.gridMng.template.createMyGridData import CreateMyGridData
from django.db import IntegrityError
from RGT.gridMng.error.unablaToCreateUSID import UnablaToCreateUSID

from RGT.gridMng.utility import generateGridTable, createDendogram, createFileResponse
from RGT.settings import GRID_USID_KEY_LENGTH

import sys, os
import traceback

from io import BytesIO
from types import StringType
from RGT.gridMng.fileData import fileData

def getCreateMyGridPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        tableOnly= False
        if request.REQUEST.has_key('tableOnly'):
            if request.REQUEST['tableOnly'] == 'true':
                tableOnly= True
    
        gridTableTemplate= GridTableData(generateGridTable(None))
        gridTableTemplate.changeRatingsWeights= True
        gridTableTemplate.changeCornAlt= True
        gridTableTemplate.tableId= randomStringGenerator()
             
        context= None 
        #RequestContext(request, {'data': gridTableTemplate })
        if tableOnly:
            template= loader.get_template('gridMng/createMyGridBase.html')
            templateData= CreateMyGridBaseData(gridTableTemplate)
            context= RequestContext(request, {'data': templateData })
            htmlData= template.render(context)
            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
        else:
            templateData= CreateMyGridData(CreateMyGridBaseData(gridTableTemplate))
            context= RequestContext(request, {'data': templateData })
            return render(request, 'gridMng/createMyGrid.html', context_instance=context)

    except:
        #do nothing
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('unknown error'), content_type='application/xml')

#extraXmlData is only added if the response is a success
def ajaxCreateGrid(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    if request.method == 'POST':
        
        #for key in request.REQUEST.keys():
        #    print 'key: ' + key + ' values: ' + request.REQUEST[key]
        #print '------'
        
        gridType= None
        userObj= request.user
        isConcernAlternativeResponseGrid= False
        #check the if the inputs are correct
        if request.POST.has_key('nAlternatives') and request.POST.has_key('nConcerns'): #and request.POST.has_key('gridName')
            if request.POST.has_key('gridType'):
                if request.POST['gridType'] == 'response':
                    return HttpResponse(createXmlErrorResponse("Invalid request, unsupported operation"), content_type='application/xml') 
                elif request.POST['gridType'] == 'user':
                    gridType= Grid.GridType.USER_GRID
                else:
                    return HttpResponse(createXmlErrorResponse("Unsupported grid type"), content_type='application/xml')
            else:
                #if the gridType key is not found assume it is a user grid
                gridType= Grid.GridType.USER_GRID
        else:
            return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')

        #lets validate the data
        try:                
            obj= __validateInputForGrid__(request, isConcernAlternativeResponseGrid)
        except KeyError as error:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
        except ValueError as error:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
        nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues= obj
        gridName= None
        if request.POST.has_key('gridName'):
            result= validateName(request.POST['gridName'])
            if  type(result) == StringType:
                gridName= result
            else:
                return result
        try:
            createGrid(userObj, gridType,  gridName, nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, True)
        except:
            #return render_to_response('gridMng/createGrid.html', {'existingProjectName': request.REQUEST['grid']}, context_instance=RequestContext(request))
            return HttpResponse(createXmlErrorResponse("Could not create grid."), content_type='application/xml')
    #return an empty grid page
    return getCreateMyGridPage(request)


def getShowGridPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    user1= request.user
    templateData= ShowGridsData()
    templateData.grids= user1.grid_set.all();

    if len(templateData.grids) <= 0:
        templateData.grids= None

    context= RequestContext(request, {'data' : templateData})

    return render(request, 'gridMng/showMyGrids.html', context_instance = context)

def ajaxGetGrid(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    user1= request.user
    
    #####view mode values########################################################################
    # all: show the concerns/alternatives and ratings/weights                                   #
    # ac: show only alternatives and concerns (only works with write mode read)                 #
    #############################################################################################
    
    #####write mode values#######################################
    # read: can only see the values                             #
    # write: can see and change the values                      #
    #############################################################
    
    #####check table values#######################################
    # true: will call the javascript function isTableSaved()     #
    # false: will not call the javascript function isTableSaved()#
    ##############################################################
    
    checkForTableIsSave= False
    changeRatingsWeights= False
    changeCornAlt= False
    showRatingWhileFalseChangeRatingsWeights= True
    error= None;
    
    #validate the options
    gridUSID = None
    viewMode = None
    writeMode = None
    try:
        gridUSID= request.REQUEST['gridUSID']
        viewMode= request.REQUEST['viewMode']
        writeMode= request.REQUEST['writeMode']
    except KeyError:
        error = 'Invalid arguments.'
    
    #variable check
    try:
        if not gridUSID:
            error= 'name of the grid was not specified'
        if not viewMode:
            viewMode= 'all'
        if not writeMode:
            writeMode= 'write'
            
        if writeMode == 'write':
            changeCornAlt= True
            changeRatingsWeights= True
            if viewMode == 'ac':
                showRatingWhileFalseChangeRatingsWeights= False
        
        if request.REQUEST.has_key('checkTable'):
            if request.REQUEST['checkTable'] == 'true':
                checkForTableIsSave= True
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        error= 'one or more variables were not found'
    
    if not error:
        # create the table for the template
        grids= user1.grid_set
        gridObj= grids.filter(usid= gridUSID) #gridObj is first a list 
        if len(gridObj) > 0:
            gridObj= gridObj[0]
            try:
                templateData= GridTableData(generateGridTable(gridObj))
                templateData.tableId= randomStringGenerator()
                templateData.changeRatingsWeights= changeRatingsWeights
                templateData.changeCornAlt= changeCornAlt
                templateData.showRatingWhileFalseChangeRatingsWeights= showRatingWhileFalseChangeRatingsWeights
                templateData.checkForTableIsSave= checkForTableIsSave
                #dic= __generateGridTable__(gridObj)
                template= loader.get_template('gridMng/gridTable.html')
                context= RequestContext(request, {'data': templateData})
                htmlData= template.render(context)
                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                #return render_to_response('gridMng/gridTable.html', {'table' : table, 'tableHeader': header, 'hiddenFields': hidden, 'weights':concernWeights, 'showRatings':showRatings, 'readOnly':readOnly, 'checkForTableIsSave':checkForTableIsSave }, context_instance=RequestContext(request))
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                return HttpResponse(createXmlErrorResponse('unknown error'), content_type='application/xml')                
        else:
            return HttpResponse(createXmlErrorResponse('Grid was not found'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse(error), content_type='application/xml')
    

def ajaxUpdateGrid(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    
    for key in request.REQUEST.keys():
        print 'key: ' + key + ' values: ' + request.REQUEST[key]
    print '------'
    
    user1= request.user
    gridObj= None
    isConcernAlternativeResponseGrid= False
    
    #lets determine what type of grid we are dealing with here
    if request.POST.has_key('gridType'):
        gridType= request.POST['gridType']
        if gridType == 'session':
            if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
                facilitatorObj= Facilitator.objects.isFacilitator(request.user)
                if facilitatorObj :
                    session= facilitatorObj.session_set.filter(usid= request.POST['sessionUSID'])
                    if len(session) >= 1:
                        session= session[0]
                        sessionGridRelation= session.sessiongrid_set.filter(iteration= request.POST['iteration'])
                        if len(sessionGridRelation) >= 1:
                            if session.state.name == State.CHECK:
                                gridObj= sessionGridRelation[0].grid
                            else:
                                return HttpResponse(createXmlErrorResponse("Grid can\t be changed in the current session state"), content_type='application/xml')
                        else:
                            return HttpResponse(createXmlErrorResponse("Grid was not found"), content_type='application/xml')
                    else:
                        return HttpResponse(createXmlErrorResponse("Session was not found"), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse("You are not a facilitator, can't change grid"), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
        elif gridType == 'response':
            return HttpResponse(createXmlErrorResponse("Invalid request, unsupported operation"), content_type='application/xml')
        elif gridType == 'user':
            gridObj= Grid.objects.get(user= user1, usid= request.POST['gridUSID'])
    else:
        try:
            gridObj= Grid.objects.get(user= user1, usid= request.POST['gridUSID'])
        except:
            pass

    if request.POST.has_key('gridName'):
        gridCheckNameResult= validateName(request.POST['gridName'])
        if  type(gridCheckNameResult) == StringType:
            gridObj.name= gridCheckNameResult
        else:
            #if the grid name isn't a string than it is an error
            return gridCheckNameResult
    #because django will save stuff to the database even if .save() is not called, we need to validate everything before starting to create the objects that will be used to populate the db
    obj= None
    try:
        obj= __validateInputForGrid__(request, isConcernAlternativeResponseGrid)
    except KeyError as error:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
    except ValueError as error:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
    nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues= obj     
    
    #update the grid
    if gridObj != None: 
        try:   
            isGridCreated= updateGrid(gridObj , nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, isConcernAlternativeResponseGrid)
            if isGridCreated:
                return HttpResponse(createXmlSuccessResponse('Grid was saved', createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), content_type='application/xml')
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse("No grid found"), content_type='application/xml')
    
def ajaxDeleteGrid(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    if request.POST.has_key('gridUSID'):
        gridUSID= request.POST['gridUSID']
        grid= None
        try:
            grid= Grid.objects.get(user= request.user, usid= gridUSID)
        except:
            HttpResponse(createXmlErrorResponse('couldn\'t find grid'), content_type='application/xml')
        if grid != None:
            grid.delete()
            return HttpResponse(createXmlSuccessResponse('Grid was deleted'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing arguments'), content_type='application/xml')

def ajaxGenerateDendogram(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    if request.POST.has_key('gridUSID'):
        grid1= Grid.objects.filter(user= request.user, usid= request.POST['gridUSID'])
        if len(grid1) >= 1:
            try:
                grid1= grid1[0]
                if grid1.dendogram != None and grid1.dendogram != '':
                    #test
                    xml= createDendogram(grid1)
                    f = open('D:/Temp/newSvgText.svg','w')
                    f.write(xml)
                    f.close()
                    #end test
                    return HttpResponse(grid1.dendogram, content_type='application/xml')
                else:
                    try:     
                        imgData= createDendogram(grid1)
                        return HttpResponse(imgData, content_type='application/xml')
                    except:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        return HttpResponse(createXmlErrorResponse('Unknown dendrogram error'), content_type='application/xml')
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('Could not find the grid to generate the dendrogram'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')

#This function will return the html code that is needed to generate the dialog box 
#that is used to ask to user to which format should a svg image be saved
def ajaxGetSaveSvgPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    
    template= loader.get_template('gridMng/saveSvg.html')
    context= RequestContext(request, {})
    htmlData= template.render(context)
    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
    
#this function will receive a svg string and will convert it to another file type
def ajaxConvertSvgTo(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        if request.POST.has_key('data') and request.POST.has_key('fileName') and request.POST.has_key('convertTo'):
            if request.POST['data'] and request.POST['convertTo']:
                imgData= __convertSvgStringTo__(request.POST['data'], request.POST['convertTo'])
                if not request.POST['fileName']:
                    imgData.fileName= randomStringGenerator()
                else:
                    imgData.fileName= request.POST['fileName']
                return createFileResponse(imgData)             
        else:
            if not request.POST.has_key('data'):
                raise Exception('data key was not received')
            if not request.POST.has_key('convertTo'):
                raise Exception('convertTo key was not received')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    #in case of an error or checks failing return an image error
    errorImageData= getImageError()
    # send the file
    response = HttpResponse(errorImageData, content_type= 'image/jpg')
    response['Content-Disposition'] = 'attachment; filename=error.jpg'
    return response

#this function will convert the dendrogram to a image file
def dendrogramTo(request):
    
    #########################################
    ############## Options ##################
    #########################################
    #                                       #
    #convertTo: svg                         #
    #gridUSID: usid of the grid in question #
    #########################################
    
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        if request.POST.has_key('gridUSID') and request.POST.has_key('convertTo'):
            #check to see if the inputs are not None
            if request.POST['gridUSID'] and request.POST['convertTo']:
                grid= Grid.objects.filter(usid= request.POST['gridUSID'])
                if len(grid) >= 1:
                    grid= grid[0] 
                    data= __convertSvgStringTo__(grid.dendogram, request.POST['convertTo'])
                    if request.POST.has_key('fileName'):
                        data.fileName= request.POST['fileName']
                    else:
                        data.fileName= randomStringGenerator()
                    
                    #return the file
                    return createFileResponse(data)
            else:
                if not request.POST['gridUSID']:
                    raise ValueError('gridUSID had an invalid value: ' + request.POST['gridUSID'])
                if not request.POST['convertTo']:
                    raise ValueError('convertTo had an invalid value: ' + request.POST['convertTo'])
        else:
            if not request.POST.has_key('gridUSID'):
                raise Exception('gridUSID key was not received')
            if not request.POST.has_key('convertTo'):
                raise Exception('convertTo key was not received')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60                 
    #in case of an error or failing of one the checks return an image error
    errorImageData= getImageError()
    # send the file
    response = HttpResponse(errorImageData, content_type= 'image/jpg')
    response['Content-Disposition'] = 'attachment; filename=error.jpg' 
    return response
    
def __convertSvgStringTo__(svgString= None, convertTo= None):
    fpInMemory = None
    imgData= fileData()
    if svgString and convertTo:
        if convertTo == 'svg':
            imgData.data= svgString
            imgData.ContentType= 'image/svg+xml'
            imgData.fileExtention= 'svg'
            #response = HttpResponse(request.POST['data'], content_type='image/svg+xml')
            #response['Content-Disposition'] = 'attachment; filename=' + fileName + '.svg'
            #return response
            return imgData
        
        #################################################################
        ## Warning, old code that wasn't tested with the new functions ##
        #################################################################
        else:
                (imageFileName, mimeType, fileExtention)= convertSvgTo(svgString, convertTo)
                imgData.ContentType= mimeType
                imgData.fileExtention= fileExtention
                if imageFileName != None:
                    fpInMemory= BytesIO()
                    fp= open(imageFileName, "rb")
                    
                    #read the file and place it in memory
                    try:
                        byte= fp.read(1)
                        while byte != '':
                            fpInMemory.write(byte)
                            byte= fp.read(1)
                    finally:
                        fp.close()
                        os.remove(imageFileName)
                    
                    imgData.data= fpInMemory.getvalue()
                    imgData.length= fpInMemory.tell()
                    # send the file
                    #response = HttpResponse(fpInMemory.getvalue(), content_type= mimeType)
                    #response['Content-Length'] = fpInMemory.tell()
                    #fileName= request.POST['fileName']
                    #if fileName != None and fileName != '':
                    #    response['Content-Disposition'] = 'attachment; filename=' + fileName + fileExtention
                    #else:
                    #    response['Content-Disposition'] = 'attachment; filename=' + randomStringGenerator() + fileExtention
                    #return response
                    return imgData
                else:
                    raise Exception('Error image file name was None')
#                    imgData.ContentType= 'image/jpg'
#                    
#                    errorImageData= getImageError()
#                    # send the file
#                    response = HttpResponse(errorImageData, content_type= 'image/jpg')
#                    response['Content-Length'] = fpInMemory.tell()
#                    response['Content-Disposition'] = 'attachment; filename=error.jpg' 
#                    return response
    else:
        raise ValueError('svgString or convertTo was None')

def __validateInputForGrid__(request, isConcernAlternativeResponseGrid):

    concernValues= [] #this will contain a tuple with 3 values, (leftPole, rightPole, weight)
    alternativeValues= []
    ratioValues= []
    usedConcernNames= []
    

    i= 0
    j= 0
    nAlternatives= int(request.POST['nAlternatives'])
    nConcerns= int(request.POST['nConcerns'])
    
    #check if the keys with the alternatives are present
    while i < nAlternatives:
        keyName= 'alternative_' + str((i + 1)) + '_name'
        if not request.POST.has_key(keyName):
            #print 'Error key not found: ' + keyName
            raise KeyError('Invalid request, request is missing argument(s)', 'Error key not found: ' + keyName)
            #return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
        else:
            #alternative names should be unique in a grid, so lets check for that
            temp= request.POST[keyName].strip()
            if temp != '':
                if not temp in alternativeValues:
                    alternativeValues.append(temp)
                else:
                    raise ValueError("The name " + request.POST[keyName] + " is being used more than one time")
                    #return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"))
            else:
                raise ValueError("No empty values are allowed for alternatives")
                #return HttpResponse(createXmlErrorResponse("No empty values are allowed for alternatives"), content_type='application/xml') 
        i+= 1
    
    i= 0
    #check if all the keys for the left and right pole are present
    while i < nConcerns:
        leftPole= None
        rightPole= None
        #check the left pole first
        keyName= 'concern_'+ str((i + 1)) + '_left'
        if not request.POST.has_key(keyName):
            #print 'Error key not found: ' + keyName
            raise KeyError('Invalid request, request is missing argument(s)',  'Error key not found: ' + keyName)
            #return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
        else:
            #the right and left pole can be None so convert the empty string into None
            leftPole= request.POST[keyName]
            if leftPole == '':
                leftPole= None
            #the names of the left and right pole should be unique in a grid, so lets check for that. If the left pole is none, allow it to be saved
            if not leftPole in usedConcernNames or leftPole == None:
                usedConcernNames.append(leftPole)
            else:
                raise ValueError("The name " + request.POST[keyName] + " is being used more than one time")
                #return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"), content_type='application/xml')
        #check the right pole
        keyName= 'concern_'+ str((i + 1)) + '_right'
        if not request.POST.has_key(keyName):
            #print 'Error key not found: ' + keyName
            raise KeyError('Invalid request, request is missing argument(s)', 'Error key not found: ' + keyName)
            #return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
        else:
            #the right and left pole can be None so convert the empty string into None
            rightPole= request.POST[keyName].strip()
            if rightPole == '':
                rightPole= None
            #the names of the left and right pole should be unique in a grid, so lets check for that. If the right pole is none, allow it to be saved
            if not rightPole in usedConcernNames or rightPole == None:
                usedConcernNames.append(rightPole)
            else:
                raise ValueError("The name " + request.POST[keyName] + " is being used more than one time")
                #return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"), content_type='application/xml')
        #if it is a response grid of the alternative.concern we don't need to check for the weights as they will not be there
        if not isConcernAlternativeResponseGrid:
            #lets check if the weight key is present
            keyName= 'weight_concern'+ str((i + 1))
            if not request.POST.has_key(keyName):
                #print 'Error key not found: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)', 'Error key not found: ' + keyName)
                #return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
            else:
                #allowed values for the values are None, '', ' ' and numbers
                keyValue= request.POST[keyName]
                if not (keyValue == None or keyValue == ' ' or keyValue == ''): 
                    try:
                        value= float(keyValue)
                        concernValues.append((leftPole, rightPole, value))
                    except:
                        raise ValueError("Invalid input " + keyValue)
                        #return HttpResponse(createXmlErrorResponse("Invalid input " + keyValue), content_type='application/xml')
                else:
                    concernValues.append((leftPole, rightPole, None)) 
        else:
            concernValues.append((leftPole, rightPole, None))
        i+= 1
    i= 0
    
    #we are going to check the ratios now, because the response grid for the alternative/concern doesn't have ratios we don't need to check for them
    if not isConcernAlternativeResponseGrid:
        i= 0
        j= 0
        hasEmptyConcern= False;
        while i < nConcerns:
            ratios= []
            #it is not allowed to have rations in an concern that has no leftPole or rightPole
            if concernValues[i][0] != None and concernValues[i][1] != None:
                hasEmptyConcern= False
            else:
                hasEmptyConcern= True
            while j < nAlternatives:
                keyName= 'ratio_concer' + str((i + 1)) +'_alternative' + str(( j + 1))
                if not request.POST.has_key(keyName):
                    #print 'Error key not found: ' + keyName
                    raise KeyError('Invalid request, request is missing argument(s)', 'Error key not found: ' + keyName)
                    #return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
                else:
                    keyValue= request.POST[keyName].strip()
                    #valid values for the they are None, ' ', '' and numbers, anything else is not allowed
                    if not (keyValue == None or keyValue == ''):
                        if hasEmptyConcern:
                            raise ValueError('It is not allowed to have ratings while the concern is empty')
                            #return HttpResponse(createXmlErrorResponse('It is not allowed to have ratings while the concern is empty'), content_type='application/xml')
                        else:
                            try:
                                value= float(keyValue)
                                ratios.append(value)
                            except:
                                raise ValueError("Invalid value: " + keyValue)
                                #return HttpResponse(createXmlErrorResponse("Invalid value: " + keyValue), content_type='application/xml')
                    else:
                        ratios.append(None)
                j+= 1
            ratioValues.append(ratios)
            j= 0
            i+= 1
    return (nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues)
    
    


#intern function used to update a grid
def updateGrid(gridObj, nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, isConcernAlternativeResponseGrid):
    if gridObj != None:
        valuesChanged= None #use to check if we need to clear the dendogram field in the Grid model
        objToCommit= []
        totalConcenrs= gridObj.concerns_set.all().count()
        totalAlternatives= gridObj.alternatives_set.all().count()
        alternatives= []
        concerns= []
           
        for obj in gridObj.alternatives_set.all():
            alternatives.append(obj)
            
        for obj in gridObj.concerns_set.all():
            concerns.append(obj)
            
        i= 0;
        j= 0;
            
        #remove the concerns and alternatives first, this is because we want to avoid any type of database errors
        if nConcerns < totalConcenrs:
            valuesChanged= 1
            i= totalConcenrs - nConcerns
            while i > 0:
                concern1= concerns.pop()
                concern1.delete()
                i-= 1
        if nAlternatives < totalAlternatives:
            valuesChanged= 1
            i= totalAlternatives - nAlternatives
            while i > 0:
                alternative1= alternatives.pop()
                alternative1.delete()
                i-= 1
            
        i= 0
        #lets update what we have
        #lets check what changed with the concerns first
        while i < nConcerns and i < totalConcenrs:
            #check if the name of the concern is the same
            if concerns[i].leftPole != concernValues[i][0] or concerns[i].rightPole != concernValues[i][1]:
                concern1= concerns[i]
                concern1.leftPole= concernValues[i][0]
                concern1.rightPole= concernValues[i][1]
                if not valuesChanged:
                    valuesChanged= 1
                objToCommit.append(concern1)
            #check if the weight didn't change only if the grid is not an response grid from alternative/concerns as it doesn't have weights or ratios
            if not isConcernAlternativeResponseGrid:
                newWeight= concernValues[i][2]
                if concerns[i].weight != newWeight :
                    concern1= concerns[i]
                    concern1.weight= newWeight
                    if not valuesChanged:
                        valuesChanged= 1
                    objToCommit.append(concern1)
            i+= 1
        i= 0
        #check if the names are the same
        while i < nAlternatives and i < totalAlternatives:
            if alternatives[i].name != alternativeValues[i]:
                alternatives[i].name= alternativeValues[i]
                if not valuesChanged:
                    valuesChanged= 1
                objToCommit.append(alternatives[i])
            i+= 1
        i= 0
        j= 0
        #the alternative/concern response grid has no ratios, so just ignore it
        if not isConcernAlternativeResponseGrid:
            while i < nConcerns and i < totalConcenrs:
                while j < nAlternatives and j < totalAlternatives:
                    newValue= ratioValues[i][j]
                    #if request.POST.has_key('ratio_concer' + str(i + 1) + '_alternative' + str(j + 1)):
                        #newValue= float(request.POST['ratio_concer' + str(i + 1) + '_alternative' + str(j + 1)]) 
                    ratingObjList= Ratings.objects.filter(concern= concerns[i], alternative= alternatives[j])
                    if (len(ratingObjList) > 0):
                        ratingObj = ratingObjList[0]
                    # check to see if the rating had a value before, if not create the new value
                    if newValue != ratingObj.rating:
                        #update values here
                        ratingObj.rating= newValue
                        objToCommit.append(ratingObj)
                        if not valuesChanged:
                            valuesChanged= 1
                    j+= 1
                i+= 1
                j= 0
            
        #now lets take care of adding stuff
        if nConcerns > totalConcenrs:
            valuesChanged= 1
            i= totalConcenrs
            j= 0
            while i < nConcerns:
                concern= Concerns.objects.create(grid= gridObj, leftPole= concernValues[i][0], rightPole= concernValues[i][1], weight= concernValues[i][2])
                objToCommit.append(concern)
                concerns.append(concern)
                if not isConcernAlternativeResponseGrid:
                    #create ratios for the concern, ratios will be created only for the old known alternatives
                    while j < totalAlternatives:
                        rate= Ratings(concern= concerns[i], alternative= alternatives[j], rating= ratioValues[i][j])
                        objToCommit.append(rate)
                        j+= 1
                    j= 0
                i+= 1
        #here we know if we had more concerns it has already been added to the concern list, thus totalConcenrs == nConcerns now.
        if nAlternatives > totalAlternatives:
            valuesChanged= 1
            i= 0;
            j= totalAlternatives
            #lets create the new alternatives
            while i < (nAlternatives - totalAlternatives):
                #print request.REQUEST['alternative_' + str((totalAlternatives + i + 1)) + '_name']
                alternative= Alternatives.objects.create(grid= gridObj, name= alternativeValues[i + totalAlternatives])
                objToCommit.append(alternative)
                alternatives.append(alternative)
                i+= 1
            i= 0
            #create the ratios
            if not isConcernAlternativeResponseGrid:
                while i < nConcerns:
                    while j < nAlternatives:
                        rate= Ratings(concern= concerns[i], alternative= alternatives[j], rating= ratioValues[i][j])
                        objToCommit.append(rate);
                        j+= 1
                    j= totalAlternatives
                    i+= 1
        if valuesChanged:
            gridObj.dendogram= ''
            #check to see if the grid obj is already schedule to be saved
            if not (gridObj in objToCommit):
                objToCommit.append(gridObj)
        #now that all went ok commit the changes (except delete as that one is done when the function is called)
        for obj in objToCommit:
            obj.save()
        gridObj.dateTime = datetime.utcnow().replace(tzinfo=utc)
        gridObj.save()
        return True
    else:
        raise ValueError('GridObj was None')
    
#this function will create and save a basic grid. After successful creation the grid is returned 
def createGrid(userObj, gridType,  gridName, nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, createRatios):
    
    if userObj != None and gridType != None and nConcerns != None and nAlternatives != None and concernValues != None and alternativeValues != None and ratioValues != None and createRatios != None:
        try:
            gridObj= Grid.objects.create(user= userObj, grid_type= gridType)
            if gridName != None:
                gridObj.name= gridName
            gridObj.usid = randomStringGenerator(GRID_USID_KEY_LENGTH)
            gridObj.dateTime = datetime.utcnow().replace(tzinfo=utc)
            #gridObj.dateTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            try:
                gridObj.save()
            except IntegrityError as error:
                # check to see if the usid is duplicated or not
                results= Grid.objects.filter(usid= gridObj.usid)
                if len(results) >= 1:
                    #in this case the key was duplicated, so lets try to create a new key
                    maxAttempts= 5
                    wasGridSaved= False
                    while maxAttempts >= 0:
                        maxAttempts-= 1
                        key= randomStringGenerator(GRID_USID_KEY_LENGTH)
                        #check to see if this key is unique
                        results= Grid.objects.filter(usid= key)
                        if len(results) <= 0:
                            gridObj.usid= key
                            gridObj.save()
                            wasGridSaved= True
                            break
                    if wasGridSaved == False:
                        #in case we can not create a unique key, raise an error
                        raise UnablaToCreateUSID('Unable to create unique suid for the grid ' + gridName)
                    else:
                        #the integratyError was not caused by a duplicated suid so, raise it again
                        raise error
            #gridObj= Grid.objects.create(user= userObj, name= gridName)
            #print 'nAlternatives: ' + str(nAlternatives)
            
            alternatives= []
            concerns= []
            
            for i in range(int(nAlternatives)):
                alternative= Alternatives.objects.create(grid= gridObj, name= alternativeValues[i])
                alternatives.append(alternative)
            
            for i in range(int(nConcerns)):
                concern= Concerns.objects.create(grid= gridObj, leftPole= concernValues[i][0], rightPole= concernValues[i][1], weight= concernValues[i][2])
                concerns.append(concern)
            print ratioValues
            if createRatios:
                for i in range(int(nConcerns)):
                    for j in range(int(nAlternatives)):
                        Ratings.objects.create(concern= concerns[i], alternative= alternatives[j], rating= ratioValues[i][j])

            return gridObj
        except:
            try:
                gridObj.delete()
            except:
                print 'Could not delete the grid'
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
            raise
    else:
        raise ValueError('One or more variables were None')
