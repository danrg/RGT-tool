from RGT.gridMng.models import UserParticipateSession, State, ResponseGrid


class ParticipatingSessionsData(object):
    sessions = None
    pendingResponses = None

    def __init__(self, user):
        participations = user.userparticipatesession_set.all()
        self.sessions = [participation.session for participation in participations]
        self.pendingResponses = self.__get_sessions_with_pending_responses(user)

    def __get_sessions_with_pending_responses(self, user):
        """
        This function is used to create the data required to be used in the pendingResponses.html
        template.

        Arguments:
            user: django.contrib.auth.models.User

        Return
            List
            information: The returned array contains all sessions the given user needs to respond to
        """
        participations = user.userparticipatesession_set.all()
        return [p.session for p in participations if p.has_pending_response(user)]


        