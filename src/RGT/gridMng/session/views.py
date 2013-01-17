from django.shortcuts import render_to_response, render
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.template import loader
from django.http import HttpResponse #,HttpResponseRedirect
from RGT.gridMng.models import Grid
from RGT.gridMng.models import Ratings
from RGT.gridMng.models import Facilitator
from RGT.gridMng.models import Session
from RGT.gridMng.models import State
from RGT.gridMng.models import SessionGrid
from RGT.gridMng.models import ResponseGrid
from RGT.gridMng.models import SessionIterationState
from RGT.gridMng.models import UserParticipateSession
from RGT.gridMng.session.state import State as SessionState
from RGT.gridMng.error.userAlreadyParticipating import UserAlreadyParticipating
from RGT.gridMng.error.wrongState import WrongState
from RGT.gridMng.error.userIsFacilitator import UserIsFacilitator
from RGT.gridMng.error.wrongGridType import WrongGridType
from RGT.gridMng.error.wrongSessionIteration import WrongSessionIteration
from RGT.gridMng.utility import randomStringGenerator, validateName, SessionResultImageConvertionData, convertRatingWeightSessionResultToSvg, createFileResponse, convertAlternativeConcernSessionResultToSvg
from RGT.gridMng.response.xml.htmlResponseUtil import createXmlErrorResponse, createXmlSuccessResponse, createXmlForComboBox, createDateTimeTag
from RGT.gridMng.response.xml.svgResponseUtil import createSvgResponse
from RGT.gridMng.response.xml.generalUtil import createXmlGridIdNode, createXmlNumberOfResponseNode
from RGT.gridMng.views import updateGrid, createGrid, __validateInputForGrid__
from math import sqrt, ceil
from RGT.gridMng.template.session.createSessionData import CreateSessionData
from RGT.gridMng.template.session.mySessionsData import MySessionsData
from RGT.gridMng.template.session.mySessionsContentData import MySessionsContentData
from RGT.gridMng.template.session.participatingSessionsData import ParticipatingSessionsData
from RGT.gridMng.template.session.participatingSessionsContentData import ParticipatingSessionsContentData
from RGT.gridMng.template.session.resultAlternativeConcernTableData import ResultAlternativeConcernTableData
from RGT.gridMng.template.session.participatingSessionsContentGridsData import ParticipatingSessionsContentGridsData
from RGT.gridMng.template.session.resultRatingWeightTableData import ResultRatingWeightTableData
from RGT.gridMng.template.session.resultRatingWeightTablesData import ResultRatingWeightTablesData
from RGT.gridMng.template.session.participantsData import ParticipantsData
from RGT.gridMng.template.gridTableData import GridTableData
from RGT.gridMng.template.session.pedingResponsesData import PedingResponsesData
from RGT.gridMng.fileData import FileData
from RGT.gridMng.utility import generateGridTable, createDendogram, getImageError
from RGT.settings import SESSION_USID_KEY_LENGTH

import uuid
import sys
import traceback
from types import StringType
from datetime import datetime

def ajaxGetCreateSessionPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    user1= request.user
    grids= user1.grid_set.all()

    if len(grids) <= 0:
        grids= None
    
    templateData= CreateSessionData(grids)
    
    context= RequestContext(request, {'data': templateData})

    return render(request, 'gridMng/createSession.html', context_instance = context);

def getMySessionsPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    try:
        facilitator1= Facilitator.objects.isFacilitator(request.user)
        if facilitator1:
            sessions= Session.objects.filter(facilitator= facilitator1)
            if sessions and len(sessions) > 0:
                sessionList= []
                for session in sessions:
                    sessionList.append((session.name, session.usid))
                    #print session.name + ' ' + str(session.usid)

                templateData= MySessionsData(sessionList)
                context= RequestContext(request, {'data': templateData})

                return render(request, 'gridMng/mySessions.html', context_instance=context)
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

    context= RequestContext(request, {})
    return render(request, 'gridMng/mySessions.html', context_instance=context)

def ajaxGetMySessionContentPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    sessionObj= None
    try:
        if request.POST.has_key('sessionUSID'):
            try:
                facilitator1= Facilitator.objects.isFacilitator(request.user)
                if facilitator1:
                    sessionObj= Session.objects.get(usid= request.POST['sessionUSID'], facilitator= facilitator1)
                    #get the users
                    #participants= sessionObj.getParticipators()
                    
                    templateData= MySessionsContentData()
                    templateData.participantTableData= ParticipantsData(__createPaticipantPanelData__(sessionObj))
                    iteration= sessionObj.iteration
                    sessionGrid= sessionObj.sessiongrid_set.all()[iteration].grid
                    gridTemplateData= GridTableData(generateGridTable(sessionGrid))
                    gridTemplateData.tableId= randomStringGenerator()
                    gridTemplateData.usid= sessionGrid.usid
                    templateData.tableData= gridTemplateData
                    iterationValueType = {}
                    iterationTypes = SessionIterationState.objects.filter(session=sessionObj)
                    i= 0;
                    # -1 because the last iteration is the one currently on, which does not
                    # produce any results anyway
                    while i <= iteration-1:
                        if i == 0:
                            iterationValueType[i] = {'':'','':''}
                        else:
                            if iterationTypes[i-1].state.name == SessionState.AC:
                                iterationValueType[i] = {'stateNameKey':SessionState.AC, 'stateName':'Alternatives and Concerns'}
                            elif iterationTypes[i-1].state.name == SessionState.RW:
                                iterationValueType[i] = {'stateNameKey':SessionState.RW, 'stateName':'Ratings and Weights'}
                        i+= 1
                        #hidden.append(( str(len(dic['table'])), 'nConcerns'))
                    #hidden.append(( str(len(dic['table'][0]) - 2), 'nAlternatives'))
                    
                    templateData.iterationValueType= iterationValueType
                    templateData.sessionName= sessionObj.name
                    templateData.iteration= iteration
                    templateData.invitationKey= sessionObj.invitationKey
                    
                    template= loader.get_template('gridMng/mySessionsContent.html')
                    context= None
                    #now lets see what we have to return
                    if sessionObj.state.name == SessionState.INITIAL:
                        templateData.state= 'Invitation'
                        gridTemplateData.showRatingWhileFalseChangeRatingsWeights= True

                    elif sessionObj.state.name == SessionState.AC:
                        templateData.state= 'A/C'
                        templateData.hasSessionStarted= True
                        templateData.showFinishButton= True
                        gridTemplateData.showRatingWhileFalseChangeRatingsWeights= True

                    elif sessionObj.state.name == SessionState.RW:
                        templateData.state= 'R/W'
                        templateData.hasSessionStarted= True
                        templateData.showFinishButton= True
                        gridTemplateData.showRatingWhileFalseChangeRatingsWeights= True

                    elif sessionObj.state.name == SessionState.FINISH:
                        templateData.state= 'Closed'
                        templateData.isSessionClose= True
                        templateData.hasSessionStarted= True
                        gridTemplateData.showRatingWhileFalseChangeRatingsWeights= True

                    elif sessionObj.state.name == SessionState.CHECK:
                        templateData.state= 'Check Values'
                        templateData.hasSessionStarted= True
                        templateData.showRequestButtons= True
                        templateData.showCloseSessionButton= True
                        templateData.savaGridSession= True
                        gridTemplateData.changeRatingsWeights= True
                        gridTemplateData.changeCornAlt= True
                        gridTemplateData.checkForTableIsSave= True
                        
                    context= RequestContext(request, {'data': templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    #return render_to_response('gridMng/mySessionsContent.html', {'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'showRatings':True, 'readOnly':True}, context_instance=RequestContext(request))
                else:
                    return HttpResponse(createXmlErrorResponse('You are not the facilitator for this session'), content_type='application/xml')
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                return HttpResponse(createXmlErrorResponse('No session found'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('No session id found in the request'), content_type='application/xml')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('unknown error'), content_type='application/xml')

def ajaxCreateSession(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    if request.method == 'POST':
        user1= request.user
        gridUSID= request.POST['gridUSID']
        gridObj= None
        hasError= False
        errorMsg= ''
        sessionGrid= None
        facilitator1= None
        newSession= None
        showResults= False
        sessionGridName= 'untitled' #default name
        try:
            gridObj= Grid.objects.get(user= user1, usid= gridUSID)
            if request.POST.has_key('sessionName'):
                temp= request.POST['sessionName']
                result = validateName(temp)
                if type(result) == StringType:
                    sessionGridName= result
                else:
                    return result

            if request.POST.has_key('showResults'):
                temp1= request.POST['showResults']
                result1 = validateName(temp1)
                if type(result1) == StringType:
                    if result1 == 'Y':
                        showResults= True
                    else:
                        showResults= False
                else:
                    return result1
        except:
            hasError= True
            errorMsg= 'grid was not found'
        if gridObj:
            try:
                # now lets create a new session with a copy of the current grid
                facilitator1= Facilitator.objects.isFacilitator(user1)
                print facilitator1
                #create the facilitator if it doesn't exist in the facilitator table
                if not facilitator1:
                    facilitator1= Facilitator.objects.create(user= user1)
                    #now copy the grid
                try:
                    state1= State.objects.getInitialState()
                    newSession= Session.objects.create(usid=randomStringGenerator(SESSION_USID_KEY_LENGTH), facilitator= facilitator1, iteration= 0, name= sessionGridName, showResult= showResults, state= state1, invitationKey= str(uuid.uuid4()))
                    try:
                        sessionGrid= Grid.objects.duplicateGrid(gridObj, gridType= Grid.GridType.SESSION_GRID)
                        if sessionGrid:
                            try:
                                SessionGrid.objects.create(session= newSession, grid= sessionGrid, iteration= 0)
                                return HttpResponse(createXmlSuccessResponse('Session was created.'), content_type='application/xml')
                            except:
                                newSession.delete()
                                hasError= True
                                errorMsg= 'unable to relate the grid with the session'
                                print "Exception in user code:"
                                print '-'*60
                                traceback.print_exc(file=sys.stdout)
                                print '-'*60
                    except:
                        try:
                            newSession.delete()
                        except:
                            print 'Could\'t delete the session'
                        hasError= True
                        errorMsg= 'unable to copy the grid to the session'
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                except:
                    hasError= True
                    errorMsg= 'unable to create the session'
                    print "Exception in user code:"
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
            except:
                hasError= True
                errorMsg= 'unable to create or set the facilitator for the session'
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
        if hasError:
            try:
                #revert changes
                newSession.delete()
                sessionGrid.delete()
            except:
                #do nothing
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
            return HttpResponse(createXmlErrorResponse(errorMsg), content_type='application/xml')
        return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
    return ajaxGetCreateSessionPage(request)

def getParticipatingSessionsPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    sessions= []
    templateDate= ParticipatingSessionsData()
    for userParticipateSession in request.user.userparticipatesession_set.all():
        sessions.append((userParticipateSession.session.usid, userParticipateSession.session.facilitator.user.first_name + ':' + userParticipateSession.session.name))
    if len(sessions) > 0:
        templateDate.hasSessions= True
    
    templateDate.sessions= sessions
    pendingResponses= PedingResponsesData()
    pendingResponses.pedingResponsesTable= __createPendingResponseData__(request.user)
    templateDate.pendingResponses= pendingResponses

    context= RequestContext(request, {'data': templateDate})
    return render(request, 'gridMng/participatingSessions.html', context)

def ajaxJoinSession(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    user1= request.user
    invitationKey1= None
    error= None
    if request.POST.has_key('invitationKey'):
        invitationKey1= request.POST['invitationKey']
    else:
        error= 'no invitation key was received'
    if not error:
        try:
            session= Session.objects.filter(invitationKey= invitationKey1)
            if len(session) > 0:
                session[0].addParticipant(user1)
                data= {};
                data[session[0].usid]= session[0].facilitator.user.first_name + ':' + session[0].name
                return HttpResponse(createXmlSuccessResponse('You have been added as participant in session: "' + session[0].name + '".', createXmlForComboBox(data)), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('Session does not exist'), content_type='application/xml')
        except UserAlreadyParticipating:
            return HttpResponse(createXmlErrorResponse('You are already participating in the session'), content_type='application/xml')
        except WrongState:
            return HttpResponse(createXmlErrorResponse('Can\'t join session as it is passed \'initial\' state'), content_type='application/xml')
        except UserIsFacilitator:
            return HttpResponse(createXmlErrorResponse('You are the facilitator of the session, facilitators can\'t be added as participants'), content_type='application/xml')
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse(error), content_type='application/xml')

def ajaxChangeSessionState(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    if request.POST.has_key('sessionUSID') and request.POST.has_key('newState'):
        facilitatorObj= request.user.facilitator_set.all()
        if len(facilitatorObj) >= 1:
            facilitatorObj= facilitatorObj[0]
            session= facilitatorObj.session_set.filter(usid= request.POST['sessionUSID'])
            if len(session) >= 1:
                try:
                    session= session[0]
                    name= request.POST['newState']
                    stateObj= State.objects.filter(name= request.POST['newState'])
                    if len(stateObj) >= 1:
                        stateObj= stateObj[0]
                        if name == 'finish':
                            
                            try:
                                __saveSessionGridAsUserGrid__(request) 
                            except:
                                print "Exception in user code:"
                                print '-'*60
                                traceback.print_exc(file=sys.stdout)
                                print '-'*60
                                print 'Could not save session grid as user grid'
                        session.changeState(stateObj)
                        return ajaxGetMySessionContentPage(request)
                    else:
                        return HttpResponse(createXmlErrorResponse('Invalid state given in the request'), content_type='application/xml')
                except WrongState:
                    print "Exception in user code:"
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    return HttpResponse(createXmlErrorResponse('Can\'t change states, session is in the wrong state'), content_type='application/xml')
                except:
                    print "Exception in user code:"
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('Session not found'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('You are not a facilitator for the session, can\'t change states.'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing arguments'), content_type='application/xml')

def ajaxGetParticipatingSessionContentPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    if request.method == 'POST':
        if request.POST.has_key('sessionUSID'):
            sessionID = Session.objects.get(usid=request.POST['sessionUSID'])
            sessionObj= request.user.userparticipatesession_set.filter(session=sessionID)
            if len(sessionObj) >= 1:
                sessionObj= sessionObj[0].session
                state= sessionObj.state
                iteration= sessionObj.iteration
                iterations= []
                hasPreviousResponseRelationGrid= False
                templateData= ParticipatingSessionsContentData()
                templateData.iteration= iteration
                templateData.responseStatus= '-----'
                
                #lets create a list of iteration that i have responded
                responseGridRelations= ResponseGrid.objects.filter(session= sessionObj, user= request.user)
                gridTablesData= __generateParticipatingSessionsGridsData__(sessionObj, iteration, responseGridRelations)
                if len(responseGridRelations) >= 1:
                    for responseGridRelation in responseGridRelations:
                        iterations.append(responseGridRelation.iteration)
                templateData.iterations= iterations
                if state.name == SessionState.CHECK:
                    templateData.hideSaveResponseButton= True
                    templateData.sessionStatus= 'Checking previous results'
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'data': templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.INITIAL:
                    templateData.hideSaveResponseButton= True
                    templateData.sessionStatus= 'Waiting for users to join'
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'data': templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.FINISH:
                    templateData.hideSaveResponseButton= True
                    templateData.sessionStatus= 'Closed'
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'data': templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    
                    templateParticipatingSessions= ParticipatingSessionsContentGridsData()
                    templateData.participatingSessionsContentGridsData= templateParticipatingSessions
                    #there always is a session table being displayed to the user, so add this table in here
                    templateParticipatingSessions.displaySessionGrid= True
                    templateParticipatingSessions.sessionGridData= GridTableData(gridTablesData['sessionGridTable'])
                    templateParticipatingSessions.sessionGridData.tableId= randomStringGenerator()
                    templateParticipatingSessions.sessionGridData.doesNotShowLegend= True
                    #check to see if there is a response table, if so add it
                    if gridTablesData.has_key('currentResponseGridTable'):
                        templateParticipatingSessions.responseGridData= GridTableData(gridTablesData['currentResponseGridTable'])
                    else:
                        #if there is no response display a table with the data as seem in the session grid
                        templateParticipatingSessions.responseGridData= GridTableData(gridTablesData['sessionGridTable'])
                        #the weights need to be duplicated in a new object as  the list will be poped later on
                        templateParticipatingSessions.responseGridData.weights= templateParticipatingSessions.sessionGridData.weights[:] 
                    templateParticipatingSessions.responseGridData.tableId= randomStringGenerator()
                    templateParticipatingSessions.displayResponseGrid= True
                    #if the gridTablesData contains a previous response table add it
                    if gridTablesData.has_key('previousResponseGrid'):
                        templateParticipatingSessions.previousResponseGridData= GridTableData(gridTablesData['previousResponseGrid'])
                        templateParticipatingSessions.previousResponseGridData.tableId= randomStringGenerator()
                        templateParticipatingSessions.previousResponseGridData.doesNotShowLegend= True
                        hasPreviousResponseRelationGrid= True
                        templateParticipatingSessions.displayPreviousResponseGrid= True
                    
                    #calculate how many participants there are in this session and how many have sent a response
                    templateData.nReceivedResponses= 0
                    templateData.nParticipants= 0
                    templateData.showNParticipantsAndResponces= True
                    try:
                        templateData.nReceivedResponses= len(sessionObj.getUsersThatRespondedRequest())
                        templateData.nParticipants= len(sessionObj.getParticipators())
                    except:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        #check if i have sent a response grid
                    responseGrid= request.user.responsegrid_set.filter(user= request.user, iteration= iteration, session=sessionObj)
                    if len(responseGrid) <= 0:
                        #i didn't respond, so display a page with the correct settings to answer it
                        templateData.responseStatus= 'No response was sent'
                        if state.name == SessionState.AC:
                            #first get the current session grid to display to the user
                            templateParticipatingSessions.responseGridData.changeCornAlt= True
                            templateParticipatingSessions.responseGridData.doesNotShowLegend= True
                            templateData.sessionStatus= 'Waiting for Alternative and concerns'
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'data': templateData})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        elif state.name == SessionState.RW:
                            templateData.sessionStatus= 'Waiting for Ratings and Weights'
                            templateParticipatingSessions.sessionGridData.showRatingWhileFalseChangeRatingsWeights= True
                            templateParticipatingSessions.responseGridData.changeRatingsWeights= True
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            if hasPreviousResponseRelationGrid == True:
                                templateParticipatingSessions.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights= True
                                
                            context= RequestContext(request, {'data': templateData})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        #if i did respond show me my response and the current session grid so if i changed my mind i still can change the response
                        templateData.responseStatus= 'Response was sent at: '
                        templateData.dateTime= responseGrid[0].grid.dateTime
                        if state.name == SessionState.AC:
                            templateParticipatingSessions.responseGridData.changeCornAlt= True
                            templateData.sessionStatus= 'Waiting for Alternative and concerns'
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'data': templateData})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        elif state.name == SessionState.RW:
                            templateParticipatingSessions.sessionGridData.showRatingWhileFalseChangeRatingsWeights= True
                            templateParticipatingSessions.responseGridData.changeRatingsWeights= True
                            templateData.sessionStatus= 'Waiting for Ratings and Weights'
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            if hasPreviousResponseRelationGrid == True:
                                templateParticipatingSessions.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights= True
                                
                            context= RequestContext(request, {'data': templateData})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    return HttpResponse(createXmlErrorResponse('Unable to identify current session state'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('You are not participating in the given session'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing arguments'), content_type='application/xml')
    return getParticipatingSessionsPage(request)

#this function will determine if we are creating a new response grid or updating an old one
def ajaxRespond(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
        #check inputs
    userObj= request.user
    nConcerns= None
    nAlternatives= None
    concernValues= None
    alternativeValues= None
    ratioValues= None
    if request.POST.has_key('sessionUSID') and request.POST.has_key('gridType') and request.POST.has_key('iteration'):
        #check if user can answer to the session
        sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
        if len(sessionObj) >= 1:
            sessionObj= sessionObj[0]
            userSessionRelation= userObj.userparticipatesession_set.filter(session= sessionObj)
            if len(userSessionRelation) >= 1:
                sessionIteration= int(request.POST['iteration'])
                #check if the session is in a state where it is allowed to send a response
                if sessionIteration == sessionObj.iteration:
                    userResponseGridRelation= userObj.responsegrid_set.filter(iteration= sessionIteration, session= sessionObj)

                    #if the response is for a concern/alternative request, run extra validation code (no empty concerns or alternatives allowed)
                    if sessionObj.state.name == State.objects.getWaitingForAltAndConState().name:
                        try:
                            __validateAltConResponse__(request)
                        except ValueError as error:
                            print "Exception in user code:"
                            print '-'*60
                            traceback.print_exc(file=sys.stdout)
                            print '-'*60
                            return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
                        except KeyError as error:
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
                            #determine if it is a new response grid or not
                    if len(userResponseGridRelation) >= 1:
                        #this is an update
                        gridObj= userResponseGridRelation[0].grid
                        isConcernAlternativeResponseGrid= False;
                        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                            isConcernAlternativeResponseGrid= True
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
                            #return ajaxUpdateGrid(request)
                    else:
                        #this is a new grid, which means first response
                        gridType= None
                        showRatings= True
                        isConcernAlternativeResponseGrid= False
                        #discover the response grid type
                        if sessionObj.state.name == SessionState.AC:
                            gridType= Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN
                            showRatings= False
                            isConcernAlternativeResponseGrid= True
                        elif sessionObj.state.name == SessionState.RW:
                            gridType= Grid.GridType.RESPONSE_GRID_RATING_WEIGHT
                        obj= None
                        #validate and retrieve the data that is going to be used in the grid
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
                        try:
                            #set the relation ship of the response grid with the session
                            gridObj= createGrid(userObj, gridType, None, nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, showRatings)
                            gridResponseRelation= ResponseGrid(grid= gridObj, session= sessionObj, iteration= sessionIteration, user= userObj)
                            gridResponseRelation.save()

                            extraXmlData= createXmlNumberOfResponseNode(len(sessionObj.getUsersThatRespondedRequest()) + 1)
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
                            print "Exception in user code:"
                            print '-'*60
                            traceback.print_exc(file=sys.stdout)
                            print '-'*60
                            return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse('Can\'t create response grid, session is in a state where that is not permitted'), content_type='application/xml')
                    #return ajaxCreateGrid(request, createXmlNumberOfResponseNode(len(sessionObj.getUsersThatRespondedRequest()) + 1))
            else:
                return HttpResponse(createXmlErrorResponse('You are not participating in the session, can\'t send response grid'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('Session was not found'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing arguments'), content_type='application/xml')

#this function only return the content grids!!
def ajaxGetParticipatingSessionsContentGrids(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    try:
        #check for the mandatory keys
        if request.POST.has_key('iteration') and request.POST.has_key('sessionUSID'):
            sessionObj= Session.objects.filter(usid=request.POST['sessionUSID'])
            if len(sessionObj) >= 1:
                templateData= ParticipatingSessionsContentGridsData()
                templateData.displaySessionGrid= True 
                templateData.displayResponseGrid= True
                iteration_= int(request.POST['iteration'])
                sessionObj= sessionObj[0]
                hasPreviousResponseRelationGrid= False
                #check if the iteration is valid
                if iteration_ > sessionObj.iteration or iteration_ < 0:
                    return HttpResponse(createXmlErrorResponse('Invalid iteration value'), content_type='application/xml')
                gridTablesData=  __generateParticipatingSessionsGridsData__(sessionObj, iteration_, ResponseGrid.objects.filter(session= sessionObj, user= request.user))
                
                #there is always a session grid, so add it
                templateData.sessionGridData= GridTableData(gridTablesData['sessionGridTable'])
                templateData.sessionGridData.tableId= randomStringGenerator()
                templateData.sessionGridData.doesNotShowLegend= True
                templateData.displaySessionGrid= True
                #if the user sent a response display that grid
                if gridTablesData.has_key('currentResponseGridTable'):
                    templateData.responseGridData= GridTableData(gridTablesData['currentResponseGridTable'])
                else:
                    #if he hasn't sent a response display a grid with the values of the session grid
                    templateData.responseGridData= GridTableData(gridTablesData['sessionGridTable'])
                    #the weights need to be in a new object as we will pop it later (in the template)
                    templateData.responseGridData.weights= templateData.responseGridData.weights[:]
                templateData.responseGridData.tableId= randomStringGenerator()
                templateData.displayResponseGrid= True
                #if the gridTablesData contains a previous response table add it
                if gridTablesData.has_key('previousResponseGrid'):
                    templateData.previousResponseGridData= GridTableData(gridTablesData['previousResponseGrid'])
                    templateData.previousResponseGridData.tableId= randomStringGenerator()
                    templateData.previousResponseGridData.doesNotShowLegend= True
                    hasPreviousResponseRelationGrid= True
                    templateData.displayPreviousResponseGrid= True
                
                if len(request.user.userparticipatesession_set.filter(session= sessionObj)) >= 1:
                    responseGridRelation= ResponseGrid.objects.filter(session= sessionObj, iteration= iteration_, user= request.user)
                    #check to see if the user has already send an response grid
                    if len(responseGridRelation) >= 1:
                        #if he has sent an response grid display it again and let him edit it
 
                        responseGridRelation= responseGridRelation[0]
                        template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                        context= None
                        if responseGridRelation.grid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                            templateData.responseGridData.doesNotShowLegend= True
                            #check to see if the user should be allowed to change the response
                            if iteration_ == sessionObj.iteration:
                                templateData.responseGridData.changeCornAlt= True
                        else:
                            #check to see if the user should be allowed to change the response
                            templateData.sessionGridData.showRatingWhileFalseChangeRatingsWeights= True
                            templateData.responseGridData.showRatingWhileFalseChangeRatingsWeights= True
                            if iteration_ == sessionObj.iteration:
                                templateData.responseGridData.changeRatingsWeights= True
                                #if the previous response grid is displayed make sure it is displayed correctly
                                if hasPreviousResponseRelationGrid == True:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights= True
                            else:
                                #if the previous response grid is displayed make sure it is displayed correctly
                                if hasPreviousResponseRelationGrid == True:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights= True
                                    
                                    
                        context= RequestContext(request, {'data': templateData})
                        htmlData= template.render(context)
                        return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        #if he hasn't send a response grid check to see if he still can send it and if so display it
                        if iteration_ == sessionObj.iteration:
                            if sessionObj.state.name == SessionState.AC:
                                template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                context= None
                                templateData.responseGridData.changeCornAlt= True
                                templateData.responseGridData.doesNotShowLegend= True
                                
                                context= RequestContext(request, {'data': templateData})
                                htmlData= template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            
                            elif sessionObj.state.name == SessionState.RW:
                                template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                context= None
                                templateData.sessionGridData.showRatingWhileFalseChangeRatingsWeights= True
                                templateData.responseGridData.changeRatingsWeights= True
                                if hasPreviousResponseRelationGrid == True:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights= True
                                
                                context= RequestContext(request, {'data': templateData})
                                htmlData= template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            else:
                                return HttpResponse(createXmlSuccessResponse('<div id="participatinSessionsMessageDiv"><p>Session is in a state where no grids are available</p></div>'), content_type='application/xml')
                        else:
                            return HttpResponse(createXmlErrorResponse('No response found for the session in iteration ' + request.POST['iteration']))
                else:
                    return HttpResponse(createXmlErrorResponse('You are not participating in the session'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('Can\'t find session'), content_type='application/xml')
                #sessionObj= request.user.userparticipatesession_set.filter()
        else:
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
 
# function is to get the session results for the facilitator for completed iterations
def ajaxGetResults(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        request_= request
        if not (request.POST.has_key('sessionUSID') and request.POST.has_key('iteration')):
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')
        else:
            facilitatorObj= None
            if len(request.user.facilitator_set.all()) < 1:
                return HttpResponse(createXmlErrorResponse('You are not a facilitator for this session'), content_type='application/xml')
            else:
                facilitatorObj= request.user.facilitator_set.all()[0]
                sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
                if len(sessionObj) < 1:
                    return HttpResponse(createXmlErrorResponse('Couldn\'t find session'), content_type='application/xml')
                else:
                    session_= sessionObj[0]
                    if session_.facilitator != facilitatorObj:
                        return HttpResponse(createXmlErrorResponse('You are not a facilitator for this session'), content_type='application/xml')
                    else:
                        iteration_= int(request.POST['iteration'])
                        try:
                            templateData= __generateSessionIterationResult__(request_, session_, iteration_)
                            if templateData != None:
                                template= None
                                if type(templateData) == ResultRatingWeightTablesData:
                                    template= loader.get_template('gridMng/resultRatingWeightTables.html')
                                elif type(templateData) == ResultAlternativeConcernTableData:
                                    template= loader.get_template('gridMng/resultAlternativeConcernTable.html')
                                context= RequestContext(request, {'data': templateData})
                                htmlData= template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            else:
                                return HttpResponse(createXmlErrorResponse('No results found. This means that the participants of this session did not provide any responses for this particular iteration.'), content_type='application/xml')
                        except WrongGridType:
                            return HttpResponse(createXmlErrorResponse('Unexpected type grid found'), content_type='application/xml')
                        except WrongSessionIteration:
                            return HttpResponse(createXmlErrorResponse('Session does not contain that iteration'), content_type='application/xml')
                        except:
                            return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml') 
                        #return ajaxGenerateResultsData(request_, session_, iteration_)
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')

# function is to get the session results for the participants for completed iterations
def ajaxGetResponseResults(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        request_= request
        if not (request.POST.has_key('sessionUSID') and request.POST.has_key('iteration')):
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')
        else:
            sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
            if len(sessionObj) < 1:
                return HttpResponse(createXmlErrorResponse('Couldn\'t find session'), content_type='application/xml')
            else:
                session_= sessionObj[0]
                showResultsYes= True
                if session_.showResult != showResultsYes:
                    return HttpResponse(createXmlErrorResponse('Results are not available for the Participants'), content_type='application/xml')
                else:
                    iteration_= int(request.POST['iteration'])
                    try:
                        templateData= __generateSessionIterationResult__(request_, session_, iteration_)
                        if templateData != None:
                            template= None
                            if type(templateData) == ResultRatingWeightTablesData:
                                template= loader.get_template('gridMng/resultRatingWeightTables.html')
                            elif type(templateData) == ResultAlternativeConcernTableData:
                                template= loader.get_template('gridMng/resultAlternativeConcernTable.html')
                            context= RequestContext(request, {'data': templateData})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        else:
                            return HttpResponse(createXmlErrorResponse('No results found. This means that the participants of this session did not provide any responses for this particular iteration.'), content_type='application/xml')
                    except WrongGridType:
                        return HttpResponse(createXmlErrorResponse('Unexpected type grid found'), content_type='application/xml')
                    except WrongSessionIteration:
                        return HttpResponse(createXmlErrorResponse('Session does not contain that iteration'), content_type='application/xml')
                    except:
                        return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')
                    #return ajaxGenerateResultsData(request_, session_, iteration_)
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return HttpResponse(createXmlErrorResponse('Unknown error'), content_type='application/xml')

#download the results from a session in the form of an image
def ajaxDonwloandSessionResults(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    
    try:
        if not request.POST.has_key('sessionUSID') or not request.POST.has_key('iteration'):
            if not request.POST.has_key('sessionUSID'):
                raise Exception('sessionUSID key was not received')
            else:
                raise Exception('iteration key was not received')
        else:
            facilitatorObj= None
            if len(request.user.facilitator_set.all()) < 1:
                raise Exception('User is not a facilitator for a session')
            else:
                facilitatorObj= request.user.facilitator_set.all()[0]
                sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
                if len(sessionObj) < 1:
                    raise Exception('Couldn\'t find session: ' + request.POST['sessionUSID'])
                else:
                    session_= sessionObj[0]
                    if session_.facilitator != facilitatorObj:
                        raise Exception('User is  not a facilitator for session ' + request.POST['sessionUSID'])
                    else:
                        iteration_= int(request.POST['iteration'])
                        templateData= __generateSessionIterationResult__(request, session_, iteration_)
                        #check which type of response it is and convert the data so a svg can be created
                        responseGridRelation= session_.responsegrid_set.filter(iteration= iteration_)
                        if len(responseGridRelation) >= 1:
                            gridType= responseGridRelation[0].grid.grid_type
                            if gridType == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                                imgData= FileData()
                                convertToData= request.POST['convertTo']
                                if convertToData == 'svg':
                                    imgData.data=  convertAlternativeConcernSessionResultToSvg(templateData)
                                    imgData.fileExtention= 'svg'
                                    imgData.ContentType= 'image/svg+xml'
                                
                                if request.POST.has_key('fileName'):
                                    imgData.fileName= request.POST['fileName']
                                    
                                    if not imgData.fileName:
                                        imgData.fileName= randomStringGenerator()
                                    
                                return createFileResponse(imgData)
                            else:
                                rangeData= SessionResultImageConvertionData()
                                meanData= SessionResultImageConvertionData()
                                stdData= SessionResultImageConvertionData()
                                
                                #the header object is shared among all the 3 tables
                                templateData.rangeData.headers.append('weight')
                                #templateData.rangeData.headers.insert(0, '')
                                #templateData.rangeData.headers.append('')
                                
                                #range
                                rangeData.tableHeader= templateData.rangeData.headers
                                sizeWeights= len(templateData.rangeData.weights)
                                i= 0
                                temp= templateData.rangeData.table
                                finalTable= []
                                concerns= []
                                
                                i= 0
                                j= 0
                                
                                while i < len(temp):
                                    row= []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], temp[i][j + 1][1]))
                                        j+= 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j= 0
                                    i+= 1
                                
                                i= 0    
                                while i < sizeWeights:
                                    finalTable[i].append((templateData.rangeData.weights[i][0], templateData.rangeData.weightColorMap[i]))
                                    i+= 1
                                
                                rangeData.tableData= finalTable
                                rangeData.header= templateData.rangeData.tableHead
                                rangeData.concerns= concerns
                                
                                #mean
                                meanData.tableHeader= templateData.meanData.headers
                                #meanData.tableHeader.append('weight')
                                finalTable= []
                                concerns= []
                                sizeWeights= len(templateData.meanData.weights)
                                i= 0
                                temp= templateData.meanData.table

                                i= 0
                                j= 0
                                
                                while i < len(temp):
                                    row= []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], None))
                                        j+= 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j= 0
                                    i+= 1
                                
                                i= 0    
                                while i < sizeWeights:
                                    finalTable[i].append((templateData.meanData.weights[i][0], None))
                                    i+= 1
                                
                                meanData.tableData= finalTable
                                meanData.header= templateData.meanData.tableHead
                                meanData.concerns= concerns
                                
                                #std
                                finalTable= []
                                concerns= []
                                stdData.tableHeader= templateData.stdData.headers
                                sizeWeights= len(templateData.stdData.weights)
                                i= 0
                                temp= templateData.stdData.table
                                
                                i= 0
                                j= 0
                                
                                while i < len(temp):
                                    row= []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], temp[i][j + 1][1]))
                                        j+= 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j= 0
                                    i+= 1
                                
                                i= 0    
                                while i < sizeWeights:
                                    finalTable[i].append((templateData.stdData.weights[i][0], templateData.stdData.weightColorMap[i]))
                                    i+= 1
                                
                                stdData.tableData= finalTable
                                stdData.header= templateData.stdData.tableHead
                                stdData.concerns= concerns
                                
                                imgData= FileData()
                                convertToData= request.POST['convertTo']
                                if convertToData == 'svg':
                                    imgData.data=  convertRatingWeightSessionResultToSvg(meanData, rangeData, stdData)
                                    imgData.fileExtention= 'svg'
                                    imgData.ContentType= 'image/svg+xml'
                                
                                if request.POST.has_key('fileName'):
                                    imgData.fileName= request.POST['fileName']
                                    
                                    if not imgData.fileName:
                                        imgData.fileName= randomStringGenerator()
                                    
                                return createFileResponse(imgData)
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

#function that will get the page that display the participants of a session
def ajaxGetParticipatingPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        #check if the mandatory variables are present
        if request.POST.has_key('sessionUSID'):
            #get the session
            sessionObj= Session.objects.get(usid= request.POST['sessionUSID'])
            if sessionObj != None:
                #sessionObj= sessionObj[0]
                #check if the user is a facilitator and if he is the facilitator for this session
                facilitatorObj= request.user.facilitator_set.all()
                if len(facilitatorObj) >= 1 and sessionObj.facilitator == facilitatorObj[0]:
                    #get all the users that reponded to the request
                    templateData= ParticipantsData()
                    templateData.participants= __createPaticipantPanelData__(sessionObj)
                    template= loader.get_template('gridMng/participants.html')
                    context= RequestContext(request, {'data':templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse('Can\'t complete request, you are not a facilitator for this session'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('Session does not exist'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

def ajaxGenerateSessionDendrogram(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    #check if all the mandatory keys are present
    if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
        #check to see if the user is a facilitator
        try:
            facilitatorObj= Facilitator.objects.filter(user= request.user)
            if len(facilitatorObj) >= 1:
                facilitatorObj= facilitatorObj[0]
                #find the session
                sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'], facilitator= facilitatorObj)
                if len(sessionObj) >= 1:
                    sessionObj= sessionObj[0]
                    iterationObj= int(request.POST['iteration'])
                    #display the current iteration if there was no iteration specified
                    if iterationObj < 0:
                        iterationObj= sessionObj.iteration
                    sessionGridRelation= SessionGrid.objects.filter(session= sessionObj, iteration= iterationObj)
                    if len(sessionGridRelation) >= 1:
                        sessionGridRelation= sessionGridRelation[0]
                        try:
                            imgData= createDendogram(sessionGridRelation.grid)
                            responseData= createSvgResponse(imgData, createXmlGridIdNode(sessionGridRelation.grid.usid))
                            return HttpResponse(responseData, content_type='application/xml')
                        except Exception:
                            print "Exception in user code:"
                            print '-'*60
                            traceback.print_exc(file=sys.stdout)
                            print '-'*60
                            return HttpResponse(createXmlErrorResponse('Unknown dendrogram error'), content_type='application/xml')
                    else:
                        return HttpResponse(createXmlErrorResponse('No grid found for the selected iteration'), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse('Session was not found'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('You are not a facilitator'), content_type='application/xml')
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')

def ajaxGetSessionGrid(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    #check if all the mandatory keys are present
    if request.POST.has_key('sessionUSID'):
        #check if the user is an facilitator
        facilitatorObj= request.user.facilitator_set.all()
        if len(facilitatorObj) >= 1:
            facilitatorObj= facilitatorObj[0]
            #check if the session exists
            sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'], facilitator= facilitatorObj)
            if len(sessionObj) >= 1:
                sessionObj= sessionObj[0]
                #check if the grid exists
                gridObj= SessionGrid.objects.filter(session= sessionObj, iteration= sessionObj.iteration)
                if len(gridObj) >= 1:
                    gridObj= gridObj[0].grid
                    templateData= GridTableData(generateGridTable(gridObj))
                    templateData.tableId= randomStringGenerator()
                    templateData.usid= gridObj.usid
                    #if the state is not check then return a table where nothing can be changed, else return a table that can be changed
                    if sessionObj.state.name == State.objects.getCheckState().name:
                        templateData.changeRatingsWeights= True
                        templateData.changeCornAlt= True
                        templateData.checkForTableIsSave= True
                    template= loader.get_template('gridMng/gridTable.html')
                    context= RequestContext(request, {'data':templateData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')                        
                else:
                    return HttpResponse(createXmlErrorResponse('Grid not found'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('Session was not found'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('You are not a facilitator'), content_type='application/xml')
    else:
        return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml')

def test(request):
    return render_to_response('gridMng/createGrid.html', {}, context_instance=RequestContext(request))

def __calcutateMeans__(ratioMatrices= None):

    if ratioMatrices == None or ratioMatrices[0] == None or ratioMatrices[0][0] == None:
        return None

    #find out the dimensions of the ratio matrix
    nMatrixs= len(ratioMatrices)
    nCols= len(ratioMatrices[0][0])
    nRows= len(ratioMatrices[0])
    nAvailableAnswers= 0 # used to see how many ratios are numbers in the same cell over multible ratio matrixes
    totalRatio= 0
    temp= None
    meanMatrix= []
    i= 0
    j= 0
    k= 0
    while i < nRows:
        tempRow= []
        while j < nCols:
            while k < nMatrixs:
                temp= ratioMatrices[k][i][j]
                #calculate the total ratio between all the cell in the same position of all the reponse grids
                if temp != None:
                    totalRatio+= temp
                    nAvailableAnswers+= 1
                k+= 1
            k= 0
            j+= 1
            #calculate the mean
            tempRow.append(float("{0:.2f}".format(totalRatio/nAvailableAnswers)))
            totalRatio= 0
            nAvailableAnswers= 0
        j= 0
        i+= 1
        meanMatrix.append(tempRow)
    i= 0
    return meanMatrix

def __calculateRange__(ratioMatrices= None):

    if ratioMatrices == None or ratioMatrices[0] == None or ratioMatrices[0][0] == None:
        return None

    nMatrixs= len(ratioMatrices)
    nCols= len(ratioMatrices[0][0])
    nRows= len(ratioMatrices[0])
    globalMin= None
    globalMax= None
    temp= None
    rangeMatrix= []
    i= 0
    j= 0
    k= 0
    while i < nRows:
        tempRow= []
        while j < nCols:
            while k < nMatrixs:
                temp= ratioMatrices[k][i][j]
                if temp != None:
                    #if this is the first cell set the max and min to what is found in the ration matrix
                    if globalMin == None:
                        globalMin= temp
                        globalMax= temp
                    else:
                        if temp > globalMax:
                            globalMax= temp
                        if temp < globalMin:
                            globalMin= temp
                k+= 1
            k= 0
            j+= 1
            tempRow.append(globalMax - globalMin)
            globalMax= None
            globalMin= None
        j= 0
        i+= 1
        rangeMatrix.append(tempRow)
    i= 0
    return rangeMatrix

def __calculateStandardDeviation__(ratioMatrices= None, meanMatrix= None):

    if ratioMatrices == None or ratioMatrices[0] == None or ratioMatrices[0][0] == None or meanMatrix == None:
        return None

    nMatrixs= len(ratioMatrices)
    nCols= len(ratioMatrices[0][0])
    nRows= len(ratioMatrices[0])
    temp= None
    tempMean= 0
    stdMatrix= []
    nAvailableAnswers= 0
    total= 0
    i= 0
    j= 0
    k= 0
    while i < nRows:
        tempRow= []
        while j < nCols:
            tempMean= meanMatrix[i][j]
            while k < nMatrixs:
                temp= ratioMatrices[k][i][j]
                if temp != None:
                    temp-= tempMean
                    temp= temp**2
                    total+= temp
                    nAvailableAnswers+= 1
                k+= 1
            k= 0
            j+= 1
            tempRow.append(float("{0:.2f}".format(sqrt(total/nAvailableAnswers))))
            temp= None
            total= 0
            nAvailableAnswers= 0
        j= 0
        i+= 1
        stdMatrix.append(tempRow)
    i= 0

    return stdMatrix

def __findMinMaxInMatrix__(matrix= None):

    if matrix == None or matrix[0] == None:
        return None

    nRows= len(matrix)
    nCols= len(matrix[0])
    minValue= None
    maxValue= None
    temp= None

    i= 0
    j= 0

    while i < nRows:
        while j < nCols:
            temp= matrix[i][j]
            if minValue == None:
                minValue= temp
                maxValue= temp
            else:
                if temp > maxValue:
                    maxValue= temp
                if temp < minValue:
                    minValue= temp
            j+= 1
        j= 0
        i+= 1
    i= 0

    return (minValue, maxValue)

def __createJSforRatioWeightSessionResultsChart__(ratioMatrices= None, weightMatrices= None, participantNames= None):

    if ratioMatrices == None or weightMatrices == None:
        return None
        #create the data for the javascript. format should be a string --> [[name,value], [name,value], ....., [name,value]].
    javascriptRatioData= [] #format should be [[cell with js string data], [cell with js string data], ...]
    javascriptWeightData= [] #format should be [[cell with js string data], [cell with js string data], ...]
    i= 0
    j= 0
    k= 0
    temp= None
    nConcerns= len(ratioMatrices[0])
    nResponseGrids= len(ratioMatrices) - 1
    nAlternatives= len(ratioMatrices[0][0])

    #first create the table for the weights
    while i < nConcerns:
        temp= '['
        temp+= '[\'session\','
        tempWeight= weightMatrices[0][0][i]
        #first element is always what is in the session grid
        if tempWeight != None and tempWeight >= 1:
            temp+= str(tempWeight) + ']'
        else:
            temp+= '0]'
            #now add all other elements
        j= 0
        while j < nResponseGrids:
            tempWeight= weightMatrices[j + 1][0][i] #j+1 because the session grid weights are in position 0
            if tempWeight != None and tempWeight >= 1:
                temp+= ',[\'' + participantNames[j] + '\',' + str(tempWeight) + ']'
            else:
                temp+= ',[\'' + participantNames[j] + '\',0]'
            j+= 1
        temp+= ']'
        javascriptWeightData.append(temp)
        i+= 1
    i= 0
    #now create the table for the ratios
    while i < nConcerns:
        row= []
        while k < nAlternatives:
            temp= '['
            j= 0
            #first element is always what is in the session grid
            temp+= '[\'session\','
            tempRating= ratioMatrices[0][i][k]
            if tempRating != None and tempRating >= 1:
                temp+= str(tempRating) + ']'
            else:
                temp+= '0]'
                #now add all other elements
            while j < nResponseGrids:
                tempRating= ratioMatrices[j + 1][i][k] #j+1 because the session grid ratios are in position 0
                if tempRating != None and tempRating >= 1:
                    temp+= ',[\'' + participantNames[j] + '\',' + str(tempRating) + ']'
                else:
                    temp+= ',[\'' + participantNames[j] + '\',0]'
                j+= 1
            temp+= ']'
            row.append(temp)
            k+= 1
        k= 0
        javascriptRatioData.append(row)
        i+= 1
    i= 0

    return (javascriptRatioData, javascriptWeightData)



# data is a list of ResponseGrid objs
def __generateAlternativeConcernResultTable__(data=[], sessionGridObj= None):
    concernsResult= [] #obj that will be returned with the concerns as following: (leftconcern, right concern, nPair, nLeftConcern, nRightConcern, isNew)
    alternativeResult= [] #obj that will be returned with the alternative as following: (alternative, nTime, isNew)
    oldConcernsPair= []
    oldAlternatives= []
    concerns= {}
    concernPairs= {} #key is a tulp value is the number the pair is present together
    alternatives= {}
    temp= None

    #first find all the existing pairs of concerns
    if sessionGridObj != None:
        for concern in sessionGridObj.concerns_set.all():
            lConcern= concern.leftPole
            rConcern= concern.rightPole
            if lConcern == None and rConcern == None:
                pass
            else:
                if lConcern == None:
                    lConcern= ""
                if rConcern == None:
                    rConcern= ""
                oldConcernsPair.append((lConcern.lower(), rConcern.lower()))

        for alternative in sessionGridObj.alternatives_set.all():
            oldAlternatives.append(alternative.name.lower())

    for relation in data:
        grid= relation.grid
        for concern in grid.concerns_set.all():
            if concern.leftPole:
                temp= concern.leftPole.lower()
                if not concerns.has_key(temp):
                    concerns[temp]= 1
                else:
                    concerns[temp]= concerns[temp] + 1
            if concern.rightPole:
                temp= concern.rightPole.lower()
                if not concerns.has_key(temp):
                    concerns[temp]= 1
                else:
                    concerns[temp]= concerns[temp] + 1
            if concernPairs.has_key((concern.leftPole.lower(), concern.rightPole.lower())):
                concernPairs[(concern.leftPole.lower(), concern.rightPole.lower())]+= 1
            else:
                concernPairs[(concern.leftPole.lower(), concern.rightPole.lower())]= 1

        for alternative in grid.alternatives_set.all():
            if alternative:
                temp= alternative.name.lower()
                if not alternatives.has_key(temp):
                    alternatives[temp]= 1
                else:
                    alternatives[temp]= alternatives[temp] + 1
                    #create an array that contains the tulip (leftconcern, right concern, nPair, nLeftConcern, nRightConcern, isNew), where nPair is the number of times the pair is found, isNew determines if the pair was present in the session grid or not
    for key, value in concernPairs.items():
        leftC, rightC= key
        #check if this pair already exist in the main session grid
        if (leftC, rightC) in oldConcernsPair:
            concernsResult.append((leftC, rightC, value, concerns[leftC], concerns[rightC], False))
        else:
            concernsResult.append((leftC, rightC, value, concerns[leftC], concerns[rightC], True))
            #create an tulip: (anternative, nTimes, isNew) where nTimes is the amount of times each alternative is cited; isNew tells if the alternative was present in the session grid
    for key, value in alternatives.items():
        if key in oldAlternatives:
            alternativeResult.append((key, value, False))
        else:
            alternativeResult.append((key, value, True))

    return (concernsResult, alternativeResult)


def __createRangeTableColorMap__(globalMax, globalMin, rangeTable):

    #end color
    colorEnd= (255, 255, 255)

    #start color
    colorStart= (240, 72, 74)

    #part of the old code (used with the old ajaxGetResults function)
    #maxRange= globalMax - globalMin

    return __createColorMap__(100, globalMax, colorStart, colorEnd, rangeTable)

def __createStdTableColorMap__(globalMax, globalMin, stdTable):
    #end color
    colorEnd= (255, 255, 255)

    #start color
    colorStart= (240, 72, 74)

    #part of the old code (used with the old ajaxGetResults function)
    #mean= (globalMax + globalMin)/2
    #maxStd= sqrt(((globalMax - mean)**2 + (globalMin - mean)**2)/2)


    return __createColorMap__(100, globalMax, colorStart, colorEnd, stdTable)

def __createColorMap__(colorStep, maxValue, startColor, endColor, table):
    #code from http://www.designchemical.com/blog/index.php/jquery/jquery-tutorial-create-a-flexible-data-heat-map/
    yr, yg, yb= startColor
    xr, xg, xb= endColor
    colorMap= []
    for row in table:
        colorRow= []
        pos= None
        if type(row) == type([]):
            for value in row:
                if maxValue != 0:
                    if maxValue <= value:
                        colorRow.append(startColor)
                    else:
                        pos= ceil((value/maxValue)*100)
                        red = ceil((xr + (( pos * (yr - xr)) / (colorStep-1))))
                        green = ceil((xg + (( pos * (yg - xg)) / (colorStep-1))))
                        blue = ceil((xb + (( pos * (yb - xb)) / (colorStep-1))))
                        colorRow.append((int(red), int(green), int(blue)))
                else:
                    colorRow.append(endColor)
            colorMap.append(colorRow)
        else:
            if maxValue != 0:
                if maxValue <= row:
                    colorMap.append(startColor)
                else:
                    pos= ceil((row/maxValue)*100)
                    red = ceil((xr + (( pos * (yr - xr)) / (colorStep-1))))
                    green = ceil((xg + (( pos * (yg - xg)) / (colorStep-1))))
                    blue = ceil((xb + (( pos * (yb - xb)) / (colorStep-1))))
                    colorMap.append((int(red), int(green), int(blue)))
            else:
                colorMap.append(endColor)
    return colorMap

#this function is used to create the data tha is used in the participants.html page
def __createPaticipantPanelData__(sessionObj):
    usersAndDateTimes = sessionObj.getUsersThatRespondedRequest()
    participantData= []
    for user in sessionObj.getParticipators():
        #create the list with the user and the class of the css the should be coupled with the user in the html template
        #but first check if the session is in a state where there is no data that can be requested or responded
        if sessionObj.state.name == SessionState.FINISH or sessionObj.state.name == SessionState.INITIAL or sessionObj.state.name == SessionState.CHECK:
            participantData.append((user, 'respondedRequest'))
        else:
            users = []
            dateTimes = []
            for i in range(len(usersAndDateTimes)):
                users.append(usersAndDateTimes[i]['user'])
                dateTimes.append(usersAndDateTimes[i]['dateTime'])
            if user in users:
                j = users.index(user)
                participantData.append((user, 'respondedRequest', dateTimes[j]))
            else:
                participantData.append((user, 'didNotRespondedRequest'))
    return participantData

def __createPendingResponseData__(userObj= None):
    table= None

    if userObj != None:
        #find out all the sessions that the user is part of
        userSessionRelation= UserParticipateSession.objects.filter(user= userObj)
        if len(userSessionRelation) >= 1:
            for relation in userSessionRelation:
                #now lets check if the session is in a state where a response grid is required
                sessionObj= relation.session
                if sessionObj.state.name == State.objects.getWaitingForAltAndConState().name or sessionObj.state.name == State.objects.getWaitingForWeightsAndRatingsState().name:
                    #now that we know the session is in the correct state lets check if the user has responded.
                    if len(ResponseGrid.objects.filter(user= userObj, session= sessionObj, iteration= sessionObj.iteration)) <= 0:
                        if table == None:
                            table= []
                        table.append((sessionObj.name + ' : ' + sessionObj.facilitator.user.first_name, sessionObj.usid))
    return table

def __validateAltConResponse__(request):

    #general validation
    if request.POST.has_key('nAlternatives') and request.POST.has_key('nConcerns'):
        nAlternatives= int(request.POST['nAlternatives'])
        nConcerns= int(request.POST['nConcerns'])

        i= 0
        #check the concern if they are empty or not
        while i < nConcerns:
            #check left pole
            keyName= 'concern_'+ str((i + 1)) + '_left'
            if request.POST.has_key(keyName):
                if request.POST[keyName] == None or request.POST[keyName].strip() == '':
                    #print 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"'
                    raise ValueError('One or more concerns are empty', 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"')
            else:
                #print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)', 'Error request is missing argument: ' + keyName)

            #check right pole
            keyName= 'concern_'+ str((i + 1)) + '_right'
            if request.POST.has_key(keyName):
                if request.POST[keyName] == None or request.POST[keyName].strip() == '':
                    #print 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"'
                    raise ValueError('One or more concerns are empty', 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"')
            else:
                #print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)', 'Error request is missing argument: ' + keyName)
            i+= 1;

        i= 0;
        #validate the alternatives
        while i < nAlternatives:
            keyName= 'alternative_' + str((i + 1)) + '_name'
            if request.POST.has_key(keyName):
                if request.POST[keyName] == None or request.POST[keyName].strip() == '':
                    #print 'Error alternative ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"'
                    raise ValueError('One or more alternatives are empty', 'Error alternative ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"')
            else:
                #print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)', 'Error request is missing argument: ' + keyName)
            i+= 1
        return True
    else:
        #print 'Error request is missing arguments: nAlternatives: ' + str(request.POST.has_key('nAlternatives')) + ' nConcerns: ' + str(request.POST.has_key('nConcerns'))
        raise KeyError('Invalid request, request is missing argument(s)', 'Error request is missing arguments: nAlternatives: ' + str(request.POST.has_key('nAlternatives')) + ' nConcerns: ' + str(request.POST.has_key('nConcerns')))

def __isGridStateEqualSessionState__(sesssionState, gridObj):
    
    if sesssionState.name == SessionState.AC:
        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
            return True
    elif sesssionState.name == SessionState.RW:
        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT:
            return True
    return False

#This function will generate the data that is needed for the participatingSessionsContentGrids.html template
#returns a dictionary that MAY contain the following keys:  previousResponseGrid, sessionGridTable, currentResponseGridTable
def __generateParticipatingSessionsGridsData__(sessionObj, iteration_, responseGridRelation):
    data= {}
    currentResponseGridRelation= responseGridRelation.filter(iteration= iteration_)
    
    #a session grid must always be present, if something goes wrong here the calling function should deal with it
    data['sessionGridTable']= generateGridTable(sessionObj.sessiongrid_set.all()[iteration_].grid)
    
    #check to see if a previous response grid should be displayed or not
    if iteration_ >= 2 and iteration_ - 1 > 0:
        previousResponseGridRelation= responseGridRelation.filter(iteration= iteration_ - 1)
        previousResponseGrid= None
        if len(previousResponseGridRelation) >= 1:
            previousResponseGrid=  previousResponseGridRelation[0].grid
            if previousResponseGrid != None and __isGridStateEqualSessionState__(sessionObj.state, previousResponseGrid) and (previousResponseGrid.grid_type == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT or previousResponseGrid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN):
                #generate the data for the previous response grid
                data['previousResponseGrid']= generateGridTable(previousResponseGridRelation[0].grid)
            
    #generate response grid data
    #check to see if the user has already send a response grid
    if len(currentResponseGridRelation) >= 1:
        #if he has sent an response generate the data for the grid
        data['currentResponseGridTable']= generateGridTable(currentResponseGridRelation[0].grid)
    
    return data

# function saves session grid as user grid. This happens only when the facilitator click "end session" button
# to make the creation of session possible from the session that previously completed
def __saveSessionGridAsUserGrid__(request):

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
            gridType= Grid.GridType.USER_GRID
            userObj= request.user
            gridName= 'None'
            if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
                facilitatorObj= Facilitator.objects.isFacilitator(request.user)
                if facilitatorObj :
                    session= facilitatorObj.session_set.filter(usid= request.POST['sessionUSID'])
                    if len(session) >= 1:
                        session= session[0]
                        gridName= 'Session_' + session.name
                        sessionGridRelation= session.sessiongrid_set.filter(iteration= request.POST['iteration'])
                        if len(sessionGridRelation) >= 1:
                            gridObj= sessionGridRelation[0].grid
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        elif gridType == 'response':
            return False
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
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return False
    nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues= obj

    #update the grid
    if gridObj != None:
        try:
            isGridCreated= createGrid(userObj ,gridType, gridName, nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues, True)
            if isGridCreated:
                return True
        except:
            return False
    else:
        return False

#this function will generate the data for the ResultRatingWeightTablesData or ResultAlternativeConcernTableData template data objects
#this function also returns one of those objects depending on the type of requested the results will be based on.
#if no results were found none is returned
def __generateSessionIterationResult__(request, sessionObj, iterationObj):
    if sessionObj.iteration < iterationObj:
        raise WrongSessionIteration('Session does not contain that iteration')
    
    #let's find all the response grids
    responseGridRelation= sessionObj.responsegrid_set.filter(iteration= iterationObj)
    if len(responseGridRelation) >= 1:
        gridType= responseGridRelation[0].grid.grid_type
        if gridType == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
            try:
                #check to see if we have a sesssion grid for the iteration
                templateData= ResultAlternativeConcernTableData()
                sessionGrid= SessionGrid.objects.filter(session= sessionObj, iteration= iterationObj)
                if len(sessionGrid) >= 1:
                    sessionGrid= sessionGrid[0].grid
                    templateData.concerns, templateData.alternatives= __generateAlternativeConcernResultTable__(responseGridRelation, sessionGrid)
                else:
                    templateData.concerns, templateData.alternatives= __generateAlternativeConcernResultTable__(responseGridRelation)
                if len(templateData.concerns) >= 1:
                    #template= loader.get_template('gridMng/resultAlternativeConcernTable.html')
                    #context= RequestContext(request, {'data': templateData})
                    #htmlData= template.render(context)
                    return templateData
                    #return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    return None
                    #return HttpResponse(createXmlErrorResponse('No results found. This means that the participants did not provide any responses for this particular iteration.'), content_type='application/xml')
            except Exception as e:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                raise e
                #return HttpResponse(createXmlErrorResponse('Unknown Error'), content_type='application/xml')
        elif gridType == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT:
            #create a list with a matrix of ratios in each position of the list.
            ratioMatrices= []
            weightMatrices= []
            tempMatrix= []
            tempRatioRow= None
            tempWeightRow= None

            #first lets add the rations that are in the session grid to the list
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            concerns= sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.concerns_set.all()
            alternatives= sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.alternatives_set.all()
            nConcerns= len(concerns)
            nAlternatives= len(alternatives)
            nResponseGrids= len(responseGridRelation)

            i= 0
            j= 0
            tempWeightRow= []
            while i < nConcerns:
                tempRatioRow= []
                tempWeightRow.append(concerns[i].weight)
                while j < nAlternatives:
                    tempRatioRow.append(Ratings.objects.get(concern= concerns[i], alternative= alternatives[j]).rating)
                    j+= 1
                tempMatrix.append(tempRatioRow)
                j= 0
                i+= 1
            i= 0
            ratioMatrices.append(tempMatrix)
            weightMatrices.append([tempWeightRow])
            tempMatrix= []
            tempWeightRow= []
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            #now lets do the same for the response grids
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            i= 0
            j= 0
            k= 0
            tempWeightRow= []

            while i < nResponseGrids:
                respGrid= responseGridRelation[i].grid
                concerns= respGrid.concerns_set.all()
                alternatives= respGrid.alternatives_set.all()
                nConcerns= len(concerns)
                nAlternatives= len(alternatives)
                while j < nConcerns:
                    tempRatioRow= []
                    tempWeightRow.append(concerns[j].weight)
                    while k < nAlternatives:
                        tempRatioRow.append(Ratings.objects.get(concern= concerns[j], alternative= alternatives[k]).rating)
                        k+= 1
                    k= 0
                    j+= 1
                    tempMatrix.append(tempRatioRow)
                j= 0
                i+= 1
                weightMatrices.append([tempWeightRow])
                ratioMatrices.append(tempMatrix)
                tempMatrix= []
                tempWeightRow= []
            i= 0
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            #calculate the rage, mean and std for the weight and ratio
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            meanRatioMatrix= __calcutateMeans__(ratioMatrices)
            rangeRatioMatrix= __calculateRange__(ratioMatrices)
            stdRatioMatrix= __calculateStandardDeviation__(ratioMatrices, meanRatioMatrix)
            meanWeightMatrix= __calcutateMeans__(weightMatrices)
            rangeWeightMatrix= __calculateRange__(weightMatrices)
            stdWeightMatrix= __calculateStandardDeviation__(weightMatrices, meanWeightMatrix)
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            #first lets create the header
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            header= []
            for alternative in sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.alternatives_set.all():
                header.append(alternative.name)
                #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            #generate color map
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            #minMaxRangeRatio= __findMinMaxInMatrix__(rangeRatioMatrix)
            minMaxRangeWeight= __findMinMaxInMatrix__(stdRatioMatrix)

            #minMaxStdRatio= __findMinMaxInMatrix__(rangeWeightMatrix)
            minMaxStdWeight= __findMinMaxInMatrix__(stdWeightMatrix)

            rangeRatioColorMap= __createRangeTableColorMap__(4, 0, rangeRatioMatrix) # for as the max range is 1-5= 4 (as right now the user can only use the numbers between 1 and 5)
            rangeWeightColorMap= __createRangeTableColorMap__(minMaxRangeWeight[1], 0, rangeWeightMatrix[0])
            stdRatioColorMap= __createStdTableColorMap__(4, 0, stdRatioMatrix)
            stdWeightColorMap= __createStdTableColorMap__(minMaxStdWeight[1], 0, stdWeightMatrix[0])
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<


            #generate the js for the chart in the page
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            participantNames= []
            #retrieve all the names
            while i < len(responseGridRelation):
                #the initial db didn't link a response grid to a user direcly, this has changed now, but the code needs to take care of this difference. (4/7/2012)
                if responseGridRelation[i].grid.user != None:
                    participantNames.append(responseGridRelation[i].grid.user.first_name)
                else:
                    participantNames.append(responseGridRelation[i].user.first_name)
                i+= 1
            i= 0
            ratioJsChartData, weightJsChartData= __createJSforRatioWeightSessionResultsChart__(ratioMatrices, weightMatrices, participantNames)

            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            #clue everything together now and return the page
            tableRatingRangeColor= [] #final table with the value to be displayed, the background color and js code
            tableRatingStdColor= [] #final table with the value to be displayed, the background color and js code
            tableRatingMean= [] #final table with the value to be displayed and js code
            tableWeightMean= [] #final table with the weights and js code
            tableWeightStd= [] #final table with the weights and js code
            tableWeightRange= [] #final table with the weights and js code
            i= 0

            #reverse the weight color maps, this is done because we use pop in the template!!!
            rangeWeightColorMap.reverse()
            stdWeightColorMap.reverse()

            while i < nConcerns:
                rowRange= []
                rowStd= []
                rowMean= []
                tableWeightMean.append((meanWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[i]))#meanWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                tableWeightStd.append((stdWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[i]))#stdWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                tableWeightRange.append((rangeWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[i]))#rangeWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                #create a tulip with the value that should be displayed in the td and the color of the background for each cell in the row
                while k < nAlternatives:
                    rowRange.append((rangeRatioMatrix[i][k], rangeRatioColorMap[i][k], ratioJsChartData[i][k]))
                    rowStd.append((stdRatioMatrix[i][k], stdRatioColorMap[i][k], ratioJsChartData[i][k]))
                    rowMean.append((meanRatioMatrix[i][k], ratioJsChartData[i][k]))
                    k+= 1
                k= 0
                #add the concerns to the range, mean and std tables
                rightPole= concerns[i].rightPole
                leftPole= concerns[i].leftPole
                rowStd.insert(0, (leftPole, None))
                rowStd.append((rightPole, None))
                rowMean.insert(0, (leftPole, None))
                rowMean.append((rightPole, None))
                rowRange.insert(0, (leftPole, None))
                rowRange.append((rightPole, None))
                tableRatingRangeColor.append(rowRange)
                tableRatingStdColor.append(rowStd)
                tableRatingMean.append(rowMean)
                rightPole= None
                leftPole= None
                i+= 1
            i= 0

            #put all the data into objects for the template
            rangeData= ResultRatingWeightTableData()
            meanData= ResultRatingWeightTableData()
            stdData= ResultRatingWeightTableData()

            rangeData.table= tableRatingRangeColor
            rangeData.headers= header
            rangeData.weights= tableWeightRange
            rangeData.weightColorMap= rangeWeightColorMap
            rangeData.tableHead= 'Range'
            rangeData.useColorMap= True

            meanData.table= tableRatingMean
            meanData.headers= header
            meanData.weights= tableWeightMean
            meanData.tableHead= 'Mean'

            stdData.table= tableRatingStdColor
            stdData.headers= header
            stdData.weights= tableWeightStd
            stdData.weightColorMap= stdWeightColorMap
            stdData.tableHead= 'Standard Deviation'
            stdData.useColorMap= True

            templateData= ResultRatingWeightTablesData()
            templateData.rangeData= rangeData
            templateData.meanData= meanData
            templateData.stdData= stdData

            #template= loader.get_template('gridMng/resultRatingWeightTables.html')
            #context= RequestContext(request, {'data': templateData})
            #htmlData= template.render(context)
            return templateData
            #return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
        else:
            raise WrongGridType('Unexpected type grid found')
            #return HttpResponse(createXmlErrorResponse('Unexpected type grid found'), content_type='application/xml')
    else:
        return None
        #return HttpResponse(createXmlErrorResponse('No results found. This means that the participants of this session did not provide any responses for this particular iteration.'), content_type='application/xml')

