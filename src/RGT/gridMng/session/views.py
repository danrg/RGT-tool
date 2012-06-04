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
from RGT.gridMng.error.wrongState import  WrongState
from RGT.gridMng.error.userIsFacilitator import  UserIsFacilitator
from RGT.gridMng.views import __generateGridTable__, __createDendogram__
from RGT.gridMng.utility import createXmlErrorResponse, createXmlSuccessResponse, randomStringGenerator, createXmlForComboBox, validateName, createXmlForNumberOfResponseSent
from RGT.gridMng.views import ajaxUpdateGrid, ajaxCreateGrid
from math import sqrt, ceil
import uuid
import sys
import traceback
from types import StringType

def ajaxGetCreateSessionPage(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')

    user1= request.user
    grids= user1.grid_set.all()

    if len(grids) <= 0:
        grids= None

    context= RequestContext(request, {'grids' : grids})

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

                context= RequestContext(request, {'sessions':sessionList})

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
                    participants= __createPaticipantPanelData__(sessionObj)
                    hidden= []
                    iteration= sessionObj.iteration
                    dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                    iterationValues= []
                    iterationValueType = {}
                    iterationTypes = SessionIterationState.objects.filter(session=sessionObj)
                    i= 0;
                    # -1 because the last iteration is the one currently on, which does not
                    # produce any results anyway
                    while i <= iteration-1:
                        iterationValues.append(i)
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

                    template= loader.get_template('gridMng/mySessionsContent.html')
                    context= None
                    #now lets see what we have to return
                    if sessionObj.state.name == SessionState.INITIAL:
                        context= RequestContext(request, {'sessionName':sessionObj.name, 'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'changeRatingsWeights':False, 'changeCornAlt':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'hasSessionStarted':False, 'showRequestButtons':False , 'showFinishButton':False, 'showCloseSessionButton':False, 'state':'Invitation', 'iterationValues':iterationValues, 'tableId':randomStringGenerator(), 'iterationValueType':iterationValueType})
                        
                    elif sessionObj.state.name == SessionState.AC:
                        context= RequestContext(request, {'sessionName':sessionObj.name, 'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'changeRatingsWeights':False, 'changeCornAlt':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'hasSessionStarted':True, 'showRequestButtons':False, 'showFinishButton':True, 'showCloseSessionButton':False, 'state':'A/C', 'iterationValues':iterationValues, 'tableId':randomStringGenerator(), 'iterationValueType':iterationValueType})
                    
                    elif sessionObj.state.name == SessionState.RW:
                        context= RequestContext(request, {'sessionName':sessionObj.name, 'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'changeRatingsWeights':False, 'changeCornAlt':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'hasSessionStarted':True, 'showRequestButtons':False, 'showFinishButton':True, 'showCloseSessionButton':False, 'state':'R/W', 'iterationValues':iterationValues, 'tableId':randomStringGenerator(), 'iterationValueType':iterationValueType})
                        
                    elif sessionObj.state.name == SessionState.FINISH:
                        context= RequestContext(request, {'sessionName':sessionObj.name, 'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'changeRatingsWeights':False, 'changeCornAlt':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'hasSessionStarted':True, 'showRequestButtons':False, 'showFinishButton':False, 'showCloseSessionButton':False, 'state':'Closed', 'iterationValues':iterationValues, 'isSessionClose':True, 'tableId':randomStringGenerator(), 'iterationValueType':iterationValueType})
                    
                    elif sessionObj.state.name == SessionState.CHECK:
                        context= RequestContext(request, {'sessionName':sessionObj.name, 'participants':participants, 'iteration': iteration, 'invitationKey': sessionObj.invitationKey, 'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'hiddenFields':hidden, 'changeRatingsWeights':True, 'changeCornAlt':True, 'hasSessionStarted':True, 'state':'Check Values', 'iterationValues':iterationValues, 'showRequestButtons':True, 'showFinishButton':False, 'showCloseSessionButton':True, 'checkForTableIsSave':True ,'savaGridSession':True, 'tableId':randomStringGenerator(), 'iterationValueType':iterationValueType})
                    
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
                    newSession= Session.objects.create(usid=randomStringGenerator(20), facilitator= facilitator1, iteration= 0, name= sessionGridName, state= state1, invitationKey= str(uuid.uuid4()))
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
    hasSessions= True
    for userParticipateSession in request.user.userparticipatesession_set.all():
        sessions.append((userParticipateSession.session.usid, userParticipateSession.session.facilitator.user.first_name + ':' + userParticipateSession.session.name))
    if len(sessions) <= 0:
        hasSessions= False
    
    pendingResponsesTable=  __createPendingResponseData__(request.user)
    if pendingResponsesTable != None:
        context= RequestContext(request, {'sessions':sessions, 'hasSessions':hasSessions, 'pedingResponsesTable':pendingResponsesTable})
    else:
        context= RequestContext(request, {'sessions':sessions, 'hasSessions':hasSessions})
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
                    stateObj= State.objects.filter(name= request.POST['newState'])
                    if len(stateObj) >= 1:
                        stateObj= stateObj[0]   
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
                #lets create a list of iteration that i have responded
                responseGridRelations= ResponseGrid.objects.filter(session= sessionObj, user= request.user)
                if len(responseGridRelations) >= 1:
                    for responseGridRelation in responseGridRelations:
                        iterations.append(responseGridRelation.iteration)
                if state.name == SessionState.CHECK:
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'displaySessionGrid': False, 'displayResponseGrid': False, 'sessionStatus':'Checking previous results', 'responseStatus':'-----', 'sessionStatusClass':'green', 'responseStatusClass':'green', 'iteration':iteration, 'iterations':iterations})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.INITIAL:
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'displaySessionGrid': False, 'displayResponseGrid': False, 'sessionStatus':'Waiting for users to join', 'responseStatus':'-----', 'sessionStatusClass':'green', 'responseStatusClass':'green', 'iteration':iteration, 'iterations':iterations})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.FINISH:
                    template= loader.get_template('gridMng/participatingSessionsContent.html')
                    context= RequestContext(request, {'displaySessionGrid': False, 'displayResponseGrid': False, 'sessionStatus':'Closed', 'responseStatus':'-----', 'sessionStatusClass':'red', 'responseStatusClass':'green', 'iteration':iteration, 'iterations':iterations})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    #calculate how many participants there are in this session and how many have sent a response
                    nResponses= 0
                    nParticipants= 0
                    try:
                        nResponses= len(sessionObj.getUsersThatRespondedRequest())
                        nParticipants= len(sessionObj.getParticipators())
                    except:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60 
                    #check if i have sent a response grid
                    responseGrid= request.user.responsegrid_set.filter(user= request.user, iteration= iteration, session=sessionObj)
                    if len(responseGrid) <= 0:
                        #i didn't respond, so display a page with the correct settings to answer it
                        if state.name == SessionState.AC:
                            #first get the current session grid to display to the user
                            dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'showRatingWhileFalseChangeRatingsWeights':False, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Alternative and concerns', 'responseStatus':'No response was sent', 'sessionStatusClass':'green', 'responseStatusClass':'red', 'iteration':iteration, 'iterations':iterations, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                              'responseTable': dic['table'], 'responseTableHeader':dic['tableHeader'], 'responseWeights':dic['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':True, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator(), 'nParticipants':nParticipants, 'nReceivedResponses':nResponses, 'showNParticipantsAndResponces': True, 'responseDoesNotShowLegend': True})
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        elif state.name == SessionState.RW:
                            dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'][:], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Ratings and Weights', 'responseStatus':'No response was sent', 'sessionStatusClass':'green', 'responseStatusClass':'red', 'iteration':iteration, 'iterations':iterations, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                                  'responseTable': dic['table'], 'responseTableHeader':dic['tableHeader'], 'responseWeights':dic['weights'], 'responseChangeRatingsWeights':True, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator(), 'nParticipants':nParticipants, 'nReceivedResponses':nResponses, 'showNParticipantsAndResponces': True })
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        #if i did respond show me my response and the current session grid so if i changed my mind i still can change the response
                        if state.name == SessionState.AC:
                            dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                            dic2= __generateGridTable__(responseGrid[0].grid)
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Alternative and concerns', 'responseStatus':'Response was sent at: ', 'responseWasSent':True, 'sessionStatusClass':'green', 'responseStatusClass':'green', 'iteration':iteration, 'iterations':iterations, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':True, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator(), 'dateTime':responseGrid[0].grid.dateTime, 'nParticipants':nParticipants, 'nReceivedResponses':nResponses, 'showNParticipantsAndResponces': True, 'responseDoesNotShowLegend': True })
                            htmlData= template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')    
                        elif state.name == SessionState.RW:
                            dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                            dic2= __generateGridTable__(responseGrid[0].grid)
                            template= loader.get_template('gridMng/participatingSessionsContent.html')
                            context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'showRatingWhileFalseChangeRatingsWeights':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Ratings and Weights', 'responseStatus':'Response was sent at: ', 'responseWasSent':True, 'sessionStatusClass':'green', 'responseStatusClass':'green', 'iteration':iteration, 'iterations':iterations, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':True, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator(), 'dateTime':responseGrid[0].grid.dateTime, 'nParticipants':nParticipants, 'nReceivedResponses':nResponses, 'showNParticipantsAndResponces': True })
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
    if request.POST.has_key('sessionUSID') and request.POST.has_key('gridType') and request.POST.has_key('iteration'):
        #check if user can answer to the session
        sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
        if len(sessionObj) >= 1:
            sessionObj= sessionObj[0]
            userSessionRelation= userObj.userparticipatesession_set.filter(session= sessionObj)
            if len(userSessionRelation) >= 1:
                #determine if it is a new response grid or not
                userResponseGridRelation= userObj.responsegrid_set.filter(iteration= int(request.POST['iteration']), session= sessionObj)
                #if the response is for a concern/alternative request, run extra validation code (no empty concerns or alternatives allowed)
                if sessionObj.state.name == State.objects.getWaitingForAltAndConState().name:
                    try:
                        __validateAltConResponse__(request)
                    except ValueError as error:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60 
                        return HttpResponse(createXmlErrorResponse(error.args[0]))
                    except KeyError as error:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60 
                        return HttpResponse(createXmlErrorResponse(error.args[0]))
                    except:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60 
                        return HttpResponse(createXmlErrorResponse('Unknown error'))
                if len(userResponseGridRelation) >= 1:
                    #this is an update
                    try:
                        return ajaxUpdateGrid(request)
                    except:
                        print "Exception in user code:"
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60 
                else:
                    #this is a new grid, which means first response
                    return ajaxCreateGrid(request, createXmlForNumberOfResponseSent(len(sessionObj.getUsersThatRespondedRequest()) + 1))
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
                sessionObj= sessionObj[0]
                iteration= int(request.POST['iteration'])
                if len(request.user.userparticipatesession_set.filter(session= sessionObj)) >= 1:
                    responseGridRelation= ResponseGrid.objects.filter(session= sessionObj, iteration= iteration, user= request.user)
                    #check to see if the user has already send an response grid
                    if len(responseGridRelation) >= 1:
                        #if he has sent an response grid display it again and let him edit it
                        responseGridRelation= responseGridRelation[0]
                        dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                        dic2= __generateGridTable__(responseGridRelation.grid)
                        template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                        context= None
                        if responseGridRelation.grid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                            if iteration == sessionObj.iteration:
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'displaySessionGrid': True, 'displayResponseGrid': True, 'hideSaveResponseButton':True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':True, 'responseCheckForTableIsSave':False, 'responseShowRatingWhileFalseChangeRatingsWeights':False, 'responseTableId':randomStringGenerator(), 'responseDoesNotShowLegend': True })
                            else:
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'displaySessionGrid': True, 'displayResponseGrid': True, 'hideSaveResponseButton':True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseShowRatingWhileFalseChangeRatingsWeights':False, 'responseTableId':randomStringGenerator(), 'responseDoesNotShowLegend': True }) 
                        else:
                            if iteration == sessionObj.iteration:
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'showRatingWhileFalseChangeRatingsWeights':True, 'tableId':randomStringGenerator(), 'displaySessionGrid': True, 'displayResponseGrid': True, 'hideSaveResponseButton':True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':True, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseShowRatingWhileFalseChangeRatingsWeights':True, 'responseTableId':randomStringGenerator()})
                            else:
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'displaySessionGrid':True, 'showRatingWhileFalseChangeRatingsWeights':True, 'tableId':randomStringGenerator(), 'displaySessionGrid': True, 'displayResponseGrid': True, 'hideSaveResponseButton':True, 'doesNotShowLegend': True,
                                                              'responseTable': dic2['table'], 'responseTableHeader':dic2['tableHeader'], 'responseWeights':dic2['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseShowRatingWhileFalseChangeRatingsWeights':True, 'responseTableId':randomStringGenerator()})
                        htmlData= template.render(context)
                        return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        #if he hasn't send a response grid check to see if he still can send it and if so display it
                        if iteration == sessionObj.iteration:
                            if sessionObj.state.name == SessionState.AC:
                                dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                                template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                context= None
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'showRatingWhileFalseChangeRatingsWeights':False, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Alternative and concerns', 'responseStatus':'No response was sent', 'sessionStatusClass':'green', 'responseStatusClass':'red', 'iteration':iteration, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                          'responseTable': dic['table'], 'responseTableHeader':dic['tableHeader'], 'responseWeights':dic['weights'], 'responseChangeRatingsWeights':False, 'responseChangeCornAlt':True, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator(), 'responseDoesNotShowLegend': True })
                                htmlData= template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            elif sessionObj.state.name == SessionState.RW:
                                dic= __generateGridTable__(sessionObj.sessiongrid_set.all()[iteration].grid)
                                template= loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                context= None
                                context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'][:], 'changeRatingsWeights':False, 'changeCornAlt':False, 'checkForTableIsSave':False, 'showRatingWhileFalseChangeRatingsWeights':True, 'displaySessionGrid':True, 'tableId':randomStringGenerator(), 'sessionStatus':'Waiting for Ratings and Weights', 'responseStatus':'No response was sent', 'sessionStatusClass':'green', 'responseStatusClass':'red', 'iteration':iteration, 'displaySessionGrid': True, 'displayResponseGrid': True, 'doesNotShowLegend': True,
                                                              'responseTable': dic['table'], 'responseTableHeader':dic['tableHeader'], 'responseWeights':dic['weights'], 'responseChangeRatingsWeights':True, 'responseChangeCornAlt':False, 'responseCheckForTableIsSave':False, 'responseTableId':randomStringGenerator() })
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

