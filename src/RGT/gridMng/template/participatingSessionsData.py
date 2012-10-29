from RGT.gridMng.template.pedingResponsesData import PedingResponsesData

class ParticipatingSessionsData(PedingResponsesData, object):

    sessions= None # list used to create the menu for the participant that displays the session which he is participating. format: [(session_uid, 'facilitatorName:sessionName'), ...] 
    hasSessions= False    

    def __init__(self):
        pass
        