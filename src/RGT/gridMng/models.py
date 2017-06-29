import uuid

from copy import deepcopy

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.db import transaction

from ..settings import SESSION_USID_KEY_LENGTH, GRID_USID_KEY_LENGTH
from .error.userAlreadyParticipating import UserAlreadyParticipating
from .error.userIsFacilitator import UserIsFacilitator
from .error.wrongState import WrongState
from .session.state import State as SessionState
from utility import generateRandomString
from datetime import datetime
from django.utils.timezone import utc
from django.core.urlresolvers import reverse


class GridManager(models.Manager):
    @transaction.atomic
    def create_grid(self, user, type, concernValues=None, alternativeValues=None, createRatings=False, ratioValues=None,
                    **kwargs):
        if kwargs['name'] is None:
            del kwargs['name']
        grid = self.create(user=user, grid_type=type, **kwargs)

        # Create related objects
        if alternativeValues is not None:
            alternatives = [Alternatives(grid=grid, name=alt) for alt in alternativeValues]
            Alternatives.objects.bulk_create(alternatives)
        if concernValues is not None:
            concerns = [Concerns(grid=grid, leftPole=c[0], rightPole=c[1], weight=c[2]) for c in concernValues]
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
        # create new grid
        if userObj:
            if gridName is not None:
                newGrid = Grid(user=userObj, description=gridObj.description, name=gridName,
                               dendogram=gridObj.dendogram, grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
            else:
                newGrid = Grid(user=userObj, description=gridObj.description, name=gridObj.name,
                               dendogram=gridObj.dendogram, grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
        else:
            if gridName is not None:
                newGrid = Grid(description=gridObj.description, name=gridName, dendogram=gridObj.dendogram,
                               grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
            else:
                newGrid = Grid(description=gridObj.description, name=gridObj.name, dendogram=gridObj.dendogram,
                               grid_type=gridObj.grid_type, usid=generateRandomString(20),
                               dateTime=datetime.utcnow().replace(tzinfo=utc))
        if gridType is not None:
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
                # delete what ever we had
                if newGrid:
                    newGrid.delete()
        return False


class Grid(models.Model):
    # from django.contrib.auth import get_user_model
    # User = get_user_model()

    usid = models.CharField(max_length=20, unique=True, default=lambda: generateRandomString(GRID_USID_KEY_LENGTH))

    from django.contrib.auth.models import User

    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=30, default='untitled')
    description = models.TextField(null=True)
    dendogram = models.TextField(null=True)
    dateTime = models.DateTimeField(auto_now_add=True, null=True)
    grid_types = (('u', 'User grid'), ('s', 'Session grid'), ('ac', 'Response grid, Alternative/Concern'),
                  ('rw', 'Response grid, Ratings/Weight'), ('cg', 'Composite Grid'))
    grid_type = models.CharField(max_length=2, choices=grid_types, default='u')
    objects = GridManager()

    def get_absolute_url(self):
        # return reverse('RGT.gridMng.views.show_grid', args=[self.usid])
        return reverse('views.show_grid', args=[self.usid])

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
        app_label = 'gridMng'

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
        return unicode(self.name)

    def get_total_rating(self):
        total_rating = 0
        concerns = self.grid.concerns_set.all()
        for concern in concerns:
            rating = Ratings.objects.get(concern=concern, alternative=self).rating
            total_rating += rating * concern.weight / 100.0

        return total_rating

    def save(self, *args, **kwargs):
        if not self.pk:
            old_name = ""
        else:
            old_name = Alternatives.objects.get(pk=self.pk).name
        super(Alternatives, self).save(*args, **kwargs)
        if old_name != self.name:
            AlternativeDiff.objects.create(related_id=self.id, grid=self.grid, old_name=old_name, new_name=self.name)

    def delete(self, *args, **kwargs):
        for r in self.ratings_set.all():
            r.delete(grid=self.grid)

        old_name = self.name
        old_id = self.id
        super(Alternatives, self).delete(*args, **kwargs)
        AlternativeDiff.objects.create(related_id=old_id, grid=self.grid, old_name=old_name, new_name="")

    def __lt__(self, other):
        return self.id < other.id

    class Meta:
        ordering = ['id']
        app_label = 'gridMng'


class Revision:
    grid = None
    date = None
    aggregations = None

    def __init__(self, grid, date):
        self.grid = grid
        self.date = date
        self.aggregations = {}

    def __unicode__(self):
        items = []
        for key in self.aggregations.keys():
            operation = key.replace("Diff_", "s ")
            items.append('%s: %i' % (operation, self.aggregations.get(key)))

        if items:
            return ", ".join(sorted(items))
        else:
            return "Grid created"


class SubclassingQuerySet(QuerySet):
    """ Needed for polymorphism, see http://stackoverflow.com/questions/5360995/polymorphism-in-django-models
    """

    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class DiffManager(models.Manager):
    def daily_revisions(self, grid):
        rev_grid = GridProxy(grid)
        revisions = []
        previous_date = None
        diffs = grid.diff_set.all().order_by('-datetime')
        diff_aggregations = {}
        for diff in diffs:
            key = self.__aggregations_key(diff)
            current = diff_aggregations.get(key, 0)
            diff_aggregations[key] = current + 1
            if diff.datetime.date() != previous_date:
                if revisions:
                    revisions[-1].aggregations = deepcopy(diff_aggregations)
                    diff_aggregations = {}
                revisions.append(Revision(deepcopy(rev_grid), diff.datetime.date()))
            previous_date = diff.datetime.date()
            rev_grid = diff.revert(rev_grid)
        if revisions:
            revisions[-1].aggregations = deepcopy(diff_aggregations)
        revisions.append(Revision(rev_grid, grid.dateTime.date()))

        return revisions

    def get_query_set(self):
        return SubclassingQuerySet(self.model)

    def __aggregations_key(self, diff):
        name = diff.__class__.__name__
        if diff.is_addition_diff():
            type = "added"
        elif diff.is_deletion_diff():
            type = "deleted"
        else:
            type = "changed"

        return "%s_%s" % (name, type)


class Diff(models.Model):
    related_id = models.IntegerField()
    grid = models.ForeignKey(Grid)
    datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    objects = DiffManager()

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Diff, self).save(*args, **kwargs)

    def is_addition_diff(self):
        return not any(self.old_values()) and any(self.new_values())

    def is_deletion_diff(self):
        return any(self.old_values()) and not any(self.new_values())

    def is_change_diff(self):
        return any(self.old_values()) and any(self.new_values())

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if model == Diff:
            return self
        return model.objects.get(id=self.id)

    class Meta:
        app_label = 'gridMng'


class AlternativeDiff(Diff):
    old_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)
    objects = DiffManager()

    def old_values(self):
        return self.old_name

    def new_values(self):
        return self.new_name

    def __unicode__(self):
        if self.old_name == "":
            change_str = "added %s" % self.new_name
        elif self.new_name == "":
            change_str = "removed %s" % self.old_name
        else:
            change_str = "changed %s to %s" % (self.old_name, self.new_name)
        return "%s (alt %i): %s" % (self.grid, self.related_id, change_str)

    def revert(self, grid):
        reverted = GridProxy(grid)
        if self.is_addition_diff():
            reverted.alternatives = [a for a in grid.alternatives if self.related_id != a.id]
        elif self.is_deletion_diff():
            a = Alternatives(grid_id=grid.id, name=self.old_name)
            a.id = self.related_id
            reverted.alternatives.append(a)
            reverted.alternatives.sort()
        else:
            a = next(a for a in reverted.alternatives if a.id == self.related_id)
            a.name = self.old_name

        return reverted

    class Meta:
        app_label = 'gridMng'