#this function will return the page that displays the results of a iteration from a session 
def ajaxGetResults(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    try:
        if request.POST.has_key('sessionUSID') and request.POST.has_key('iteration'):
            facilitatorObj= None
            if len(request.user.facilitator_set.all()) >= 1 :
                facilitatorObj= request.user.facilitator_set.all()[0]
                sessionObj= Session.objects.filter(usid= request.POST['sessionUSID'])
                if len(sessionObj) >= 1:
                    sessionObj= sessionObj[0]
                    if sessionObj.facilitator == facilitatorObj:
                        iterationObj= int(request.POST['iteration'])
                        if sessionObj.iteration >= iterationObj:
                            #let's find all the response grids
                            responseGridRelation= sessionObj.responsegrid_set.filter(iteration= iterationObj)
                            if len(responseGridRelation) >= 1:
                                gridType= responseGridRelation[0].grid.grid_type
                                if gridType == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                                    try:
                                        #check to see if we have a sesssion grid for the iteration
                                        concerns= None
                                        alternatives= None
                                        sessionGrid= SessionGrid.objects.filter(session= sessionObj, iteration= iterationObj)
                                        if len(sessionGrid) >= 1:
                                            sessionGrid= sessionGrid[0].grid
                                            concerns, alternatives= __generateAlternativeConcernResultTable__(responseGridRelation, sessionGrid)
                                        else:
                                            concerns, alternatives= __generateAlternativeConcernResultTable__(responseGridRelation)
                                        if len(concerns) >= 1:
                                            template= loader.get_template('gridMng/resultAlternativeConcernTable.html')
                                            context= RequestContext(request, {'concerns':concerns, 'alternatives':alternatives})
                                            htmlData= template.render(context)
                                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                                        else:
                                            return HttpResponse(createXmlErrorResponse('No results found. This means that the participants did not provide any responses for this particular iteration.'), content_type='application/xml')
                                    except:
                                        print "Exception in user code:"
                                        print '-'*60
                                        traceback.print_exc(file=sys.stdout)
                                        print '-'*60
                                        return HttpResponse(createXmlErrorResponse('Unknown Error'), content_type='application/xml')
                                elif gridType == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT:
                                    stdRating, meanRating, rangeRating, stdWeight, meanWeight, rangeWeight, globalData= __generateWeightRatingResultTables__(sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid, responseGridRelation)
                                    # now that we have the results lets change the format so we can create the tables
                                    #first lets  create the header
                                    header= []
                                    for alternative in sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.alternatives_set.all():
                                        header.append(alternative.name)
                                    #now add the left and right concern pole
                                    i= 0
                                    k= 0
                                    concerns= sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.concerns_set.all()
                                    alternatives= sessionObj.sessiongrid_set.filter(iteration= iterationObj)[0].grid.alternatives_set.all()
                                    rightPole= None
                                    leftPole= None
                                    rangeColorMap= __createRangeTableColorMap__(globalData[0], globalData[1], rangeRating)
                                    rangeWeightColorMap= __createRangeTableColorMap__(globalData[2], globalData[3], rangeWeight)
                                    stdColorMap= __createStdTableColorMap__(globalData[0], globalData[1], stdRating)
                                    stdWeightColorMap= __createStdTableColorMap__(globalData[2], globalData[3], stdWeight)
                                    tableRatingRangeColor= []
                                    tableRatingStdColor= []
                                    while i < len(concerns):
                                        rowRange= []
                                        rowStd= []
                                        while k < len(alternatives):
                                            rowRange.append((rangeRating[i][k], rangeColorMap[i][k]))
                                            rowStd.append((stdRating[i][k], stdColorMap[i][k]))
                                            k+= 1
                                        k= 0
                                        rightPole= concerns[i].rightPole
                                        leftPole= concerns[i].leftPole
                                        rowStd.insert(0, (leftPole, None))
                                        rowStd.append((rightPole, None))
                                        meanRating[i].insert(0, leftPole)
                                        meanRating[i].append(rightPole)
                                        rowRange.insert(0, (leftPole, None))
                                        rowRange.append((rightPole, None))
                                        tableRatingRangeColor.append(rowRange)
                                        tableRatingStdColor.append(rowStd)
                                        rightPole= None
                                        leftPole= None
                                        i+= 1
#                                    tableWeightRangeColor= []
                                    i=0
#                                    while i < len(rangeWeight):
#                                        tableWeightRangeColor.append((rangeWeight[i], rangeWeightColorMap[i]))
#                                        i+= 1
                                    template= loader.get_template('gridMng/resultRatingWeightTables.html')
                                    context= RequestContext(request, {'rangeTable':tableRatingRangeColor, 'rangeHeaders':header, 'rangeWeights':rangeWeight, 'rangeWeightColorMap':rangeWeightColorMap, 'rangeTableHead':'Range', 'meanWeights':meanWeight, 'meanTable':meanRating, 'meanHeaders':header, 'meanTableHead':'Mean', 'stdTable':tableRatingStdColor, 'stdHeaders':header, 'stdWeights':stdWeight, 'stdWeightColorMap':stdWeightColorMap, 'stdTableHead':'Standard Deviation' })
                                    htmlData= template.render(context)
                                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                                else:
                                    return HttpResponse(createXmlErrorResponse('Unexpected type grid found'), content_type='application/xml')
                            else:
                                return HttpResponse(createXmlErrorResponse('No results found. This means that the participants of this session did not provide any responses for this particular iteration.'), content_type='application/xml')
                        else:
                            return HttpResponse(createXmlErrorResponse('Session does not contain that iteration'), content_type='application/xml')
                    else:
                        return HttpResponse(createXmlErrorResponse('You are not a facilitator for this session'), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse('Couldn\'t find session'), content_type='application/xml')
            else:
                return HttpResponse(createXmlErrorResponse('You are not a facilitator for this session'), content_type='application/xml')
        else:
            return HttpResponse(createXmlErrorResponse('Invalid request, request is missing argument(s)'), content_type='application/xml') 
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60 

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
                    participantData= __createPaticipantPanelData__(sessionObj)
                    template= loader.get_template('gridMng/participants.html')
                    context= RequestContext(request, {'participants':participantData})
                    htmlData= template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    return HttpResponse(createXmlErrorResponse('Can\'t complete  request, you are not a facilitator for this session'), content_type='application/xml')
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
                            imgData= __createDendogram__(sessionGridRelation.grid)
                            return HttpResponse(imgData, content_type='application/xml')
                        except Exception as error:
                            if len(error.args) >= 1:
                                return HttpResponse(createXmlErrorResponse(error.args[0]), content_type='application/xml')
                            else:
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
                    #if the state is not check then return a table where nothing can be changed, else return a table that can be changed
                    if sessionObj.state.name == State.objects.getCheckState().name:
                        dic= __generateGridTable__(gridObj);
                        template= loader.get_template('gridMng/gridTable.html')
                        context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'],
                                                  'changeRatingsWeights': True, 'changeCornAlt': True,
                                                  'checkForTableIsSave':True, 'tableId':randomStringGenerator() })
                        htmlData= template.render(context)
                        return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        dic= __generateGridTable__(gridObj);
                        template= loader.get_template('gridMng/gridTable.html')
                        context= RequestContext(request, {'table' : dic['table'], 'tableHeader': dic['tableHeader'], 'weights':dic['weights'],
                                                          'tableId':randomStringGenerator() })
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

