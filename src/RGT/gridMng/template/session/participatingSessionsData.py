
class ParticipatingSessionsData(object):

    sessions= None # list used to create the menu for the participant that displays the session which he is participating. format: [(session_uid, 'facilitatorName:sessionName'), ...] 
    pendingResponses= None #pendingResponsesData object
    hasSessions= False    

    def __init__(self):
        pass
        