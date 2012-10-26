class MySessionsContentData(object):

    sessionName= None
    invitationKey= None
    iteration= None
    state= None
    iterationValueType= None #data used to generate the menu the facilitator uses to select the results of previous iterations. format is {{'stateNameKey':SessionState, 'stateName':'state name'}, ......}
    isSessionClose= False
    hasSessionStarted= False
    showRequestButtons= False
    showFinishButton= False
    showCloseSessionButton= False
    savaGridSession= False
   
    def __init__(self):
        pass
        