# data is a list of ResponseGrid objs
def __generateAlternativeConcernResultTable__(data=[], sessionGridObj= None):
    concernsResult= [] #obj that will be returned with the concerns as following:  (leftconcern, right concern, nPair, nLeftConcern, nRightConcern, isNew)
    alternativeResult= []  #obj that will be returned with the alternative as following:  (alternative, nTime, isNew)
    oldConcernsPair= []
    oldAlternatives= []
    concerns= {}
    concernPairs= {} #key is a tulp value is the number the pair is present together
    alternatives= {}
    temp= None
    
    #first find all the existing pairs of concerns
    if sessionGridObj != None:
        for concern in sessionGridObj.concerns_set.all():
            oldConcernsPair.append((concern.leftPole.lower(), concern.rightPole.lower()))
        
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

# data is a list of ResponseGrid objs
def __generateWeightRatingResultTables__(sessionGrid=None, data=[], calculateWithWeight=False):
    nData= len(data)
    if nData >= 1:
        meanTableRating=[]
        rangeTableRating=[]
        stdTableRating=[]
        meanTableWeight=[]
        rangeTableWeight=[]
        stdTableWeight=[]
        globalMax= None; #this will be needed to calculate the color map of the table
        globalMin= None; #this will be needed to calculate the color map of the table
        globalWeightMin= None
        globalWeightMax= None
        
        sessionConcerns= sessionGrid.concerns_set.all()
        sessionAlternatives= sessionGrid.alternatives_set.all()
        nConcerns= len(data[0].grid.concerns_set.all())
        nAlternatives= len(data[0].grid.alternatives_set.all())
        i,j,k= 0, 0, 0
        
        while i < nConcerns:
            rowMean= []
            rowRange= []
            rowStd= []
            weight= None
            while j < nAlternatives:
                maxValue= None
                minValue= None
                total= 0
                population= []
                mean= 0;
                #collect the data that we will need to calculate the mean, range and std
                if sessionConcerns[i] and sessionAlternatives[j]:
                    rating= Ratings.objects.filter(concern= sessionConcerns[i], alternative= sessionAlternatives[j])
                    #get the rating of the session grid if available
                    if len(rating) >= 1:
                        rating= rating[0]
                        if rating.rating != None:
                            value= None
                            if calculateWithWeight:
                                weight= sessionConcerns[i].weight
                            if calculateWithWeight and weight != None:
                                value= rating.rating * weight
                            else:
                                value= rating.rating
                            if globalMax == None:
                                globalMax= value
                                globalMin= value
                            else:
                                if value > globalMax:
                                    globalMax= value
                                if value < globalMin:
                                    globalMin= value
                            maxValue= value
                            minValue= value
                            total+= value
                            population.append(value)
                while k < nData:
                    concernObj= data[0].grid.concerns_set.all()[i]
                    alternativeObj= data[0].grid.alternatives_set.all()[j]
                    rating= Ratings.objects.get(concern=concernObj, alternative=alternativeObj) #spyros: i do a 'get' here instead of 'filter'. why you use filter?
                    if calculateWithWeight:
                        weight= concernObj.weight
                    #check if we have a min and max value in the begin, if not set it now
                    if maxValue == None:
                        value= 0
                        if calculateWithWeight and weight != None:
                            value= rating.rating * weight
                        else:
                            maxValue= rating.rating
                        if globalMax == None:
                                globalMax= value
                                globalMin= value
                        else:
                            if value > globalMax:
                                globalMax= value
                            if value < globalMin:
                                globalMin= value
                        maxValue= value
                        minValue= value
                        total+= value
                        population.append(value)  
                    else:
                        #if len(rating) >= 1:
                        #rating= rating[0]
                        if rating.rating != None:
                            value= None
                            if calculateWithWeight and weight != None:
                                value= rating.rating * weight
                            else:
                                value= rating.rating
                            if maxValue < value:
                                maxValue= value
                            if minValue > value:
                                minValue= value
                            if globalMax == None:
                                globalMax= value
                                globalMin= value
                            else:
                                if value > globalMax:
                                    globalMax= value
                                if value < globalMin:
                                    globalMin= value
                            total+= value
                            population.append(value)
                    k+= 1
                if len(population) > 0:
                    #now that we have the data lets first calculate the range
                    rowRange.append(maxValue - minValue)
                    #calculate the mean
                    mean= total/len(population)
                    rowMean.append( float("{0:.3f}".format(mean)))
                    #calculate std
                    total= 0
                    for value in population:
                        total+= (value - mean)**2
                    rowStd.append( float("{0:.3f}".format(round(sqrt(total/len(population)), 1))))
                    k= 0
                    j+= 1
                else:
                    rowRange.append(None)
                    rowMean.append(None)
                    rowStd.append(None)
            stdTableRating.append(rowStd)
            meanTableRating.append(rowMean)
            rangeTableRating.append(rowRange)
            j= 0
            i+= 1
        i= 0
        k= 0
        #lets do the same to the weights
        while i < nConcerns:
            maxValue= None
            minValue= None
            total= 0
            population= []
            mean= 0;
            if sessionConcerns[i]:
                if sessionConcerns[i].weight:
                    maxValue= sessionConcerns[i].weight
                    minValue= sessionConcerns[i].weight
                    if globalWeightMax == None:
                        globalWeightMax= sessionConcerns[i].weight
                        globalWeightMin= sessionConcerns[i].weight
            while k < nData:
                if maxValue == None:
                    weight= data[k].grid.concerns_set.all()[i].weight
                    if weight != None:
                        if globalWeightMax == None:
                            globalWeightMax= weight
                            globalWeightMin= weight
                        maxValue= weight
                        minValue= weight
                        population.append(weight)
                        total+= weight
                elif data[k].grid.concerns_set.all()[i].weight != None:
                    weight= data[k].grid.concerns_set.all()[i].weight
                    if maxValue < weight:
                        maxValue= weight
                    if minValue > weight:
                        minValue= weight
                    if globalWeightMax < weight:
                        globalWeightMax= weight
                    if globalWeightMin > weight:
                        globalWeightMin= weight
                    total+= weight
                    population.append(weight) 
                k+= 1
            i+= 1
            #calculate the mean
            if len(population) > 0:
                #now that we have the data lets first calculate the range
                rangeTableWeight.append(maxValue - minValue)
                #now lets calculate the mean
                mean= total/len(population)
                meanTableWeight.append(mean)
                #calculate std
                total= 0
                for value in population:
                    total+= (value - mean)**2
                stdTableWeight.append(sqrt(total/len(population)))
                k= 0
            else:
                rangeTableWeight.append(None)
                meanTableWeight.append(None)
                stdTableWeight.append(None)
                
        return (stdTableRating, meanTableRating, rangeTableRating, stdTableWeight, meanTableWeight, rangeTableWeight, (globalMax, globalMin, globalWeightMax, globalWeightMin))
    else:
        return None
    
