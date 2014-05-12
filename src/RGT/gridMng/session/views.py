from math import sqrt, ceil
import uuid
import logging
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required

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
from RGT.gridMng.utility import *
from RGT.gridMng.response.xml.htmlResponseUtil import *
from RGT.gridMng.response.xml.svgResponseUtil import createSvgResponse
from RGT.gridMng.response.xml.generalUtil import createXmlGridIdNode, createXmlNumberOfResponseNode
from RGT.gridMng.views import updateGrid, createGrid, __validateInputForGrid
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
from RGT.gridMng.template.session.pendingResponsesData import PendingResponsesData
from RGT.gridMng.fileData import FileData
from RGT.gridMng.utility import generateGridTable, createDendogram, getImageError
from RGT.settings import SESSION_USID_KEY_LENGTH, DEBUG


logger = logging.getLogger('django.request')


@login_required
def ajaxGetCreateSessionPage(request):
    """
    This function is used to send back the page that the user sees when he
    press the button to create a new session.
    """
    user1 = request.user
    gridtype = Grid.GridType.USER_GRID
    grids = Grid.objects.filter(user=user1, grid_type=gridtype)

    if len(grids) <= 0:
        grids = None

    templateData = CreateSessionData(grids)
    context = RequestContext(request, {'data': templateData})

    return render(request, 'gridMng/createSession.html', context_instance=context)


@login_required
def getMySessionsPage(request):
    try:
        is_facilitator = Facilitator.objects.isFacilitator(request.user)
        if is_facilitator:
            facilitator = Facilitator.objects.get(user=request.user)
            sessions = facilitator.session_set.all()
            return render(request, 'gridMng/mySessions.html', {'sessions': sessions})
    except:
        __debug_print_stacktrace()

    return render(request, 'gridMng/mySessions.html')

@login_required
def show_detailed(request, usid):
    """
     This function is used to display a detailed page of a session with the given usid
    """
    facilitator, created = Facilitator.objects.get_or_create(user=request.user)
    session = get_object_or_404(Session, usid=usid, facilitator=facilitator)
    template_data = MySessionsContentData(session=session)
    context = RequestContext(request, {'session': session, 'data': template_data})
    template = loader.get_template('gridMng/mySessionsContent.html')
    session_html = template.render(context)
    sessions = Session.objects.filter(facilitator=facilitator)

    return render(request, 'gridMng/showSession.html', {'session': session, 'sessions': sessions, 'session_html': session_html })


@login_required
def show_latest(request):
    if Facilitator.objects.isFacilitator(request.user):
        facilitator, created = Facilitator.objects.get_or_create(user=request.user)
        latest_session = Session.objects.filter(facilitator=facilitator).last()
        return redirect(latest_session)
    else:
        return redirect('/sessions')


@login_required
def ajaxGetMySessionContentPage(request):
    if not 'sessionUSID' in request.POST:
        return HttpErrorResponse('No session id found in the request')

    try:
        is_facilitator = Facilitator.objects.isFacilitator(request.user)
        if not is_facilitator:
            return HttpErrorResponse('You are not the facilitator for this session')

        facilitator = Facilitator.objects.get(user=request.user)
        session = Session.objects.get(usid=request.POST['sessionUSID'], facilitator=facilitator)
        template_data = MySessionsContentData(session)
        template = loader.get_template('gridMng/mySessionsContent.html')
        context = RequestContext(request, {'data': template_data, 'session': session})
        htmlData = template.render(context)
        return HttpSuccessResponse(htmlData)
    except:
        logger.exception("Exception in user code")
        return HttpErrorResponse('No session found')


@login_required
def ajaxCreateSession(request):
    if request.method == 'GET':
        return ajaxGetCreateSessionPage(request)
    elif request.method == 'POST':
        gridUSID = request.POST.get('gridUSID')
        if not gridUSID:
            return HttpErrorResponse('gridUSID can not be empty')

        try:
            grid = Grid.objects.get(user=request.user, usid=gridUSID)
        except ObjectDoesNotExist:
            return HttpErrorResponse('Grid was not found')

        name = None
        if 'sessionName' in request.POST:
            name = request.POST.get('sessionName','').strip()
            if not name:
                return HttpErrorResponse('Name can not be empty')

        show_results = None
        if 'showResults' in request.POST:
            if request.POST.get('showResults') == "Y":
                show_results = True
            elif request.POST.get('showResults') != "N":
                return HttpErrorResponse('Invalid value for showResults given')

        session = Session.objects.create_session(request.user, grid, name, show_results)
        return HttpSuccessResponse('Session was created.')


@login_required
def getParticipatingSessionsPage(request):
    sessions = []
    templateData = ParticipatingSessionsData()
    for participation in request.user.userparticipatesession_set.all():
        session = participation.session
        sessions.append((session.usid, session.get_descriptive_name()))
    if len(sessions) > 0:
        templateData.hasSessions = True

    templateData.sessions = sessions
    pendingResponses = PendingResponsesData()
    pendingResponses.pedingResponsesTable = __createPendingResponseData(request.user)
    templateData.pendingResponses = pendingResponses

    context = RequestContext(request, {'data': templateData})
    return render(request, 'gridMng/participatingSessions.html', context)


@login_required
def ajaxJoinSession(request):
    user1 = request.user
    invitationKey1 = None
    error = None
    if 'invitationKey' in request.POST:
        invitationKey1 = request.POST['invitationKey'].strip()
    else:
        error = 'no invitation key was received'
    if not error:
        try:
            session = Session.objects.filter(invitationKey=invitationKey1)
            if len(session) > 0:
                session[0].addParticipant(user1)
                data = {session[0].usid: session[0].get_descriptive_name()}
                return HttpResponse(createXmlSuccessResponse(
                    'You have been added as participant in session: "' + session[0].name + '".',
                    createXmlForComboBox(data)), content_type='application/xml')
            else:
                return HttpErrorResponse('Session does not exist')
        except UserAlreadyParticipating:
            return HttpErrorResponse('You are already participating in the session')
        except WrongState:
            return HttpErrorResponse('Can\'t join session as it is passed \'initial\' state')
        except UserIsFacilitator:
            return HttpErrorResponse('You are already the facilitator of this session.'),
        except:
            __debug_print_stacktrace()
            logger.exception('Unknown error')
            return HttpErrorResponse('Unknown error')
    else:
        return HttpErrorResponse(error)


@login_required
def ajaxChangeSessionState(request):
    if 'sessionUSID' in request.POST and 'newState' in request.POST:
        facilitatorObj = request.user.facilitator_set.all()
        if len(facilitatorObj) >= 1:
            facilitatorObj = facilitatorObj[0]
            session = facilitatorObj.session_set.filter(usid=request.POST['sessionUSID'])
            if len(session) >= 1:
                try:
                    session = session[0]
                    name = request.POST['newState']
                    stateObj = State.objects.filter(name=request.POST['newState'])
                    if len(stateObj) >= 1:
                        stateObj = stateObj[0]
                        if name == 'finish':

                            try:
                                __saveSessionGridAsUserGrid(request)
                            except:
                                __debug_print_stacktrace()
                        session.changeState(stateObj)
                        return ajaxGetMySessionContentPage(request)
                    else:
                        return HttpErrorResponse('Invalid state given in the request')
                except WrongState:
                    __debug_print_stacktrace()
                    return HttpErrorResponse('Can\'t change states, session is in the wrong state')
                except:
                    __debug_print_stacktrace()
                    logger.exception('Unknown error')
                    return HttpErrorResponse('Unknown error')
            else:
                return HttpErrorResponse('Session not found')
        else:
            return HttpErrorResponse('You are not a facilitator for the session, can\'t change states.')
    else:
        return HttpErrorResponse('Invalid request, request is missing arguments')


