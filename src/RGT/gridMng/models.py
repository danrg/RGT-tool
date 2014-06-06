import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from RGT.gridMng.error.userAlreadyParticipating import UserAlreadyParticipating
from RGT.gridMng.error.wrongState import WrongState
from RGT.gridMng.error.userIsFacilitator import UserIsFacilitator
from RGT.gridMng.session.state import State as SessionState
from RGT.settings import SESSION_USID_KEY_LENGTH, GRID_USID_KEY_LENGTH
from utility import generateRandomString
from datetime import datetime
from django.utils.timezone import utc
from django.core.urlresolvers import reverse

#grid manager
class GridManager(models.Manager):

    @transaction.atomic
    def create_grid(self, user, type, concernValues=None, alternativeValues=None, createRatings=False, ratioValues=None, **kwargs):
        if kwargs['name'] is None:
            del kwargs['name']
        grid = self.create(user=user, grid_type=type, **kwargs)

        # Create related objects
        if alternativeValues is not None:
            alternatives = [Alternatives(grid=grid, name=alt) for alt in alternativeValues]
            Alternatives.objects.bulk_create(alternatives)
        if concernValues is not None:
            concerns = [Concerns(grid=grid, leftPole=c[0],rightPole=c[1], weight=c[2]) for c in concernValues]
            Concerns.objects.bulk_create(concerns)
        if createRatings and ratioValues is not None:
            # Retrieve them again to populate primary keys (still better than saving each object seperately above)
            concerns = Concerns.objects.filter(grid=grid).all()
            alternatives = Alternatives.objects.filter(grid=grid).all()
            ratings = []
            for i, concern in enumerate(concerns):
                 for j, alternative in enumerate(alternatives):
                     ratings.append(Ratings(concern=concern, alternative=alternative, rating=ratioValues[i][j]))
            Ratings.objects.bulk_create(ratings)

        return grid

    def duplicateGrid(self, gridObj, userObj=None, gridName=None, gridType=None):
        #create new grid
        if userObj:
            if gridName != None:
                newGrid = Grid(user=userObj, description=gridObj.description, name=gridName,
                               dendogram=gridObj.dendogram, grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
            else:
                newGrid = Grid(user=userObj, description=gridObj.description, name=gridObj.name,
                               dendogram=gridObj.dendogram, grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
        else:
            if gridName != None:
                newGrid = Grid(description=gridObj.description, name=gridName, dendogram=gridObj.dendogram,
                               grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
            else:
                newGrid = Grid(description=gridObj.description, name=gridObj.name, dendogram=gridObj.dendogram,
                               grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
        if gridType != None:
            newGrid.grid_type = gridType
        if newGrid:
            try:
                newGrid.save()
                newConcerns = []
                newAlternatives = []
                oldConcerns = gridObj.concerns_set.all()
                oldAlternatives = gridObj.alternatives_set.all()
                lenOldConcerns = len(oldConcerns)
                lenOldAlternatives = len(oldAlternatives)
                for concern in oldConcerns:
                    temp = Concerns.objects.create(grid=newGrid, leftPole=concern.leftPole, rightPole=concern.rightPole,
                                                   weight=concern.weight)
                    newConcerns.append(temp)
                for alternative in oldAlternatives:
                    temp = Alternatives.objects.create(grid=newGrid, name=alternative.name,
                                                       description=alternative.description)
                    newAlternatives.append(temp)
                i = 0
                j = 0
                while i < lenOldConcerns:
                    while j < lenOldAlternatives:
                        oldRating = Ratings.objects.get(concern=oldConcerns[i], alternative=oldAlternatives[j])
                        Ratings.objects.create(concern=newConcerns[i], alternative=newAlternatives[j],
                                               rating=oldRating.rating)
                        j += 1
                    j = 0
                    i += 1
                return newGrid
            except:
                #delete what ever we had
                if newGrid:
                    newGrid.delete()
        return False


#grid model
class Grid(models.Model):
    usid = models.CharField(max_length=20, unique=True, default=lambda: generateRandomString(GRID_USID_KEY_LENGTH))
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=30, default='untitled')
    description = models.TextField(null=True)
    dendogram = models.TextField(null=True)
    dateTime = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc), null=True)
    grid_types = (('u', 'User grid'), ('s', 'Session grid'), ('ac', 'Response grid, Alternative/Concern'),
                  ('rw', 'Response grid, Ratings/Weight'), ('cg', 'Composite Grid') )
    grid_type = models.CharField(max_length=2, choices=grid_types, default='u')
    objects = GridManager()

    def get_absolute_url(self):
        return reverse('RGT.gridMng.views.show_grid', args=[self.usid])

    def get_alternative_total_rating_tuples(self):
        """ Return a collection containing a tuple for each alternative containing that alternative and the total
         weighted rating of that alternative. E.g. in a grid for programming languages, it returns a collection as
         (['Python', 1], ['Java', 2], ['PHP', 5])
        """
        alts_and_ratings = []
        for alternative in self.alternatives_set.all():
            total_rating = alternative.get_total_rating()
            alts_and_ratings.append((alternative.name, total_rating))

        return alts_and_ratings

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']

    class GridType(object):
        USER_GRID = 'u'
        SESSION_GRID = 's'
        RESPONSE_GRID_ALTERNATIVE_CONCERN = 'ac'
        RESPONSE_GRID_RATING_WEIGHT = 'rw'
        COMPOSITE_GRID = 'cg'


class Alternatives(models.Model):
    grid = models.ForeignKey(Grid)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    def get_total_rating(self):
        total_rating = 0
        concerns = self.grid.concerns_set.all()
        for concern in concerns:
            rating = Ratings.objects.get(concern=concern, alternative=self).rating
            total_rating += rating * concern.weight / 100.0

        return total_rating

    class Meta:
        ordering = ['id']


class Composite(models.Model):
    compid= models.CharField(max_length=20, unique=False)
    user= models.ForeignKey(User, null= True)
    rule = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['id']


class Rule:
    """ A rule used in the composite grid wizard. It provides functionality for creation based on a list of alternatives
     and ordering based on the total rating of the alternatives.
    """

    def __init__(self, alternatives, total_rating):
        self.name = '(' + ', '.join(alternatives) + ')'
        self.total_rating = total_rating

    def __lt__(self, other):
        return self.total_rating < other.total_rating

class Concerns(models.Model):
    grid = models.ForeignKey(Grid)
    leftPole = models.CharField(max_length=150, null=True)
    rightPole = models.CharField(max_length=150, null=True)
    weight = models.FloatField(null=True)

    def __unicode__(self):
        return '%s -- %s (%f)' % (self.leftPole, self.rightPole, self.weight)

    class Meta:
        ordering = ['id']


class Ratings(models.Model):
    concern = models.ForeignKey(Concerns)
    alternative = models.ForeignKey(Alternatives)
    rating = models.FloatField(null=True)

    class Meta:
        unique_together = ('concern',
                           'alternative') # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used

#manager for state
class StateManager(models.Manager):
    def getInitialState(self):
        return self.get(name='initial')

    def getCheckState(self):
        return self.get(name='check')

    def getWaitingForAltAndConState(self):
        return self.get(name='waitingForAltAndCon')

    def getWaitingForWeightsAndRatingsState(self):
        return self.get(name='waitingForWeightsAndRatings')

    def getFinishState(self):
        return self.get(name='finish')

    def respondable(self):
        return self.filter(name__in=(SessionState.AC, SessionState.RW))

#model for state
class State(models.Model):
    name = models.CharField(max_length=30)
    objects = StateManager()
    verbose_names = { SessionState.INITIAL: 'Invitation', SessionState.AC: 'Alternatives / Concerns',
                      SessionState.RW: 'Ratings / Weights', SessionState.FINISH: 'Closed',
                      SessionState.CHECK: 'Check values'}
    participation_statuses = {SessionState.INITIAL: 'Waiting for users to join',
                              SessionState.AC: 'Waiting for Alternative and concerns',
                              SessionState.RW: 'Waiting for Ratings and Weights', SessionState.FINISH: 'Closed',
                              SessionState.CHECK: 'Checking previous results'}

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.verbose_names.get(self.name)

    def is_finishable(self):
        """ Returns true if this session is in a state which the facilitator can finish, i.e. (A/C or R/W) """
        return self.name in (SessionState.AC, SessionState.RW)

    def can_be_responded_to(self):
        """ Returns true if this session is in a state where participants can respond, i.e. (A/C or R/W) """
        return self.is_finishable()

    def get_participation_status(self):
        """ Return a user-friendly description of the current state for participators """
        return self.participation_statuses.get(self.name)

    def is_alt_and_con_state(self):
        return self.name == SessionState.AC

    def is_ratings_weights_state(self):
        return self.name == SessionState.RW

    def is_check_values_state(self):
        return self.name == SessionState.CHECK

    def is_equal_to_grid_state(self, grid):
        if self.is_alt_and_con_state():
            return grid.grid_type == Grid.GridType.RESPONSE_GRID_ALTERNATIVE_CONCERN
        elif self.is_ratings_weights_state():
            return grid.grid_type == Grid.GridType.RESPONSE_GRID_RATING_WEIGHT
        return False

    def get_possible_next_states(self):
        if self.name in (SessionState.INITIAL, SessionState.AC, SessionState.RW):
            return (SessionState.CHECK)
        elif self.name == SessionState.CHECK:
            return (SessionState.AC, SessionState.RW, SessionState.FINISH)
        else:
            return ()

#manager for facilitator
class FacilitatorManager(models.Manager):
    def isFacilitator(self, userObj):
        facilitator, created = self.get_or_create(user=userObj)
        return not created and facilitator.session_set.count() > 0

#model for facilitator
class Facilitator(models.Model):
    user = models.ForeignKey(User, unique=True)
    objects = FacilitatorManager()

    class Meta:
        ordering = ['id']

class SessionManager(models.Manager):

    @transaction.atomic
    def create_session(self, facilitating_user, original_grid, name=None, show_results=None):
        if name is None or name == '':
            name = 'untitled'
        if show_results is None:
            show_results = False

        facilitator, created = Facilitator.objects.get_or_create(user=facilitating_user)
        usid = generateRandomString(SESSION_USID_KEY_LENGTH)
        state = State.objects.getInitialState()
        invitation_key = str(uuid.uuid4())

        session = self.create(usid=usid, facilitator=facilitator, name=name, showResult=show_results, state=state, invitationKey=invitation_key)
        duplicateGrid = Grid.objects.duplicateGrid(original_grid, gridType=Grid.GridType.SESSION_GRID)
        SessionGrid.objects.create(session=session, grid=duplicateGrid, iteration=0)

        return session

    def with_participation(self, user):
        participations = user.userparticipatesession_set
        return self.filter(id__in=participations.values('session_id'))

    def with_facilitator(self, user):
        facilitator, created = Facilitator.objects.get_or_create(user=user)
        return self.filter(facilitator=facilitator)

    def with_pending_responses(self, user):
        respondable_states = State.objects.respondable()
        return self.with_participation(user).filter(state__in=respondable_states)

class Session(models.Model):
    usid = models.CharField(max_length=20, unique=True)
    facilitator = models.ForeignKey(Facilitator)
    iteration = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State)
    showResult = models.BooleanField(default=False)
    invitationKey = models.TextField(null=True)
    description = models.TextField(null=True)
    objects = SessionManager()

    class Meta:
        ordering = ['id']

    def getParticipators(self):
        return [participator.user for participator in self.userparticipatesession_set.all()]

    def addParticipant(self, user):
        if(self.facilitator.user == user):
            raise UserIsFacilitator(user, self)
        if self.userparticipatesession_set.filter(user=user).exists():
            raise UserAlreadyParticipating(user, self)
        if self.has_started():
            raise WrongState('Can\'t add user in session with state:' + self.state.name, sessionState=self.state)

        UserParticipateSession.objects.create(session=self, user=user)

    def changeState(self, new_state):
        if new_state.name in self.state.get_possible_next_states():
            if self.state.can_be_responded_to():
                SessionIterationState.objects.create_from_session(self)
            self.state = new_state
            if new_state.is_check_values_state():
                self.__goToNextIteration()
            self.save()
        else:
            raise WrongState('Current sessions state is %s, can\'t go from that state to %s' % (self.state, new_state))

    def get_absolute_url(self):
        return reverse('RGT.gridMng.session.views.show_detailed', args=[self.usid])

    def getUsersThatDidNotRespondedRequest(self):
        repondedUsers = set(self.getRespondents())
        users = set(self.getParticipators())
        return users - repondedUsers

    def getRespondents(self):
        responseGridRelations = ResponseGrid.objects.filter(session=self, iteration=self.iteration)
        return [{'user': relation.user, 'dateTime': relation.grid.dateTime} for relation in responseGridRelations]

    def get_descriptive_name(self):
        """ Returns a user friendly descriptive name of this session """
        return '%s: %s' % (self.facilitator.user.get_full_name(), self.name)

    def has_started(self):
        """ Returns True if this session has started (i.e. not in invitation state) """
        return self.state.name != SessionState.INITIAL

    def is_closed(self):
        """ Returns True if this session is in the finish state """
        return self.state.name == SessionState.FINISH

    def get_iteration_states(self):
        """ Returns all iteration states for this session """
        return self.sessioniterationstate_set.all().order_by('iteration')

    def get_session_grid(self):
        """ Returns the session grid of the current iteration """
        return self.sessiongrid_set.get(iteration=self.iteration).grid

    def get_iterations_with_results(self):
        """ Returns a list of all the iterations for which this session has results """
        return [x.iteration for x in self.responsegrid_set.all()]

    def __unicode__(self):
        return self.name

    def __goToNextIteration(self):
        sessionGrid = SessionGrid.objects.get(session=self, iteration=self.iteration).grid
        newSessionGrid = Grid.objects.duplicateGrid(sessionGrid)
        self.iteration += 1
        SessionGrid.objects.create(iteration=self.iteration, session=self, grid=newSessionGrid)