def __createRangeTableColorMap__(globalMax, globalMin, rangeTable):
   
    #end color
    colorEnd= (255, 255, 255)
    
    #start color
    colorStart= (240, 72, 74)
       
    maxRange= globalMax - globalMin
    return  __createColorMap__(100, maxRange, colorStart, colorEnd, rangeTable)

def __createStdTableColorMap__(globalMax, globalMin, stdTable):
    #end color
    colorEnd= (255, 255, 255)
    
    #start color
    colorStart= (240, 72, 74)
    
    mean= (globalMax + globalMin)/2
    maxStd= sqrt(((globalMax - mean)**2 + (globalMin - mean)**2)/2)
    return  __createColorMap__(100, maxStd, colorStart, colorEnd, stdTable)   

def __createColorMap__(colorStep, maxValue, startColor, endColor, table):
    
    yr, yg, yb= startColor
    xr, xg, xb= endColor
    colorMap= []
    for row in table:
        colorRow= []
        pos= None
        if type(row) == type([]): 
            for value in row:
                if maxValue != 0:
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
                pos= ceil((row/maxValue)*100)
                red = ceil((xr + (( pos * (yr - xr)) / (colorStep-1))))        
                green = ceil((xg + (( pos * (yg - xg)) / (colorStep-1))))       
                blue = ceil((xb + (( pos * (yb - xb)) / (colorStep-1))))
                #colorRow.append((int(red), int(green), int(blue)))
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
        #but first check if the session is in a state where there is no data the can be requested or responded
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
                    print 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"' 
                    raise ValueError('One or more concerns are empty')
            else:
                print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)')
            
            #check right pole
            keyName= 'concern_'+ str((i + 1)) + '_right'
            if request.POST.has_key(keyName):
                if request.POST[keyName] == None or request.POST[keyName].strip() == '':
                    print 'Error concern ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"' 
                    raise ValueError('One or more concerns are empty')
            else:
                print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)')
            i+= 1;
        
        i= 0;
        #validate the alternatives
        while i < nAlternatives:
            keyName= 'alternative_' + str((i + 1)) + '_name'
            if request.POST.has_key(keyName):
                if request.POST[keyName] == None or request.POST[keyName].strip() == '':
                    print 'Error alternative ' + keyName + ' has an invalid value: "' + request.POST[keyName] + '"' 
                    raise ValueError('One or more alternatives are empty')
            else:
                print 'Error request is missing argument: ' + keyName
                raise KeyError('Invalid request, request is missing argument(s)') 
            i+= 1
        return True
    else:
        print 'Error request is missing arguments: nAlternatives: ' + str(request.POST.has_key('nAlternatives')) + ' nConcerns: ' +  str(request.POST.has_key('nConcerns'))
        raise KeyError('Invalid request, request is missing argument(s)')