@login_required
def ajaxGetParticipatingSessionContentPage(request):
    if request.method == 'POST':
        if 'sessionUSID' in request.POST:
            sessionID = Session.objects.get(usid=request.POST['sessionUSID'])
            sessionObj = request.user.userparticipatesession_set.filter(session=sessionID)
            if len(sessionObj) >= 1:
                sessionObj = sessionObj[0].session
                state = sessionObj.state
                iteration = sessionObj.iteration
                iterations = []
                hasPreviousResponseRelationGrid = False
                templateData = ParticipatingSessionsContentData()
                templateData.iteration = iteration
                templateData.responseStatus = '-----'

                # lets create a list of iteration that i have responded
                responseGridRelations = ResponseGrid.objects.filter(session=sessionObj, user=request.user)
                gridTablesData = __generateParticipatingSessionsGridsData(sessionObj, iteration,
                                                                          responseGridRelations)
                if len(responseGridRelations) >= 1:
                    for responseGridRelation in responseGridRelations:
                        iterations.append(responseGridRelation.iteration)
                templateData.iterations = iterations
                if state.name == SessionState.CHECK:
                    templateData.hideSaveResponseButton = True
                    templateData.sessionStatus = 'Checking previous results'
                    template = loader.get_template('gridMng/participatingSessionsContent.html')
                    context = RequestContext(request, {'data': templateData})
                    htmlData = template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.INITIAL:
                    templateData.hideSaveResponseButton = True
                    templateData.sessionStatus = 'Waiting for users to join'
                    template = loader.get_template('gridMng/participatingSessionsContent.html')
                    context = RequestContext(request, {'data': templateData})
                    htmlData = template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                elif state.name == SessionState.FINISH:
                    templateData.hideSaveResponseButton = True
                    templateData.sessionStatus = 'Closed'
                    template = loader.get_template('gridMng/participatingSessionsContent.html')
                    context = RequestContext(request, {'data': templateData})
                    htmlData = template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:

                    templateParticipatingSessions = ParticipatingSessionsContentGridsData()
                    templateData.participatingSessionsContentGridsData = templateParticipatingSessions
                    # there always is a session table being displayed to the user, so add this table in here
                    templateParticipatingSessions.displaySessionGrid = True
                    templateParticipatingSessions.sessionGridData = GridTableData(gridTablesData['sessionGridTable'])
                    templateParticipatingSessions.sessionGridData.tableId = generateRandomString()
                    templateParticipatingSessions.sessionGridData.doesNotShowLegend = True
                    # check to see if there is a response table, if so add it
                    if 'currentResponseGridTable' in gridTablesData:
                        templateParticipatingSessions.responseGridData = GridTableData(
                            gridTablesData['currentResponseGridTable'])
                    else:
                        # if there is no response display a table with the data as seem in the session grid
                        templateParticipatingSessions.responseGridData = GridTableData(
                            gridTablesData['sessionGridTable'])
                        # the weights need to be duplicated in a new object as  the list will be poped later on
                        templateParticipatingSessions.responseGridData.weights = templateParticipatingSessions.sessionGridData.weights[
                            :]
                    templateParticipatingSessions.responseGridData.tableId = generateRandomString()
                    templateParticipatingSessions.displayResponseGrid = True
                    # if the gridTablesData contains a previous response table add it
                    if 'previousResponseGrid' in gridTablesData:
                        templateParticipatingSessions.previousResponseGridData = GridTableData(
                            gridTablesData['previousResponseGrid'])
                        templateParticipatingSessions.previousResponseGridData.tableId = generateRandomString()
                        templateParticipatingSessions.previousResponseGridData.doesNotShowLegend = True
                        hasPreviousResponseRelationGrid = True
                        templateParticipatingSessions.displayPreviousResponseGrid = True

                    # calculate how many participants there are in this session and how many have sent a response
                    templateData.nReceivedResponses = 0
                    templateData.nParticipants = 0
                    templateData.showNParticipantsAndResponces = True
                    try:
                        templateData.nReceivedResponses = len(sessionObj.getUsersThatRespondedRequest())
                        templateData.nParticipants = len(sessionObj.getParticipators())
                    except:
                        __debug_print_stacktrace()
                    # check if i have sent a response grid
                    responseGrid = request.user.responsegrid_set.filter(user=request.user, iteration=iteration,
                                                                        session=sessionObj)
                    if len(responseGrid) <= 0:
                        # i didn't respond, so display a page with the correct settings to answer it
                        templateData.responseStatus = 'No response was sent'
                        if state.name == SessionState.AC:
                            # first get the current session grid to display to the user
                            templateParticipatingSessions.responseGridData.changeCornAlt = True
                            templateParticipatingSessions.responseGridData.doesNotShowLegend = True
                            templateData.sessionStatus = 'Waiting for Alternative and concerns'
                            template = loader.get_template('gridMng/participatingSessionsContent.html')
                            context = RequestContext(request, {'data': templateData})
                            htmlData = template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        elif state.name == SessionState.RW:
                            templateData.sessionStatus = 'Waiting for Ratings and Weights'
                            templateParticipatingSessions.sessionGridData.showRatingWhileFalseChangeRatingsWeights = True
                            templateParticipatingSessions.responseGridData.changeRatingsWeights = True
                            template = loader.get_template('gridMng/participatingSessionsContent.html')
                            if hasPreviousResponseRelationGrid:
                                templateParticipatingSessions.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights = True

                            context = RequestContext(request, {'data': templateData})
                            htmlData = template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        # if i did respond show me my response and the current session grid so if i changed my mind i still can change the response
                        templateData.responseStatus = 'Response was sent at: '
                        templateData.dateTime = responseGrid[0].grid.dateTime
                        if state.name == SessionState.AC:
                            templateParticipatingSessions.responseGridData.changeCornAlt = True
                            templateData.sessionStatus = 'Waiting for Alternative and concerns'
                            template = loader.get_template('gridMng/participatingSessionsContent.html')
                            context = RequestContext(request, {'data': templateData})
                            htmlData = template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        elif state.name == SessionState.RW:
                            templateParticipatingSessions.sessionGridData.showRatingWhileFalseChangeRatingsWeights = True
                            templateParticipatingSessions.responseGridData.changeRatingsWeights = True
                            templateData.sessionStatus = 'Waiting for Ratings and Weights'
                            template = loader.get_template('gridMng/participatingSessionsContent.html')
                            if hasPreviousResponseRelationGrid:
                                templateParticipatingSessions.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights = True

                            context = RequestContext(request, {'data': templateData})
                            htmlData = template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    return HttpErrorResponse('Unable to identify current session state')
            else:
                return HttpErrorResponse('You are not participating in the given session')
        else:
            return HttpErrorResponse('Invalid request, request is missing arguments')
    return getParticipatingSessionsPage(request)


