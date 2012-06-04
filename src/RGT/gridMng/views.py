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
from RGT.gridMng.models import Session
from RGT.gridMng.models import ResponseGrid
from RGT.gridMng.utility import createXmlErrorResponse, createXmlSuccessResponse, randomStringGenerator, validateName, convertSvgTo, getImageError,\
    createDateTimeTag
from RGT.gridMng.hierarchical import hcluster, drawDendogram2, transpose, drawDendogram3
from RGT.gridMng.session.state import State
import sys, os
import traceback
import base64
from io import BytesIO
from types import TupleType, StringType

def getCreateMyGridPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        tableOnly= False
        if request.REQUEST.has_key('tableOnly'):
            if request.REQUEST['tableOnly'] == 'true':
                tableOnly= True
    
        hidden= []
        defaultNConcerns= 3
        defaultNAlternatives= 2
        defaultWeightValue= 1.0
    
        table= [[""] * (defaultNAlternatives + 2) ] * defaultNConcerns
        header= [""] * defaultNAlternatives 
        concernWeights= [defaultWeightValue] * defaultNConcerns
    
        #hidden.append(( defaultNConcerns, 'nConcerns'))
        #hidden.append(( defaultNAlternatives, 'nAlternatives'))
        context= RequestContext(request, {'table' : table, 'tableHeader': header, 'weights':concernWeights, 'hiddenFields': hidden, 'changeRatingsWeights':True, 'changeCornAlt':True, 'tableId':randomStringGenerator() })
        if tableOnly:
            template= loader.get_template('gridMng/createMyGridBase.html')
            htmlData= template.render(context)
            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
        else:
            return render(request, 'gridMng/createMyGrid.html', context_instance=context)

    except:
        #do nothing
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('unknown error'), content_type='application/xml')

