from RGT.gridMng.template.participatingSessionsContentGridsData import ParticipatingSessionsContentGridsData

class ParticipatingSessionsContentData(ParticipatingSessionsContentGridsData, object):

    iteration= None #integer
    iterations= None #list containing an integer representing each iteration that is used to create the menu that the participant uses to navigate between response. format [1,2,3,....]
    sessionStatus= None #string
    showNParticipantsAndResponces= None #boolean
    nReceivedResponses= None #integer
    nParticipants= None #integer
    responseStatus= None #string
    dateTime= None #django time object
    hideSaveResponseButton= False

    def __init__(self):
        pass
        