@login_required
def ajaxRespond(request):
    """ This function will determine if we are creating a new response grid or updating an old one """

    userObj = request.user
    if 'sessionUSID' in request.POST and 'gridType' in request.POST and 'iteration' in request.POST:
        # check if user can answer to the session
        sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'])
        if len(sessionObj) >= 1:
            sessionObj = sessionObj[0]
            userSessionRelation = userObj.userparticipatesession_set.filter(session=sessionObj)
            if len(userSessionRelation) >= 1:
                sessionIteration = int(request.POST['iteration'])
                # check if the session is in a state where it is allowed to send a response
                if sessionIteration == sessionObj.iteration:
                    userResponseGridRelation = userObj.responsegrid_set.filter(iteration=sessionIteration,
                                                                               session=sessionObj)

                    # if the response is for a concern/alternative request, run extra validation code (no empty concerns or alternatives allowed)
                    if sessionObj.state.name == State.objects.getWaitingForAltAndConState().name:
                        try:
                            __validateAltConResponse(request)
                        except (ValueError, KeyError) as error:
                            __debug_print_stacktrace()
                            return HttpErrorResponse(error.args[0])
                        except:
                            __debug_print_stacktrace()
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown error')
                            # determine if it is a new response grid or not
                    if len(userResponseGridRelation) >= 1:
                        # this is an update
                        gridObj = userResponseGridRelation[0].grid
                        isConcernAlternativeResponseGrid = False
                        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                            isConcernAlternativeResponseGrid = True
                        try:
                            obj = __validateInputForGrid(request, isConcernAlternativeResponseGrid)
                        except (KeyError, ValueError) as error:
                            __debug_print_stacktrace()
                            return HttpErrorResponse(error.args[0])
                        except:
                            __debug_print_stacktrace()
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown error')
                        nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues = obj

                        if gridObj is not None:
                            for i in range(int(nAlternatives)):
                                try:
                                    str(alternativeValues[i])
                                except:
                                    return HttpErrorResponse("Invalid alternative name : " + alternativeValues[i])
                            for i in range(int(nConcerns)):
                                try:
                                    str(concernValues[i][0])
                                except:
                                    return HttpErrorResponse("Invalid left concern name : " + concernValues[i][0])
                                try:
                                    str(concernValues[i][1])
                                except:
                                    return HttpErrorResponse("Invalid right concern name : " + concernValues[i][1])
                            try:
                                isGridCreated = updateGrid(gridObj, nConcerns, nAlternatives, concernValues,
                                                           alternativeValues, ratioValues,
                                                           isConcernAlternativeResponseGrid)
                                if isGridCreated:
                                    return HttpResponse(createXmlSuccessResponse('Grid was saved', createDateTimeTag(
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), content_type='application/xml')
                            except:
                                __debug_print_stacktrace()
                                logger.exception('Unknown error')
                                return HttpErrorResponse('Unknown error')
                        else:
                            return HttpErrorResponse("No grid found")
                            # return ajaxUpdateGrid(request)
                    else:
                        # this is a new grid, which means first response
                        gridType = None
                        showRatings = True
                        isConcernAlternativeResponseGrid = False
                        # discover the response grid type
                        if sessionObj.state.name == SessionState.AC:
                            gridType = Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN
                            showRatings = False
                            isConcernAlternativeResponseGrid = True
                        elif sessionObj.state.name == SessionState.RW:
                            gridType = Grid.GridType.RESPONSE_GRID_RATING_WEIGHT
                        # validate and retrieve the data that is going to be used in the grid
                        try:
                            obj = __validateInputForGrid(request, isConcernAlternativeResponseGrid)
                        except (KeyError, ValueError) as error:
                            __debug_print_stacktrace()
                            return HttpErrorResponse(error.args[0])
                        except:
                            __debug_print_stacktrace()
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown error')

                        nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues = obj
                        try:
                            # set the relation ship of the response grid with the session
                            gridObj = createGrid(userObj, gridType, None, nConcerns, nAlternatives, concernValues,
                                                 alternativeValues, ratioValues, showRatings)
                            gridResponseRelation = ResponseGrid(grid=gridObj, session=sessionObj,
                                                                iteration=sessionIteration, user=userObj)
                            gridResponseRelation.save()

                            extraXmlData = createXmlNumberOfResponseNode(
                                len(sessionObj.getUsersThatRespondedRequest()) + 1)
                            if extraXmlData is None:
                                return HttpResponse(createXmlSuccessResponse('Grid created successfully.',
                                                                             createDateTimeTag(datetime.now().strftime(
                                                                                 "%Y-%m-%d %H:%M:%S"))),
                                                    content_type='application/xml')
                            else:
                                if isinstance(extraXmlData, list):
                                    extraXmlData.append(createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                    extraDataToUse = extraXmlData
                                else:
                                    extraDataToUse = [extraXmlData,
                                                      createDateTimeTag(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
                                return HttpResponse(
                                    createXmlSuccessResponse('Grid created successfully.', extraDataToUse),
                                    content_type='application/xml')
                        except:
                            __debug_print_stacktrace()
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown error')
                else:
                    return HttpErrorResponse(
                        'Can\'t create response grid, session is in a state where that is not permitted')
            else:
                return HttpErrorResponse('You are not participating in the session, can\'t send response grid')
        else:
            return HttpErrorResponse('Session was not found')
    else:
        return HttpErrorResponse('Invalid request, request is missing arguments')


# this function only return the content grids!!
@login_required
def ajaxGetParticipatingSessionsContentGrids(request):
    try:
        # check for the mandatory keys
        if 'iteration' in request.POST and 'sessionUSID' in request.POST:
            sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'])
            if len(sessionObj) >= 1:
                templateData = ParticipatingSessionsContentGridsData()
                templateData.displaySessionGrid = True
                templateData.displayResponseGrid = True
                iteration_ = int(request.POST['iteration'])
                sessionObj = sessionObj[0]
                hasPreviousResponseRelationGrid = False
                # check if the iteration is valid
                if iteration_ > sessionObj.iteration or iteration_ < 0:
                    return HttpErrorResponse('Invalid iteration value')
                response_grids = ResponseGrid.objects.filter(session=sessionObj, user=request.user)
                gridTablesData = __generateParticipatingSessionsGridsData(sessionObj, iteration_, response_grids)

                # there is always a session grid, so add it
                templateData.sessionGridData = GridTableData(gridTablesData['sessionGridTable'])
                templateData.sessionGridData.tableId = generateRandomString()
                templateData.sessionGridData.doesNotShowLegend = True
                templateData.displaySessionGrid = True
                # if the user sent a response display that grid
                if 'currentResponseGridTable' in gridTablesData:
                    templateData.responseGridData = GridTableData(gridTablesData['currentResponseGridTable'])
                else:
                    # if he hasn't sent a response display a grid with the values of the session grid
                    templateData.responseGridData = GridTableData(gridTablesData['sessionGridTable'])
                    # the weights need to be in a new object as we will pop it later (in the template)
                    templateData.responseGridData.weights = templateData.responseGridData.weights[:]
                templateData.responseGridData.tableId = generateRandomString()
                templateData.displayResponseGrid = True
                # if the gridTablesData contains a previous response table add it
                if 'previousResponseGrid' in gridTablesData:
                    templateData.previousResponseGridData = GridTableData(gridTablesData['previousResponseGrid'])
                    templateData.previousResponseGridData.tableId = generateRandomString()
                    templateData.previousResponseGridData.doesNotShowLegend = True
                    hasPreviousResponseRelationGrid = True
                    templateData.displayPreviousResponseGrid = True

                if len(request.user.userparticipatesession_set.filter(session=sessionObj)) >= 1:
                    responseGridRelation = ResponseGrid.objects.filter(session=sessionObj, iteration=iteration_,
                                                                       user=request.user)
                    # check to see if the user has already send an response grid
                    if len(responseGridRelation) >= 1:
                        # if he has sent an response grid display it again and let him edit it

                        responseGridRelation = responseGridRelation[0]
                        template = loader.get_template('gridMng/participatingSessionsContentGrids.html')
                        if responseGridRelation.grid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                            templateData.responseGridData.doesNotShowLegend = True
                            # check to see if the user should be allowed to change the response
                            if iteration_ == sessionObj.iteration:
                                templateData.responseGridData.changeCornAlt = True
                        else:
                            # check to see if the user should be allowed to change the response
                            templateData.sessionGridData.showRatingWhileFalseChangeRatingsWeights = True
                            templateData.responseGridData.showRatingWhileFalseChangeRatingsWeights = True
                            if iteration_ == sessionObj.iteration:
                                templateData.responseGridData.changeRatingsWeights = True
                                # if the previous response grid is displayed make sure it is displayed correctly
                                if hasPreviousResponseRelationGrid:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights = True
                            else:
                                # if the previous response grid is displayed make sure it is displayed correctly
                                if hasPreviousResponseRelationGrid:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights = True

                        context = RequestContext(request, {'data': templateData})
                        htmlData = template.render(context)
                        return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                    else:
                        # if he hasn't send a response grid check to see if he still can send it and if so display it
                        if iteration_ == sessionObj.iteration:
                            if sessionObj.state.name == SessionState.AC:
                                template = loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                templateData.responseGridData.changeCornAlt = True
                                templateData.responseGridData.doesNotShowLegend = True

                                context = RequestContext(request, {'data': templateData})
                                htmlData = template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')

                            elif sessionObj.state.name == SessionState.RW:
                                template = loader.get_template('gridMng/participatingSessionsContentGrids.html')
                                templateData.sessionGridData.showRatingWhileFalseChangeRatingsWeights = True
                                templateData.responseGridData.changeRatingsWeights = True
                                if hasPreviousResponseRelationGrid:
                                    templateData.previousResponseGridData.showRatingWhileFalseChangeRatingsWeights = True

                                context = RequestContext(request, {'data': templateData})
                                htmlData = template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            else:
                                return HttpResponse(createXmlSuccessResponse(
                                    '<div id="participatinSessionsMessageDiv"><p>Session is in a state where no grids are available</p></div>'),
                                    content_type='application/xml')
                        else:
                            return HttpErrorResponse(
                                'No response found for the session in iteration ' + request.POST['iteration'])
                else:
                    return HttpErrorResponse('You are not participating in the session')
            else:
                return HttpErrorResponse('Can\'t find session')
                #sessionObj= request.user.userparticipatesession_set.filter()
        else:
            return HttpErrorResponse('Invalid request, request is missing argument(s)')
    except:
        __debug_print_stacktrace()
        logger.exception('Unknown error')
        return HttpErrorResponse('Unknown error')


@login_required
def ajaxGetResults(request):
    """ Function is to get the session results for the facilitator for completed iterations """
    try:
        request_ = request
        if not ('sessionUSID' in request.POST and 'iteration' in request.POST):
            return HttpErrorResponse('Invalid request, request is missing argument(s)')
        else:
            if len(request.user.facilitator_set.all()) < 1:
                return HttpErrorResponse('You are not a facilitator for this session')
            else:
                facilitatorObj = request.user.facilitator_set.all()[0]
                sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'])
                if len(sessionObj) < 1:
                    return HttpErrorResponse('Couldn\'t find session')
                else:
                    session_ = sessionObj[0]
                    if session_.facilitator != facilitatorObj:
                        return HttpErrorResponse('You are not a facilitator for this session')
                    else:
                        iteration_ = int(request.POST['iteration'])
                        try:
                            templateData = __generateSessionIterationResult(request_, session_, iteration_)
                            if templateData is not None:
                                template = None
                                if type(templateData) == ResultRatingWeightTablesData:
                                    template = loader.get_template('gridMng/resultRatingWeightTables.html')
                                elif type(templateData) == ResultAlternativeConcernTableData:
                                    template = loader.get_template('gridMng/resultAlternativeConcernTable.html')
                                context = RequestContext(request, {'data': templateData})
                                htmlData = template.render(context)
                                return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                            else:
                                return HttpErrorResponse(
                                    'No results found. This means that the participants of this session did not provide any responses for this particular iteration.')
                        except WrongGridType:
                            return HttpErrorResponse('Unexpected type grid found')
                        except WrongSessionIteration:
                            return HttpErrorResponse('Session does not contain that iteration')
                        except:
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown error')
    except:
        __debug_print_stacktrace()
        logger.exception('Unknown error')
        return HttpErrorResponse('Unknown error')


@login_required
def ajaxGetResponseResults(request):
    try:
        request_ = request
        if not ('sessionUSID' in request.POST and 'iteration' in request.POST):
            return HttpErrorResponse('Invalid request, request is missing argument(s)')
        else:
            sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'])
            if len(sessionObj) < 1:
                return HttpErrorResponse('Couldn\'t find session')
            else:
                session_ = sessionObj[0]
                showResultsYes = True
                if session_.showResult != showResultsYes:
                    return HttpErrorResponse('Results are not available for the Participants')
                else:
                    iteration_ = int(request.POST['iteration'])
                    try:
                        templateData = __generateSessionIterationResult(request_, session_, iteration_)
                        if templateData is not None:
                            template = None
                            if type(templateData) == ResultRatingWeightTablesData:
                                template = loader.get_template('gridMng/resultRatingWeightTables.html')
                            elif type(templateData) == ResultAlternativeConcernTableData:
                                template = loader.get_template('gridMng/resultAlternativeConcernTable.html')
                            context = RequestContext(request, {'data': templateData})
                            htmlData = template.render(context)
                            return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                        else:
                            return HttpErrorResponse(
                                'No results found. This means that the participants of this session did not provide any responses for this particular iteration.')
                    except WrongGridType:
                        return HttpErrorResponse('Unexpected type grid found')
                    except WrongSessionIteration:
                        return HttpErrorResponse('Session does not contain that iteration')
                    except:
                        logger.exception('Unknown error')
                        return HttpErrorResponse('Unknown error')
    except:
        __debug_print_stacktrace()
        logger.exception('Unknown error')
        return HttpErrorResponse('Unknown error')


@login_required
def ajaxDownloadSessionResults(request):
    """ Download the results from a session in the form of an image """
    try:
        if not 'sessionUSID' in request.POST:
            raise Exception('sessionUSID key was not received')
        elif not 'iteration' in request.POST:
            raise Exception('iteration key was not received')
        else:
            if len(request.user.facilitator_set.all()) < 1:
                raise Exception('User is not a facilitator for a session')
            else:
                facilitatorObj = request.user.facilitator_set.all()[0]
                sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'])
                if len(sessionObj) < 1:
                    raise Exception('Couldn\'t find session: ' + request.POST['sessionUSID'])
                else:
                    session_ = sessionObj[0]
                    if session_.facilitator != facilitatorObj:
                        raise Exception('User is not a facilitator for session ' + request.POST['sessionUSID'])
                    else:
                        iteration_ = int(request.POST['iteration'])
                        templateData = __generateSessionIterationResult(request, session_, iteration_)
                        # check which type of response it is and convert the data so a svg can be created
                        responseGridRelation = session_.responsegrid_set.filter(iteration=iteration_)
                        if len(responseGridRelation) >= 1:
                            gridType = responseGridRelation[0].grid.grid_type
                            if gridType == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
                                imgData = FileData()
                                convertToData = request.POST['convertTo']
                                if convertToData == 'svg':
                                    imgData.data = convertAlternativeConcernSessionResultToSvg(templateData)
                                    imgData.fileExtention = 'svg'
                                    imgData.ContentType = 'image/svg+xml'

                                if 'fileName' in request.POST:
                                    imgData.fileName = request.POST['fileName']

                                    if not imgData.fileName:
                                        imgData.fileName = generateRandomString()

                                return createFileResponse(imgData)
                            else:
                                rangeData = SessionResultImageConvertionData()
                                meanData = SessionResultImageConvertionData()
                                stdData = SessionResultImageConvertionData()

                                # the header object is shared among all the 3 tables
                                templateData.rangeData.headers.append('weight')

                                # range
                                rangeData.tableHeader = templateData.rangeData.headers
                                sizeWeights = len(templateData.rangeData.weights)
                                temp = templateData.rangeData.table
                                finalTable = []
                                concerns = []

                                i = 0
                                j = 0

                                while i < len(temp):
                                    row = []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], temp[i][j + 1][1]))
                                        j += 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j = 0
                                    i += 1

                                i = 0
                                while i < sizeWeights:
                                    finalTable[i].append((
                                        templateData.rangeData.weights[i][0], templateData.rangeData.weightColorMap[i]))
                                    i += 1

                                rangeData.tableData = finalTable
                                rangeData.header = templateData.rangeData.tableHead
                                rangeData.concerns = concerns

                                # mean
                                meanData.tableHeader = templateData.meanData.headers
                                # meanData.tableHeader.append('weight')
                                finalTable = []
                                concerns = []
                                sizeWeights = len(templateData.meanData.weights)
                                temp = templateData.meanData.table

                                i = 0
                                j = 0

                                while i < len(temp):
                                    row = []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], None))
                                        j += 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j = 0
                                    i += 1

                                i = 0
                                while i < sizeWeights:
                                    finalTable[i].append((templateData.meanData.weights[i][0], None))
                                    i += 1

                                meanData.tableData = finalTable
                                meanData.header = templateData.meanData.tableHead
                                meanData.concerns = concerns

                                # std
                                finalTable = []
                                concerns = []
                                stdData.tableHeader = templateData.stdData.headers
                                sizeWeights = len(templateData.stdData.weights)
                                temp = templateData.stdData.table

                                i = 0
                                j = 0

                                while i < len(temp):
                                    row = []
                                    while j < len(temp[1]) - 2:
                                        row.append((temp[i][j + 1][0], temp[i][j + 1][1]))
                                        j += 1
                                    finalTable.append(row)
                                    concerns.append((temp[i][0][0], temp[i][len(temp[i]) - 1][0]))
                                    j = 0
                                    i += 1

                                i = 0
                                while i < sizeWeights:
                                    finalTable[i].append(
                                        (templateData.stdData.weights[i][0], templateData.stdData.weightColorMap[i]))
                                    i += 1

                                stdData.tableData = finalTable
                                stdData.header = templateData.stdData.tableHead
                                stdData.concerns = concerns

                                imgData = FileData()
                                convertToData = request.POST['convertTo']
                                if convertToData == 'svg':
                                    imgData.data = convertRatingWeightSessionResultToSvg(meanData, rangeData, stdData)
                                    imgData.fileExtention = 'svg'
                                    imgData.ContentType = 'image/svg+xml'

                                if 'fileName' in request.POST:
                                    imgData.fileName = request.POST['fileName']

                                    if not imgData.fileName:
                                        imgData.fileName = generateRandomString()

                                return createFileResponse(imgData)
    except:
        __debug_print_stacktrace()
    # in case of an error or checks failing return an image error
    errorImageData = getImageError()
    # send the file
    response = HttpResponse(errorImageData, content_type='image/jpg')
    response['Content-Disposition'] = 'attachment; filename=error.jpg'
    return response