class ConcernDiffManager(models.Manager):
    def daily_revisions(self, grid):
        rev_grid = GridProxy(grid)
        revisions = []
        previous_date = None
        diffs = grid.concerndiff_set.all().order_by('-datetime')
        for diff in diffs:
            if diff.datetime.date() != previous_date:
                revisions.append(Revision(deepcopy(rev_grid), diff.datetime.date()))
            previous_date = diff.datetime.date()
            rev_grid = diff.revert(rev_grid)

        revisions.append(Revision(deepcopy(rev_grid), grid.dateTime.date()))
        return revisions


class ConcernDiff(Diff):
    old_leftPole = models.CharField(max_length=150)
    old_rightPole = models.CharField(max_length=150)
    old_weight = models.FloatField(null=True)
    new_leftPole = models.CharField(max_length=150)
    new_rightPole = models.CharField(max_length=150)
    new_weight = models.FloatField(null=True)
    objects = DiffManager()

    def old_values(self):
        return (self.old_leftPole, self.old_rightPole, self.old_weight)

    def new_values(self):
        return (self.new_leftPole, self.new_rightPole, self.new_weight)

    def revert(self, grid):
        reverted = GridProxy(grid)
        if self.is_addition_diff():
            reverted.concerns = [c for c in grid.concerns if self.related_id != c.id]
        elif self.is_deletion_diff():
            c = Concerns(grid_id=grid.id, leftPole=self.old_leftPole, rightPole=self.old_rightPole,
                         weight=self.old_weight)
            c.id = self.related_id
            reverted.concerns.append(c)
            reverted.concerns.sort()
        else:
            c = next(c for c in reverted.concerns if c.id == self.related_id)
            c.leftPole = self.old_leftPole
            c.rightPole = self.old_rightPole
            c.weight = self.old_weight

        return reverted

    class Meta:
        app_label = 'gridMng'