class SessionIterationStateManager(models.Manager):
    def create_from_session(self, session):
        SessionIterationState.objects.create(iteration=session.iteration, session=session,state=session.state)


class SessionIterationState(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    state = models.ForeignKey(State)
    objects = SessionIterationStateManager()
    class Meta:
        unique_together = ('iteration', 'session')
        ordering = ['id']


class UserParticipateSession(models.Model):
    session = models.ForeignKey(Session)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('session',
                           'user') # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']

    def has_pending_response(self, user):
        if self.session.state.can_be_responded_to():
            try:
                ResponseGrid.objects.get_current(self.session, self.user)
                return False
            except ResponseGrid.DoesNotExist:
                return True

    def __unicode__(self):
        return "%s participating in %s" % (self.user, self.session)


#the name of this class in the orm is: iterationHasGridInSession
class SessionGrid(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    grid = models.ForeignKey(Grid)

    class Meta:
        unique_together = ('iteration',
                           'session') # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']

class ResponseGridManager(models.Manager):
    def get_iterations_with_grids(self, session, user):
        """ Returns a list of all the iterations in the given session for which the given user has responded """
        return [grid.iteration for grid in self.filter(session=session, user=user)]

    def get_current(self, session, user):
        """ Returns the response grid from the given user of the latest iteration of the given session """
        return user.responsegrid_set.get(session=session, iteration=session.iteration)

#the name of this class in the orm is: UserHasGridInIteration
class ResponseGrid(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    grid = models.ForeignKey(Grid)
    user = models.ForeignKey(User)
    objects = ResponseGridManager()

    class Meta:
        unique_together = ('iteration', 'user',
                           'session') # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']