# function that will get the page that display the participants of a session
@login_required
def ajaxGetParticipatingPage(request):
    try:
        # check if the mandatory variables are present
        if 'sessionUSID' in request.POST:
            # get the session
            sessionObj = Session.objects.get(usid=request.POST['sessionUSID'])
            if sessionObj is not None:
                #sessionObj= sessionObj[0]
                # check if the user is a facilitator and if he is the facilitator for this session
                facilitatorObj = request.user.facilitator_set.all()
                if len(facilitatorObj) >= 1 and sessionObj.facilitator == facilitatorObj[0]:
                    # get all the users that reponded to the request
                    templateData = ParticipantsData()
                    templateData.participants = __createParticipantPanelData(sessionObj)
                    template = loader.get_template('gridMng/participants.html')
                    context = RequestContext(request, {'data': templateData})
                    htmlData = template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    return HttpErrorResponse('Can\'t complete request, you are not a facilitator for this session')
            else:
                return HttpErrorResponse('Session does not exist')
        else:
            return HttpErrorResponse('Invalid request, request is missing argument(s)')
    except:
        __debug_print_stacktrace()
        logger.exception('Unknown error')
        return HttpErrorResponse('Unknown error')


@login_required
def ajaxGenerateSessionDendrogram(request):
    # check if all the mandatory keys are present
    if 'sessionUSID' in request.POST and 'iteration' in request.POST:
        # check to see if the user is a facilitator
        try:
            facilitatorObj = Facilitator.objects.filter(user=request.user)
            if len(facilitatorObj) >= 1:
                facilitatorObj = facilitatorObj[0]
                # find the session
                sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'], facilitator=facilitatorObj)
                if len(sessionObj) >= 1:
                    sessionObj = sessionObj[0]
                    iterationObj = int(request.POST['iteration'])
                    # display the current iteration if there was no iteration specified
                    if iterationObj < 0:
                        iterationObj = sessionObj.iteration
                    sessionGridRelation = SessionGrid.objects.filter(session=sessionObj, iteration=iterationObj)
                    if len(sessionGridRelation) >= 1:
                        sessionGridRelation = sessionGridRelation[0]
                        try:
                            imgData = createDendogram(sessionGridRelation.grid)
                            responseData = createSvgResponse(imgData,
                                                             createXmlGridIdNode(sessionGridRelation.grid.usid))
                            return HttpResponse(responseData, content_type='application/xml')
                        except UnicodeEncodeError as error:
                            errorString = 'Invalid character found in the grid. The "' + error.object[
                                error.start:error.end] + '" character can not be convert or used safely.\nDendogram can not be created.'
                            return HttpErrorResponse(errorString)
                        except Exception:
                            __debug_print_stacktrace()
                            logger.exception('Unknown error')
                            return HttpErrorResponse('Unknown dendrogram error')
                    else:
                        return HttpErrorResponse('No grid found for the selected iteration')
                else:
                    return HttpErrorResponse('Session was not found')
            else:
                return HttpErrorResponse('You are not a facilitator')
        except:
            __debug_print_stacktrace()
    else:
        return HttpErrorResponse('Invalid request, request is missing argument(s)')