class RatingDiff(Diff):
    # related_id from Diff class acts as relation id to Alternative
    concern_id = models.IntegerField()
    old_rating = models.FloatField(null=True)
    new_rating = models.FloatField(null=True)
    objects = DiffManager()

    def old_values(self):
        return (self.old_rating,)

    def new_values(self):
        return (self.new_rating,)

    def revert(self, grid):
        reverted = GridProxy(grid)
        if self.is_addition_diff():
            ratings = [r for r in grid.ratings if
                       self.related_id != r.alternative_id or self.concern_id != r.concern_id]
        elif self.is_deletion_diff():
            r = Ratings(alternative_id=self.related_id, concern_id=self.concern_id, rating=self.old_rating)
            reverted.ratings.append(r)
        else:
            r = next(
                r for r in reverted.ratings if r.alternative_id == self.related_id and r.concern_id == self.concern_id)
            r.rating = self.old_rating
        return reverted

    class Meta:
        app_label = 'gridMng'


class GridProxy:
    id = None
    alternatives = None
    concerns = None
    ratings = None

    def __init__(self, original_grid):
        self.id = original_grid.id
        if isinstance(original_grid, Grid):
            self.alternatives = list(original_grid.alternatives_set.all())
            self.concerns = list(original_grid.concerns_set.all())
            self.ratings = list(Ratings.objects.filter(alternative__grid_id=original_grid.id))
        else:
            self.alternatives = original_grid.alternatives
            self.concerns = original_grid.concerns
            self.ratings = original_grid.ratings


class Composite(models.Model):
    compid = models.CharField(max_length=20, unique=False)

    from django.contrib.auth.models import User
    user = models.ForeignKey(User, null=True)
    rule = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['id']
        app_label = 'gridMng'


class Rule:
    """ A rule used in the composite grid wizard. It provides functionality for creation based on a list of alternatives
     and ordering based on the total rating of the alternatives.
    """

    def __init__(self, alternatives, total_rating):
        self.name = '(' + ')*('.join(alternatives) + ')'
        self.total_rating = total_rating

    def __lt__(self, other):
        return self.total_rating < other.total_rating


class Concerns(models.Model):
    grid = models.ForeignKey(Grid)
    leftPole = models.CharField(max_length=150, null=True)
    rightPole = models.CharField(max_length=150, null=True)
    weight = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            old_values = {
                "old_leftPole": "",
                "old_rightPole": "",
                "old_weight": None
            }
        else:
            c = Concerns.objects.get(pk=self.pk)
            old_values = {
                "old_leftPole": c.leftPole,
                "old_rightPole": c.rightPole,
                "old_weight": c.weight
            }
        super(Concerns, self).save(*args, **kwargs)
        new_values = {
            "new_leftPole": self.leftPole,
            "new_rightPole": self.rightPole,
            "new_weight": self.weight
        }
        if sorted(old_values.values()) != sorted(new_values.values()):
            old_values.update(new_values)
            ConcernDiff.objects.create(related_id=self.id, grid=self.grid, **old_values)

    def delete(self, *args, **kwargs):
        for r in self.ratings_set.all():
            r.delete(grid=self.grid)

        attributes = {
            "related_id": self.id,
            "old_leftPole": self.leftPole,
            "old_rightPole": self.rightPole,
            "old_weight": self.weight,
            "new_leftPole": "",
            "new_rightPole": "",
            "new_weight": None,
        }
        super(Concerns, self).delete(*args, **kwargs)
        ConcernDiff.objects.create(grid=self.grid, **attributes)

    def __unicode__(self):
        return '%s -- %s (%f)' % (self.leftPole, self.rightPole, self.weight)

    def __lt__(self, other):
        return self.id < other.id

    class Meta:
        ordering = ['id']
        app_label = 'gridMng'