#extraXmlData is only added if the response is a success
def ajaxCreateGrid(request, extraXmlData= None):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    if request.method == 'POST':
        
        for key in request.REQUEST.keys():
            print 'key: ' + key + ' values: ' + request.REQUEST[key]
        print '------'
        
        gridObj= None
        userObj= request.user
        sessionIteration= -1
        sessionObj= None;
        isResponseGrid= False
        isConcernAlternativeResponseGrid= False
        #check the if the inputs are correct
        if request.POST.has_key('nAlternatives') and request.POST.has_key('nConcerns'): #and request.POST.has_key('gridName')
            if request.POST.has_key('gridType'):
                if request.POST['gridType'] == 'response':
                    if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
                        userObj= request.user
                        #check if user can answer to the session
                        sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
                        if len(sessionObj) >= 1:
                            sessionObj= sessionObj[0]
                            userSessionRelation= userObj.userparticipatesession_set.filter(session= sessionObj)
                            if len(userSessionRelation) >= 1:
                                sessionIteration= int(request.POST['iteration'])
                                if sessionObj.iteration == sessionIteration:
                                    if sessionObj.state.name == State.AC or sessionObj.state.name == State.RW:
                                        if sessionObj.state.name == State.AC:
                                            gridObj= Grid(grid_type= Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN);
                                            isResponseGrid= True
                                            isConcernAlternativeResponseGrid= True
                                        elif sessionObj.state.name == State.RW:
                                            gridObj= Grid(grid_type= Grid.GridType.RESPONSE_GRID_RATING_WEIGHT);
                                            isResponseGrid= True
                                    else:
                                        return HttpResponse(createXmlErrorResponse('Can\'t create response grid, session is in a state where that is not permitted'), content_type='application/xml')
                                else:
                                    return HttpResponse(createXmlErrorResponse('Can\'t create response grid, response iteration does not match current session iteration'), content_type='application/xml')
                            else:
                                return HttpResponse(createXmlErrorResponse('You are not participating in the session, can\'t send response grid'), content_type='application/xml')
                        else:
                            return HttpResponse(createXmlErrorResponse('Session was not found'), content_type='application/xml')
                    else:
                        return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml') 
                elif request.POST['gridType'] == 'user':
                    gridObj= Grid(user= userObj, grid_type= Grid.GridType.USER_GRID)
                else:
                    return HttpResponse(createXmlErrorResponse("Unsupported grid type"), content_type='application/xml')
            else:
                #if the gridType key is not found assume it is a user grid
                gridObj= Grid(user= userObj, grid_type= Grid.GridType.USER_GRID)
        else:
            return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
        
        #try:
        #    gridObj= Grid.objects.get(user= user1, name= gridName)
        #except:
        #    pass
        if gridObj != None:
            #lets validate the data, this needs to be done before we start creating the db objects because django will save the objects even if we don't ask to save it
            nConcerns= None
            nAlternatives= None
            concernValues= None
            alternativeValues= None
            ratioValues= None
            obj= __validateInputForGrid__(request, isConcernAlternativeResponseGrid)
            if type(obj) != TupleType:
                return obj
            nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues= obj
            try:
                if request.POST.has_key('gridName'):
                    result= validateName(request.POST['gridName'])
                    if  type(result) == StringType:
                        gridObj.name= result
                    else:
                        return result
                
                gridObj.usid = randomStringGenerator(20)
                gridObj.dateTime = datetime.utcnow().replace(tzinfo=utc)
                #gridObj.dateTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                gridObj.save()
                #gridObj= Grid.objects.create(user= userObj, name= gridName)
                #print 'nAlternatives: ' + str(nAlternatives)
                
                alternatives= []
                concerns= []
                i= 0
                
                while i < nAlternatives:
                    alternative= Alternatives.objects.create(grid= gridObj, name= alternativeValues[i])
                    alternatives.append(alternative)
                    i+= 1
                    
                i= 0
                while i < nConcerns:
                    concern= Concerns.objects.create(grid= gridObj, leftPole= concernValues[i][0], rightPole= concernValues[i][1], weight= concernValues[i][2])
                    concerns.append(concern)
                    i+= 1
                i= 0
                j= 0
                if not isConcernAlternativeResponseGrid:
                    while i < nConcerns:
                        while j < nAlternatives:
                            Ratings.objects.create(concern= concerns[i], alternative= alternatives[j], rating= ratioValues[i][j])
                            j+= 1
                        i+= 1
                        j= 0
                #ok, the grid was created now if the grid is a response grid, add it to the ResponseGrid table
                if isResponseGrid:
                    gridResponseRelation=  ResponseGrid(grid= gridObj, session= sessionObj, iteration= sessionIteration, user= userObj)
                    gridResponseRelation.save()
                    
                    #check if we need to pass extra data into the xml success response
                    if extraXmlData == None:
                        return HttpResponse(createXmlSuccessResponse('Grid created successfully.', createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), content_type='application/xml')
                    else:
                        extraDataToUse= None
                        if isinstance(extraXmlData, list):
                            extraXmlData.append(createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            extraDataToUse= extraXmlData
                        else:
                            extraDataToUse= [extraXmlData, createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
                        return HttpResponse(createXmlSuccessResponse('Grid created successfully.', extraDataToUse), content_type='application/xml')
            except:
                try:
                    gridObj.delete()
                except:
                    print 'Could not delete the grid'
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                return HttpResponse(createXmlErrorResponse("Could not create grid."), content_type='application/xml')
        else:
            #return render_to_response('gridMng/createGrid.html', {'existingProjectName': request.REQUEST['grid']}, context_instance=RequestContext(request))
            return HttpResponse(createXmlErrorResponse("Could not create grid."), content_type='application/xml') 
    return getCreateMyGridPage(request)


def getShowGridPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    user1= request.user
    grids= user1.grid_set.all();

    if len(grids) <= 0:
        grids= None

    context= RequestContext(request, {'grids' : grids})

    return render(request, 'gridMng/showMyGrids.html', context_instance = context)

def getGridNavigationPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    return render_to_response('gridMng/gridNavigation.html', {}, context_instance=RequestContext(request))

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
                dic= __generateGridTable__(gridObj);
                template= loader.get_template('gridMng/gridTable.html')
                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'],
                                                  'changeRatingsWeights':changeRatingsWeights, 'changeCornAlt':changeCornAlt,
                                                  'showRatingWhileFalseChangeRatingsWeights':showRatingWhileFalseChangeRatingsWeights,
                                                  'checkForTableIsSave':checkForTableIsSave, 'tableId':randomStringGenerator() })
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
            if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
                sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
                if len(sessionObj) >= 1:
                    sessionObj= sessionObj[0]
                    sessionIteration= int(request.POST['iteration'])
                    if sessionIteration == sessionObj.iteration:
                        responseGridRelation= request.user.responsegrid_set.filter(session= sessionObj, iteration= sessionIteration)
                        if len(responseGridRelation) >= 1:
                            gridObj= responseGridRelation[0].grid
                            if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                                isConcernAlternativeResponseGrid= True
                    else:
                        return HttpResponse(createXmlErrorResponse("Can't update grid, session is in a state where that is not permitted"), content_type='application/xml') 
                else:
                    return HttpResponse(createXmlErrorResponse("Session was not found"), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
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
    obj= __validateInputForGrid__(request, isConcernAlternativeResponseGrid)
    if type(obj) != TupleType:
        return obj
    nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues= obj     
        
    if gridObj != None:
        try:
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
            return HttpResponse(createXmlSuccessResponse('Grid was saved', createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), content_type='application/xml')
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse("unknown error"), content_type='application/xml')
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
                    return HttpResponse(grid1.dendogram, content_type='application/xml')
                else:
                    try:     
                        imgData= __createDendogram__(grid1)
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