@login_required
def ajaxGetSessionGrid(request):
    # check if all the mandatory keys are present
    if 'sessionUSID' in request.POST:
        # check if the user is an facilitator
        facilitatorObj = request.user.facilitator_set.all()
        if len(facilitatorObj) >= 1:
            facilitatorObj = facilitatorObj[0]
            # check if the session exists
            sessionObj = Session.objects.filter(usid=request.POST['sessionUSID'], facilitator=facilitatorObj)
            if len(sessionObj) >= 1:
                sessionObj = sessionObj[0]
                # check if the grid exists
                gridObj = SessionGrid.objects.filter(session=sessionObj, iteration=sessionObj.iteration)
                if len(gridObj) >= 1:
                    gridObj = gridObj[0].grid
                    templateData = GridTableData(generateGridTable(gridObj))
                    templateData.tableId = generateRandomString()
                    templateData.usid = gridObj.usid
                    # if the state is not check then return a table where nothing can be changed, else return a table that can be changed
                    if sessionObj.state.name == State.objects.getCheckState().name:
                        templateData.changeRatingsWeights = True
                        templateData.changeCornAlt = True
                        templateData.checkForTableIsSave = True
                    template = loader.get_template('gridMng/gridTable.html')
                    context = RequestContext(request, {'data': templateData})
                    htmlData = template.render(context)
                    return HttpResponse(createXmlSuccessResponse(htmlData), content_type='application/xml')
                else:
                    return HttpErrorResponse('Grid not found')
            else:
                return HttpErrorResponse('Session was not found')
        else:
            return HttpErrorResponse('You are not a facilitator')
    else:
        return HttpErrorResponse('Invalid request, request is missing argument(s)')


def __calculateMeans(ratioMatrices=None):
    if ratioMatrices is None or ratioMatrices[0] is None or ratioMatrices[0][0] is None:
        return None

    # find out the dimensions of the ratio matrix
    nMatrixs = len(ratioMatrices)
    nCols = len(ratioMatrices[0][0])
    nRows = len(ratioMatrices[0])
    nAvailableAnswers = 0  # used to see how many ratios are numbers in the same cell over multible ratio matrixes
    totalRatio = 0
    meanMatrix = []
    i = 0
    j = 0
    k = 0
    while i < nRows:
        tempRow = []
        while j < nCols:
            while k < nMatrixs:
                temp = ratioMatrices[k][i][j]
                # calculate the total ratio between all the cell in the same position of all the reponse grids
                if temp is not None:
                    totalRatio += temp
                    nAvailableAnswers += 1
                k += 1
            k = 0
            j += 1
            # calculate the mean
            tempRow.append(float("{0:.2f}".format(totalRatio / nAvailableAnswers)))
            totalRatio = 0
            nAvailableAnswers = 0
        j = 0
        i += 1
        meanMatrix.append(tempRow)
    return meanMatrix


def __calculateRange(ratioMatrices=None):
    if ratioMatrices is None or ratioMatrices[0] is None or ratioMatrices[0][0] is None:
        return None

    nMatrixs = len(ratioMatrices)
    nCols = len(ratioMatrices[0][0])
    nRows = len(ratioMatrices[0])
    globalMin = None
    globalMax = None
    rangeMatrix = []
    i = 0
    j = 0
    k = 0
    while i < nRows:
        tempRow = []
        while j < nCols:
            while k < nMatrixs:
                temp = ratioMatrices[k][i][j]
                if temp is not None:
                    # if this is the first cell set the max and min to what is found in the ration matrix
                    if globalMin is None:
                        globalMin = temp
                        globalMax = temp
                    else:
                        if temp > globalMax:
                            globalMax = temp
                        if temp < globalMin:
                            globalMin = temp
                k += 1
            k = 0
            j += 1
            tempRow.append(globalMax - globalMin)
            globalMax = None
            globalMin = None
        j = 0
        i += 1
        rangeMatrix.append(tempRow)
    return rangeMatrix


def __calculateStandardDeviation(ratioMatrices=None, meanMatrix=None):
    if ratioMatrices is None or ratioMatrices[0] is None or ratioMatrices[0][0] is None or meanMatrix is None:
        return None

    nMatrixs = len(ratioMatrices)
    nCols = len(ratioMatrices[0][0])
    nRows = len(ratioMatrices[0])
    stdMatrix = []
    nAvailableAnswers = 0
    total = 0
    i = 0
    j = 0
    k = 0
    while i < nRows:
        tempRow = []
        while j < nCols:
            tempMean = meanMatrix[i][j]
            while k < nMatrixs:
                temp = ratioMatrices[k][i][j]
                if temp is not None:
                    temp -= tempMean
                    temp **= 2
                    total += temp
                    nAvailableAnswers += 1
                k += 1
            k = 0
            j += 1
            tempRow.append(float("{0:.2f}".format(sqrt(total / nAvailableAnswers))))
            total = 0
            nAvailableAnswers = 0
        j = 0
        i += 1
        stdMatrix.append(tempRow)

    return stdMatrix


def __findMinMaxInMatrix(matrix=None):
    if matrix is None or matrix[0] is None:
        return None

    nRows = len(matrix)
    nCols = len(matrix[0])
    minValue = None
    maxValue = None

    i = 0
    j = 0

    while i < nRows:
        while j < nCols:
            temp = matrix[i][j]
            if minValue is None:
                minValue = temp
                maxValue = temp
            else:
                if temp > maxValue:
                    maxValue = temp
                if temp < minValue:
                    minValue = temp
            j += 1
        j = 0
        i += 1

    return minValue, maxValue