class Ratings(models.Model):
    concern = models.ForeignKey(Concerns)
    alternative = models.ForeignKey(Alternatives)
    rating = models.FloatField(null=True)

    class Meta:
        unique_together = ('concern',
                           'alternative')  # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        app_label = 'gridMng'

    def save(self, *args, **kwargs):
        if not self.pk:
            old_rating = None
        else:
            old_rating = Ratings.objects.get(pk=self.pk).rating
        super(Ratings, self).save(*args, **kwargs)
        if old_rating != self.rating:
            RatingDiff.objects.create(related_id=self.alternative_id, concern_id=self.concern_id,
                                      grid=self.alternative.grid, old_rating=old_rating, new_rating=self.rating)

    def delete(self, grid, *args, **kwargs):
        old_rating = self.rating
        old_alternative_id = self.alternative_id
        old_concern_id = self.concern_id
        super(Ratings, self).delete(*args, **kwargs)
        RatingDiff.objects.create(related_id=old_alternative_id, concern_id=old_concern_id, grid=grid,
                                  old_rating=old_rating, new_rating=None)

    def __unicode__(self):
        return "(%s, %s): %f" % (self.concern, self.alternative, self.rating)


class GridDiffManager(models.Manager):
    def ensure_initial_diff_exists(self, grid):
        exists = self.filter(grid=grid).exists()
        if not exists:
            diff = self.create(grid=grid, user=grid.user, type=DiffType.INITIAL)
            diff.date = grid.dateTime
            diff.save()


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


class State(models.Model):
    name = models.CharField(max_length=30)
    objects = StateManager()

    from .session.state import State as SessionState
    verbose_names = {SessionState.INITIAL: 'Invitation', SessionState.AC: 'Alternatives / Concerns',
                     SessionState.RW: 'Ratings / Weights', SessionState.FINISH: 'Closed',
                     SessionState.CHECK: 'Check values'}
    participation_statuses = {SessionState.INITIAL: 'Waiting for users to join',
                              SessionState.AC: 'Waiting for Alternative and concerns',
                              SessionState.RW: 'Waiting for Ratings and Weights', SessionState.FINISH: 'Closed',
                              SessionState.CHECK: 'Checking previous results'}

    class Meta:
        ordering = ['id']
        app_label = 'gridMng'

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
            return SessionState.CHECK
        elif self.name == SessionState.CHECK:
            return SessionState.AC, SessionState.RW, SessionState.FINISH
        else:
            return ()


class FacilitatorManager(models.Manager):
    def isFacilitator(self, userObj):
        facilitator, created = self.get_or_create(user=userObj)
        return not created and facilitator.session_set.count() > 0


class Facilitator(models.Model):
    from django.contrib.auth.models import User

    user = models.ForeignKey(User, unique=True)
    objects = FacilitatorManager()

    class Meta:
        ordering = ['id']
        app_label = 'gridMng'


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

        session = self.create(usid=usid, facilitator=facilitator, name=name, showResult=show_results, state=state,
                              invitationKey=invitation_key)
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
        app_label = 'gridMng'

    def getParticipators(self):
        return [participator.user for participator in self.userparticipatesession_set.all()]

    def addParticipant(self, user):
        if self.facilitator.user == user:
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
        SessionIterationState.objects.create(iteration=session.iteration, session=session, state=session.state)


class SessionIterationState(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    state = models.ForeignKey(State)
    objects = SessionIterationStateManager()

    class Meta:
        unique_together = ('iteration', 'session')
        ordering = ['id']
        app_label = 'gridMng'


class UserParticipateSession(models.Model):
    session = models.ForeignKey(Session)

    from django.contrib.auth.models import User
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('session',
                           'user')  # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']
        app_label = 'gridMng'

    def has_pending_response(self, user):
        if self.session.state.can_be_responded_to():
            try:
                ResponseGrid.objects.get_current(self.session, self.user)
                return False
            except ResponseGrid.DoesNotExist:
                return True

    def __unicode__(self):
        return "%s participating in %s" % (self.user, self.session)


# the name of this class in the orm is: iterationHasGridInSession
class SessionGrid(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    grid = models.ForeignKey(Grid)

    class Meta:
        unique_together = ('iteration',
                           'session')  # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']
        app_label = 'gridMng'


class ResponseGridManager(models.Manager):
    def get_iterations_with_grids(self, session, user):
        """ Returns a list of all the iterations in the given session for which the given user has responded """
        return [grid.iteration for grid in self.filter(session=session, user=user)]

    def get_current(self, session, user):
        """ Returns the response grid from the given user of the latest iteration of the given session """
        return user.responsegrid_set.get(session=session, iteration=session.iteration)


# the name of this class in the orm is: UserHasGridInIteration
class ResponseGrid(models.Model):
    iteration = models.IntegerField()
    session = models.ForeignKey(Session)
    grid = models.ForeignKey(Grid)

    from django.contrib.auth.models import User
    user = models.ForeignKey(User)
    objects = ResponseGridManager()

    class Meta:
        unique_together = ('iteration', 'user',
                           'session')  # they should be primary key but django wouldn't allow composite primary key so to enforce it it somewhat unique is used
        ordering = ['id']
        app_label = 'gridMng'