#this is a prototype function
def ajaxSaveSvgPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    
    template= loader.get_template('gridMng/saveSvg.html')
    context= RequestContext(request, {})
    htmlData= template.render(context)
    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
    
#this is a prototype function   
def ajaxConvertSvgTo(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    fpInMemory = None
    try:
        if request.POST.has_key('data') and request.POST.has_key('fileName') and request.POST.has_key('convertTo'):
            if request.POST['convertTo'] == 'svg':
                fileName= request.POST['fileName']
                #if the file name is empty generate a file name
                if  fileName == '':
                    fileName= randomStringGenerator()
                response = HttpResponse(request.POST['data'], content_type='image/svg+xml')
                response['Content-Disposition'] = 'attachment; filename=' + fileName + '.svg'
                return response

            else:
                try:
                    (imageFileName, mimeType, fileExtention)= convertSvgTo(request.POST['data'], request.POST['convertTo'])
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
                        
                        # send the file
                        response = HttpResponse(fpInMemory.getvalue(), content_type= mimeType)
                        response['Content-Length'] = fpInMemory.tell()
                        fileName= request.POST['fileName']
                        if fileName != None and fileName != '':
                            response['Content-Disposition'] = 'attachment; filename=' + fileName + fileExtention
                        else:
                            response['Content-Disposition'] = 'attachment; filename=' + randomStringGenerator() + fileExtention
                        return response
                    else:
                        errorImageData= getImageError()
                        # send the file
                        response = HttpResponse(errorImageData, content_type= 'image/jpg')
                        response['Content-Length'] = fpInMemory.tell()
                        response['Content-Disposition'] = 'attachment; filename=error.jpg' 
                        return response
                except:
                    print "Exception in user code:"
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    errorImageData= getImageError()
                    # send the file
                    response = HttpResponse(errorImageData, content_type= 'image/jpg')
                    response['Content-Disposition'] = 'attachment; filename=error.jpg'
                    return response 
        else:
            errorImageData= getImageError()
            # send the file
            response = HttpResponse(errorImageData, content_type= 'image/jpg')
            response['Content-Length'] = fpInMemory.tell()
            response['Content-Disposition'] = 'attachment; filename=error.jpg'
            return response 
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        errorImageData= getImageError()
        # send the file
        response = HttpResponse(errorImageData, content_type= 'image/jpg')
        response['Content-Length'] = fpInMemory.tell()
        response['Content-Disposition'] = 'attachment; filename=error.jpg'
        return response         
    
def __generateGridTable__(gridObj):
    table= []
    header= []
    i= 0;
    j= 0;
    concerns= gridObj.concerns_set.all()
    alternatives= gridObj.alternatives_set.all()
    nConcern= gridObj.concerns_set.all().count()
    nAlternatives= gridObj.alternatives_set.all().count()
    concernWeights= []
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
    dic= {};
    dic['table']= table
    dic['tableHeader']= header
    dic['weights']= concernWeights
    return dic

def __validateInputForGrid__(request, isConcernAlternativeResponseGrid):
    nAlternatives= None
    nConcerns= None 
    concernValues= [] #this will contain a tuple with 3 values, (leftPole, rightPole, weight)
    alternativeValues= []
    ratioValues= []
    usedConcernNames= []
    
    try:
        i= 0
        j= 0
        nAlternatives= int(request.POST['nAlternatives'])
        nConcerns= int(request.POST['nConcerns'])
        
        #check if the keys with the alternatives are present
        while i < nAlternatives:
            keyName= 'alternative_' + str((i + 1)) + '_name'
            if not request.POST.has_key(keyName):
                return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
            else:
                #alternative names should be unique in a grid, so lets check for that
                temp= request.POST[keyName].strip()
                if temp != '':
                    if not temp in alternativeValues:
                        alternativeValues.append(temp)
                    else:
                        return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"))
                else:
                    return HttpResponse(createXmlErrorResponse("No empty values are allowed for alternatives"), content_type='application/xml') 
            i+= 1
        
        i= 0
        #check if all the keys for the left and right pole are present
        while i < nConcerns:
            leftPole= None
            rightPole= None
            #check the left pole first
            keyName= 'concern_'+ str((i + 1)) + '_left'
            if not request.POST.has_key(keyName):
                return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
            else:
                #the right and left pole can be None so convert the empty string into None
                leftPole= request.POST[keyName]
                if leftPole == '':
                    leftPole= None
                #the names of the left and right pole should be unique in a grid, so lets check for that. If the left pole is none, allow it to be saved
                if not leftPole in usedConcernNames or leftPole == None:
                    usedConcernNames.append(leftPole)
                else:
                    return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"), content_type='application/xml')
            #check the right pole
            keyName= 'concern_'+ str((i + 1)) + '_right'
            if not request.POST.has_key(keyName):
                return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
            else:
                #the right and left pole can be None so convert the empty string into None
                rightPole= request.POST[keyName].strip()
                if rightPole == '':
                    rightPole= None
                #the names of the left and right pole should be unique in a grid, so lets check for that. If the right pole is none, allow it to be saved
                if not rightPole in usedConcernNames or rightPole == None:
                    usedConcernNames.append(rightPole)
                else:
                    return HttpResponse(createXmlErrorResponse("The name " + request.POST[keyName] + " is being used more than one time"), content_type='application/xml')
            #if it is a response grid of the alternative.concern we don't need to check for the weights as they will not be there
            if not isConcernAlternativeResponseGrid:
                #lets check if the weight key is present
                keyName= 'weight_concern'+ str((i + 1))
                if not request.POST.has_key(keyName):
                    return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
                else:
                    #allowed values for the values are None, '', ' ' and numbers
                    keyValue= request.POST[keyName]
                    if not (keyValue == None or keyValue == ' ' or keyValue == ''): 
                        try:
                            value= float(keyValue)
                            concernValues.append((leftPole, rightPole, value))
                        except:
                            return HttpResponse(createXmlErrorResponse("Invalid input " + keyValue), content_type='application/xml')
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
                        return HttpResponse(createXmlErrorResponse("Invalid request, request is missing argument(s)"), content_type='application/xml')
                    else:
                        keyValue= request.POST[keyName].strip()
                        #valid values for the they are None, ' ', '' and numbers, anything else is not allowed
                        if not (keyValue == None or keyValue == ''):
                            if hasEmptyConcern:
                                return HttpResponse(createXmlErrorResponse('It is not allowed to have ratings while the concern is empty'), content_type='application/xml')
                            else:
                                try:
                                    value= float(keyValue)
                                    ratios.append(value)
                                except:
                                    return HttpResponse(createXmlErrorResponse("Invalid value: " + keyValue), content_type='application/xml')
                        else:
                            ratios.append(None)
                    j+= 1
                ratioValues.append(ratios)
                j= 0
                i+= 1
        return (nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues)
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse("Request could not be processed, invalid argument(s)"), content_type='application/xml')
    
def __createDendogram__(gridObj):
 
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