def __createJSforRatioWeightSessionResultsChart(ratioMatrices=None, weightMatrices=None, participantNames=None):
    if ratioMatrices is None or weightMatrices is None:
        return None
        # create the data for the javascript. format should be a string --> [[name,value], [name,value], ....., [name,value]].
    javascriptRatioData = []  # format should be [[cell with js string data], [cell with js string data], ...]
    javascriptWeightData = []  # format should be [[cell with js string data], [cell with js string data], ...]
    i = 0
    k = 0
    nConcerns = len(ratioMatrices[0])
    nResponseGrids = len(ratioMatrices) - 1
    nAlternatives = len(ratioMatrices[0][0])

    # first create the table for the weights
    while i < nConcerns:
        temp = '['
        temp += '[\'session\','
        tempWeight = weightMatrices[0][0][i]
        # first element is always what is in the session grid
        if tempWeight is not None and tempWeight >= 1:
            temp += str(tempWeight) + ']'
        else:
            temp += '0]'
            # now add all other elements
        j = 0
        while j < nResponseGrids:
            tempWeight = weightMatrices[j + 1][0][i]  # j+1 because the session grid weights are in position 0
            if tempWeight is not None and tempWeight >= 1:
                temp += ',[\'' + participantNames[j] + '\',' + str(tempWeight) + ']'
            else:
                temp += ',[\'' + participantNames[j] + '\',0]'
            j += 1
        temp += ']'
        javascriptWeightData.append(temp)
        i += 1
    i = 0
    # now create the table for the ratios
    while i < nConcerns:
        row = []
        while k < nAlternatives:
            temp = '['
            j = 0
            # first element is always what is in the session grid
            temp += '[\'session\','
            tempRating = ratioMatrices[0][i][k]
            if tempRating is not None and tempRating >= 1:
                temp += str(tempRating) + ']'
            else:
                temp += '0]'
                # now add all other elements
            while j < nResponseGrids:
                tempRating = ratioMatrices[j + 1][i][k]  # j+1 because the session grid ratios are in position 0
                if tempRating is not None and tempRating >= 1:
                    temp += ',[\'' + participantNames[j] + '\',' + str(tempRating) + ']'
                else:
                    temp += ',[\'' + participantNames[j] + '\',0]'
                j += 1
            temp += ']'
            row.append(temp)
            k += 1
        k = 0
        javascriptRatioData.append(row)
        i += 1

    return javascriptRatioData, javascriptWeightData


def __generateAlternativeConcernResultTable(data=[], sessionGridObj=None):
    """
    This function is used to generate the input used for the resultAlternativeConcernTable.html template

    Arguemnts:
        data: obejct of QuerySet
            information: The QuerySet must contain all the grids that were submitted as response for a session with a iteration
        sessionGridObj: rgt.gridMng.models.Grid object
            nformation: The grid object must be of a session.

    Return:
        Tulip
            information: The tulip has two positions, the first position contains the data for the concern table and the
                         second position contains the data for the alternative table.

                         The concern data is an array containing a tulip in each position. The tulip represents a row of a table.
                         The first position of the tulip contains a string representing the left concern name. The second
                         position contains a string representing the right concern name. The third posisition contains an int
                         representing how many times the pair (left and right concern) was mentioned in all of the response grids.
                         The fourth position contains an int indicating how many times the left concern was mentioned individually.
                         The fifth position contains an int indication how many times the right concern was mentioned individially.
                         The sixth poisition contains a boolean that indicates if the pair was previously was present in the session
                         grid or not. The seventh position contains a string with the names of the users who suggested something.

                         The alternative data is an array containing a tulip. The tulip represents a row of a table. The tulip has four
                         positions. The first position contains a string representing the name of the alternative. The second position
                         contains an int that represents how many times that alternative was mentioned in the response grids. The third
                         position has a boolean indicating if the alternative was previously found in the session grid or not. The fourth
                         position has a string with the names of the users who suggested something.
    """
    concernsResult = []  # obj that will be returned with the concerns as following: (leftconcern, right concern, nPair, nLeftConcern, nRightConcern, isNew)
    alternativeResult = []  # obj that will be returned with the alternative as following: (alternative, nTime, isNew)
    oldConcernsPair = []
    oldAlternatives = []
    concerns = {}
    concernPairs = {}  # key is a tulp value is the number the pair is present together
    concernUsers = {}  # this tuple is for the list of participants who suggested the concerns in the responseGrid
    alternatives = {}
    alternativeUsers = {}  # this tuple is for the list of participants who suggested the alternative in the responseGrid
    i = 0

    # first find all the existing pairs of concerns
    if sessionGridObj is not None:
        for concern in sessionGridObj.concerns_set.all():
            lConcern = concern.leftPole
            rConcern = concern.rightPole
            if lConcern is None and rConcern is None:
                pass
            else:
                if lConcern is None:
                    lConcern = ""
                if rConcern is None:
                    rConcern = ""
                oldConcernsPair.append((lConcern.lower(), rConcern.lower()))

        for alternative in sessionGridObj.alternatives_set.all():
            oldAlternatives.append(alternative.name.lower())

    for relation in data:
        grid = relation.grid
        i += 1
        if i == 2:
            userID = relation.user.first_name + '\n'
            i = 0
        else:
            userID = relation.user.first_name + ' '
        for concern in grid.concerns_set.all():
            if concern.leftPole:
                temp = concern.leftPole.lower()
                if not temp in concerns:
                    concerns[temp] = 1
                else:
                    concerns[temp] += 1
            if concern.rightPole:
                temp = concern.rightPole.lower()
                if not temp in concerns:
                    concerns[temp] = 1
                else:
                    concerns[temp] += 1
            if (concern.leftPole.lower(), concern.rightPole.lower()) in concernPairs:
                concernPairs[(concern.leftPole.lower(), concern.rightPole.lower())] += 1
            else:
                concernPairs[(concern.leftPole.lower(), concern.rightPole.lower())] = 1
            if (concern.leftPole.lower(), concern.rightPole.lower()) in concernUsers:
                concernUsers[(concern.leftPole.lower(), concern.rightPole.lower())] += userID
            else:
                concernUsers[(concern.leftPole.lower(), concern.rightPole.lower())] = userID

        for alternative in grid.alternatives_set.all():
            if alternative:
                temp = alternative.name.lower()
                if temp not in alternatives:
                    alternatives[temp] = 1
                else:
                    alternatives[temp] += 1
                if temp not in alternativeUsers:
                    alternativeUsers[temp] = userID
                else:
                    alternativeUsers[temp] = alternativeUsers[temp] + userID
                    # create an array that contains the tulip (leftconcern, right concern, nPair, nLeftConcern, nRightConcern, isNew), where nPair is the number of times the pair is found, isNew determines if the pair was present in the session grid or not
    for key, value in concernPairs.items():
        leftC, rightC = key
        # check if this pair already exist in the main session grid
        if (leftC, rightC) in oldConcernsPair:
            concernsResult.append((leftC, rightC, value, concerns[leftC], concerns[rightC], False, concernUsers[key]))
        else:
            concernsResult.append((leftC, rightC, value, concerns[leftC], concerns[rightC], True, concernUsers[key]))
            # create an tulip: (anternative, nTimes, isNew) where nTimes is the amount of times each alternative is cited; isNew tells if the alternative was present in the session grid
    for key, value in alternatives.items():
        if key in oldAlternatives:
            alternativeResult.append((key, value, False, alternativeUsers[key]))
        else:
            alternativeResult.append((key, value, True, alternativeUsers[key]))

    return concernsResult, alternativeResult


def __createRangeTableColorMap(globalMax, rangeTable):
    colorEnd = (255, 255, 255)
    colorStart = (240, 72, 74)

    return __createColorMap(100, globalMax, colorStart, colorEnd, rangeTable)


def __createStdTableColorMap(globalMax, stdTable):
    colorEnd = (255, 255, 255)
    colorStart = (240, 72, 74)

    return __createColorMap(100, globalMax, colorStart, colorEnd, stdTable)


def __createColorMap(colorStep, maxValue, startColor, endColor, table):
    # code from http://www.designchemical.com/blog/index.php/jquery/jquery-tutorial-create-a-flexible-data-heat-map/
    yr, yg, yb = startColor
    xr, xg, xb = endColor
    colorMap = []
    for row in table:
        colorRow = []
        if type(row) == type([]):
            for value in row:
                if maxValue != 0:
                    if maxValue <= value:
                        colorRow.append(startColor)
                    else:
                        pos = ceil((value / maxValue) * 100)
                        red = ceil((xr + ((pos * (yr - xr)) / (colorStep - 1))))
                        green = ceil((xg + ((pos * (yg - xg)) / (colorStep - 1))))
                        blue = ceil((xb + ((pos * (yb - xb)) / (colorStep - 1))))
                        colorRow.append((int(red), int(green), int(blue)))
                else:
                    colorRow.append(endColor)
            colorMap.append(colorRow)
        else:
            if maxValue != 0:
                if maxValue <= row:
                    colorMap.append(startColor)
                else:
                    pos = ceil((row / maxValue) * 100)
                    red = ceil((xr + ((pos * (yr - xr)) / (colorStep - 1))))
                    green = ceil((xg + ((pos * (yg - xg)) / (colorStep - 1))))
                    blue = ceil((xb + ((pos * (yb - xb)) / (colorStep - 1))))
                    colorMap.append((int(red), int(green), int(blue)))
            else:
                colorMap.append(endColor)
    return colorMap

def __createPendingResponseData(userObj=None):
    """
    This function is used to create the data required to be used in the pendingResponses.html
    template.

    Arguments:
        userObj: django.contrib.auth.models.User

    Return
        Array
        information: The returned array contains a tulip in each position. Each tulip represents a row.
                     The tulips have two positions. The first position contains a string , this string is a
                     composite of the session name and the facilitator name. The second position contains a
                     string representing the session USID.
    """
    table = None

    if userObj is not None:
        # find out all the sessions that the user is part of
        userSessionRelation = UserParticipateSession.objects.filter(user=userObj)
        if len(userSessionRelation) >= 1:
            for relation in userSessionRelation:
                # now lets check if the session is in a state where a response grid is required
                sessionObj = relation.session
                if sessionObj.state.name == State.objects.getWaitingForAltAndConState().name or sessionObj.state.name == State.objects.getWaitingForWeightsAndRatingsState().name:
                    # now that we know the session is in the correct state lets check if the user has responded.
                    if len(ResponseGrid.objects.filter(user=userObj, session=sessionObj,
                                                       iteration=sessionObj.iteration)) <= 0:
                        if table is None:
                            table = []
                        table.append(
                            (sessionObj.name + ' : ' + sessionObj.facilitator.user.first_name, sessionObj.usid))
    return table


def __validateAltConResponse(request):
    # general validation
    if 'nAlternatives' in request.POST and 'nAlternatives' in request.POST:
        nAlternatives = int(request.POST['nAlternatives'])
        nConcerns = int(request.POST['nConcerns'])

        i = 0
        # check the concern if they are empty or not
        while i < nConcerns:
            # check left pole
            keyName = 'concern_' + str((i + 1)) + '_left'
            if keyName in request.POST:
                if request.POST[keyName] is None or request.POST[keyName].strip() == '':
                    raise ValueError('One or more concerns are empty',
                                     'Error concern ' + keyName + ' has an invalid value: "' + request.POST[
                                         keyName] + '"')
            else:
                raise KeyError('Invalid request, request is missing argument(s)',
                               'Error request is missing argument: ' + keyName)

            # check right pole
            keyName = 'concern_' + str((i + 1)) + '_right'
            if keyName in request.POST:
                if request.POST[keyName] is None or request.POST[keyName].strip() == '':
                    raise ValueError('One or more concerns are empty',
                                     'Error concern ' + keyName + ' has an invalid value: "' + request.POST[
                                         keyName] + '"')
            else:
                raise KeyError('Invalid request, request is missing argument(s)',
                               'Error request is missing argument: ' + keyName)
            i += 1

        i = 0
        # validate the alternatives
        while i < nAlternatives:
            keyName = 'alternative_' + str((i + 1)) + '_name'
            if keyName in request.POST:
                if request.POST[keyName] is None or request.POST[keyName].strip() == '':
                    raise ValueError('One or more alternatives are empty',
                                     'Error alternative ' + keyName + ' has an invalid value: "' + request.POST[
                                         keyName] + '"')
            else:
                raise KeyError('Invalid request, request is missing argument(s)',
                               'Error request is missing argument: ' + keyName)
            i += 1
        return True
    else:
        raise KeyError('Invalid request, request is missing argument(s)',
                       'Error request is missing arguments: nAlternatives: ' + str(
                           'nAlternatives' in request.POST) + ' nConcerns: ' + str(
                           'nConcerns' in request.POST))


def __isGridStateEqualSessionState(sesssionState, gridObj):
    if sesssionState.name == SessionState.AC:
        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
            return True
    elif sesssionState.name == SessionState.RW:
        if gridObj.grid_type == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT:
            return True
    return False


# This function will generate the data that is needed for the participatingSessionsContentGrids.html template
# returns a dictionary that MAY contain the following keys:  previousResponseGrid, sessionGridTable, currentResponseGridTable
def __generateParticipatingSessionsGridsData(sessionObj, iteration_, responseGridRelation):
    data = {}
    currentResponseGridRelation = responseGridRelation.filter(iteration=iteration_)

    # a session grid must always be present, if something goes wrong here the calling function should deal with it
    data['sessionGridTable'] = generateGridTable(sessionObj.sessiongrid_set.all()[iteration_].grid)

    # check to see if a previous response grid should be displayed or not
    if iteration_ >= 2 and iteration_ - 1 > 0:
        previousResponseGridRelation = responseGridRelation.filter(iteration=iteration_ - 1)
        if len(previousResponseGridRelation) >= 1:
            previousResponseGrid = previousResponseGridRelation[0].grid
            if previousResponseGrid is not None and __isGridStateEqualSessionState(sessionObj.state,
                                                                                   previousResponseGrid) and (
                    previousResponseGrid.grid_type == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT or previousResponseGrid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN):
                # generate the data for the previous response grid
                data['previousResponseGrid'] = generateGridTable(previousResponseGridRelation[0].grid)

    # generate response grid data
    # check to see if the user has already send a response grid
    if len(currentResponseGridRelation) >= 1:
        # if he has sent an response generate the data for the grid
        data['currentResponseGridTable'] = generateGridTable(currentResponseGridRelation[0].grid)

    return data


# function saves session grid as user grid. This happens only when the facilitator click "end session" button
# to make the creation of session possible from the session that previously completed
def __saveSessionGridAsUserGrid(request):
    user1 = request.user
    gridObj = userObj = gridType = gridName = None
    isConcernAlternativeResponseGrid = False

    # lets determine what type of grid we are dealing with here
    if 'gridType' in request.POST:
        gridType = request.POST['gridType']
        if gridType == 'session':
            gridType = Grid.GridType.USER_GRID
            userObj = request.user
            if 'sessionUSID' in request.POST and 'iteration' in request.POST:
                isFacilitator = Facilitator.objects.isFacilitator(request.user)
                if isFacilitator:
                    facilitatorObj = Facilitator.objects.get(user=request.user)
                    session = facilitatorObj.session_set.filter(usid=request.POST['sessionUSID'])
                    if len(session) >= 1:
                        session = session[0]
                        gridName = 'Session_' + session.name
                        sessionGridRelation = session.sessiongrid_set.filter(iteration=request.POST['iteration'])
                        if len(sessionGridRelation) >= 1:
                            gridObj = sessionGridRelation[0].grid
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
            gridObj = Grid.objects.get(user=user1, usid=request.POST['gridUSID'])
    else:
        try:
            gridObj = Grid.objects.get(user=user1, usid=request.POST['gridUSID'])
        except:
            pass

    if 'gridName' in request.POST:
        gridCheckNameResult = validateName(request.POST['gridName'])
        if type(gridCheckNameResult) == StringType:
            gridObj.name = gridCheckNameResult
        else:
            # if the grid name isn't a string than it is an error
            return gridCheckNameResult
            # because django will save stuff to the database even if .save() is not called, we need to validate everything before starting to create the objects that will be used to populate the db
    try:
        obj = __validateInputForGrid(request, isConcernAlternativeResponseGrid)
    except:
        __debug_print_stacktrace()
        return False
    nConcerns, nAlternatives, concernValues, alternativeValues, ratioValues = obj

    # update the grid
    if gridObj is not None:
        try:
            isGridCreated = createGrid(userObj, gridType, gridName, nConcerns, nAlternatives, concernValues,
                                       alternativeValues, ratioValues, True)
            if isGridCreated:
                return True
        except:
            return False
    else:
        return False


# this function will generate the data for the ResultRatingWeightTablesData or ResultAlternativeConcernTableData template data objects
# this function also returns one of those objects depending on the type of requested the results will be based on.
# if no results were found none is returned
def __generateSessionIterationResult(request, sessionObj, iterationObj):
    if sessionObj.iteration < iterationObj:
        raise WrongSessionIteration('Session does not contain that iteration')

    # let's find all the response grids
    responseGridRelation = sessionObj.responsegrid_set.filter(iteration=iterationObj)
    if len(responseGridRelation) >= 1:
        gridType = responseGridRelation[0].grid.grid_type
        if gridType == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN:
            try:
                # check to see if we have a sesssion grid for the iteration
                templateData = ResultAlternativeConcernTableData()
                sessionGrid = SessionGrid.objects.filter(session=sessionObj, iteration=iterationObj)
                if len(sessionGrid) >= 1:
                    sessionGrid = sessionGrid[0].grid
                    templateData.concerns, templateData.alternatives = __generateAlternativeConcernResultTable(
                        responseGridRelation, sessionGrid)
                else:
                    templateData.concerns, templateData.alternatives = __generateAlternativeConcernResultTable(
                        responseGridRelation)
                if len(templateData.concerns) >= 1:
                    return templateData
                else:
                    return None
            except Exception as e:
                __debug_print_stacktrace()
                raise e
        elif gridType == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT:
            # create a list with a matrix of ratios in each position of the list.
            ratioMatrices = []
            weightMatrices = []
            tempMatrix = []

            # first lets add the rations that are in the session grid to the list
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            concerns = sessionObj.sessiongrid_set.filter(iteration=iterationObj)[0].grid.concerns_set.all()
            alternatives = sessionObj.sessiongrid_set.filter(iteration=iterationObj)[0].grid.alternatives_set.all()
            nConcerns = len(concerns)
            nAlternatives = len(alternatives)
            nResponseGrids = len(responseGridRelation)

            i = 0
            j = 0
            tempWeightRow = []
            while i < nConcerns:
                tempRatioRow = []
                tempWeightRow.append(concerns[i].weight)
                while j < nAlternatives:
                    tempRatioRow.append(Ratings.objects.get(concern=concerns[i], alternative=alternatives[j]).rating)
                    j += 1
                tempMatrix.append(tempRatioRow)
                j = 0
                i += 1
            ratioMatrices.append(tempMatrix)
            weightMatrices.append([tempWeightRow])
            tempMatrix = []
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # now lets do the same for the response grids
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            i = 0
            j = 0
            k = 0
            tempWeightRow = []

            while i < nResponseGrids:
                respGrid = responseGridRelation[i].grid
                concerns = respGrid.concerns_set.all()
                alternatives = respGrid.alternatives_set.all()
                nConcerns = len(concerns)
                nAlternatives = len(alternatives)
                while j < nConcerns:
                    tempRatioRow = []
                    tempWeightRow.append(concerns[j].weight)
                    while k < nAlternatives:
                        tempRatioRow.append(
                            Ratings.objects.get(concern=concerns[j], alternative=alternatives[k]).rating)
                        k += 1
                    k = 0
                    j += 1
                    tempMatrix.append(tempRatioRow)
                j = 0
                i += 1
                weightMatrices.append([tempWeightRow])
                ratioMatrices.append(tempMatrix)
                tempMatrix = []
                tempWeightRow = []
            i = 0
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # calculate the rage, mean and std for the weight and ratio
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            meanRatioMatrix = __calculateMeans(ratioMatrices)
            rangeRatioMatrix = __calculateRange(ratioMatrices)
            stdRatioMatrix = __calculateStandardDeviation(ratioMatrices, meanRatioMatrix)
            meanWeightMatrix = __calculateMeans(weightMatrices)
            rangeWeightMatrix = __calculateRange(weightMatrices)
            stdWeightMatrix = __calculateStandardDeviation(weightMatrices, meanWeightMatrix)
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # first lets create the header
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            header = []
            for alternative in sessionObj.sessiongrid_set.filter(iteration=iterationObj)[0].grid.alternatives_set.all():
                header.append(alternative.name)
                #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # generate color map
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            #minMaxRangeRatio= __findMinMaxInMatrix__(rangeRatioMatrix)
            minMaxRangeWeight = __findMinMaxInMatrix(stdRatioMatrix)

            #minMaxStdRatio= __findMinMaxInMatrix__(rangeWeightMatrix)
            minMaxStdWeight = __findMinMaxInMatrix(stdWeightMatrix)

            rangeRatioColorMap = __createRangeTableColorMap(4,
                                                            rangeRatioMatrix)  # for as the max range is 1-5= 4 (as right now the user can only use the numbers between 1 and 5)
            rangeWeightColorMap = __createRangeTableColorMap(minMaxRangeWeight[1], rangeWeightMatrix[0])
            stdRatioColorMap = __createStdTableColorMap(4, stdRatioMatrix)
            stdWeightColorMap = __createStdTableColorMap(minMaxStdWeight[1], stdWeightMatrix[0])
            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # generate the js for the chart in the page
            #>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<
            participantNames = []
            # retrieve all the names
            while i < len(responseGridRelation):
                # the initial db didn't link a response grid to a user direcly, this has changed now, but the code needs to take care of this difference. (4/7/2012)
                if responseGridRelation[i].grid.user is not None:
                    participantNames.append(responseGridRelation[i].grid.user.first_name)
                else:
                    participantNames.append(responseGridRelation[i].user.first_name)
                i += 1
            ratioJsChartData, weightJsChartData = __createJSforRatioWeightSessionResultsChart(ratioMatrices,
                                                                                              weightMatrices,
                                                                                              participantNames)

            #>>>>>>>>>>>>>>>>>>>>>>end<<<<<<<<<<<<<<<<<<

            # clue everything together now and return the page
            tableRatingRangeColor = []  # final table with the value to be displayed, the background color and js code
            tableRatingStdColor = []  # final table with the value to be displayed, the background color and js code
            tableRatingMean = []  # final table with the value to be displayed and js code
            tableWeightMean = []  # final table with the weights and js code
            tableWeightStd = []  # final table with the weights and js code
            tableWeightRange = []  # final table with the weights and js code
            i = 0

            # reverse the weight color maps, this is done because we use pop in the template!!!
            rangeWeightColorMap.reverse()
            stdWeightColorMap.reverse()

            while i < nConcerns:
                rowRange = []
                rowStd = []
                rowMean = []
                tableWeightMean.append((meanWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[(
                    nConcerns - 1) - i]))  # meanWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                tableWeightStd.append((stdWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[(
                    nConcerns - 1) - i]))  # stdWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                tableWeightRange.append((rangeWeightMatrix[0][(nConcerns - 1) - i], weightJsChartData[(
                    nConcerns - 1) - i]))  # rangeWeightMatrix[0][], it is always [0] as in truth the matrix is not really a matrix but a 1d list, the list needs to be reserved because we use pop in the template
                # create a tulip with the value that should be displayed in the td and the color of the background for each cell in the row
                while k < nAlternatives:
                    rowRange.append((rangeRatioMatrix[i][k], rangeRatioColorMap[i][k], ratioJsChartData[i][k]))
                    rowStd.append((stdRatioMatrix[i][k], stdRatioColorMap[i][k], ratioJsChartData[i][k]))
                    rowMean.append((meanRatioMatrix[i][k], ratioJsChartData[i][k]))
                    k += 1
                k = 0
                # add the concerns to the range, mean and std tables
                rightPole = concerns[i].rightPole
                leftPole = concerns[i].leftPole
                rowStd.insert(0, (leftPole, None))
                rowStd.append((rightPole, None))
                rowMean.insert(0, (leftPole, None))
                rowMean.append((rightPole, None))
                rowRange.insert(0, (leftPole, None))
                rowRange.append((rightPole, None))
                tableRatingRangeColor.append(rowRange)
                tableRatingStdColor.append(rowStd)
                tableRatingMean.append(rowMean)
                i += 1

            # put all the data into objects for the template
            rangeData = ResultRatingWeightTableData()
            meanData = ResultRatingWeightTableData()
            stdData = ResultRatingWeightTableData()

            rangeData.table = tableRatingRangeColor
            rangeData.headers = header
            rangeData.weights = tableWeightRange
            rangeData.weightColorMap = rangeWeightColorMap
            rangeData.tableHead = 'Range'
            rangeData.useColorMap = True

            meanData.table = tableRatingMean
            meanData.headers = header
            meanData.weights = tableWeightMean
            meanData.tableHead = 'Mean'

            stdData.table = tableRatingStdColor
            stdData.headers = header
            stdData.weights = tableWeightStd
            stdData.weightColorMap = stdWeightColorMap
            stdData.tableHead = 'Standard Deviation'
            stdData.useColorMap = True

            templateData = ResultRatingWeightTablesData()
            templateData.rangeData = rangeData
            templateData.meanData = meanData
            templateData.stdData = stdData

            return templateData
        else:
            raise WrongGridType('Unexpected type grid found')
    else:
        return None


def __debug_print_stacktrace():
    """
    TODO: Switch to the default logging system
    """
    if DEBUG:
        print "Exception in user code:"
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60
