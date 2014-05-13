from django.test import TestCase
from django.contrib.auth.models import User
from models import Session, Facilitator, State, Grid, SessionGrid


class BaseSessionTest(TestCase):

    def setUp(self):
        self.facilitator = User.objects.create_user('Facilitator', 'frank@facilitator.com', 'password', first_name='Frank',
                                        last_name='Facilitator')
        grid = Grid.objects.create(usid='a1b2c3', name='TestGrid', user=self.facilitator)
        self.session = Session.objects.create_session(facilitating_user=self.facilitator, original_grid=grid, name='Session1')
        self.key = self.session.invitationKey
        self.participant = User.objects.create_user('Participant', 'peter@participant.com', 'password')

    def login(self, user):
        self.client.post('/accounts/login/', {'email': user.email, 'password': 'password'})


class SessionTest(BaseSessionTest):

    def test_get_descriptive_name(self):
        self.assertEquals("Frank Facilitator: Session1", self.session.get_descriptive_name())

    def test_get_absolute_url(self):
        self.session.usid = "abcdef"
        self.assertEquals("/sessions/show/abcdef", self.session.get_absolute_url())


class JoinSessionTest(BaseSessionTest):

    path = '/sessions/join/'

    def test_get_not_logged_in(self):
        response = self.client.get(self.path + self.key)
        self.assertRedirects(response, 'accounts/login/?next=' + self.path +  self.key)

    def test_valid(self):
        self.login(self.participant)
        response = self.client.get(self.path + self.key, follow=True)
        self.assertIn(self.participant, self.session.getParticipators())
        self.assertEquals(1, len(self.session.getParticipators()))
        self.assertRedirects(response, '/sessions/participate/')
        self.assertInHTML('<li class="success">Successfully joined session</li>', response.content)

    def test_invalid_invitation_key(self):
        self.login(self.participant)
        response = self.client.get(self.path + "abcdef")
        self.assertEquals(404, response.status_code)

    def test_join_twice(self):
        self.login(self.participant)
        self.client.get(self.path + self.key)
        response = self.client.get(self.path + self.key, follow=True)
        self.assertRedirects(response, '/sessions/participate/')
        self.assertEquals(1, len(self.session.getParticipators()))

    def test_join_as_facilitator(self):
        self.login(self.facilitator)
        response = self.client.get(self.path + self.key, follow=True)
        self.assertRedirects(response, self.session.get_absolute_url())
        self.assertInHTML('<li class="error">You are already the facilitator of this session</li>', response.content)
        self.assertEquals(0, len(self.session.getParticipators()))

    def test_join_wrong_state(self):
        self.session.state.name = 'finish'
        self.session.state.save()
        self.login(self.participant)
        response = self.client.get(self.path + self.key, follow=True)
        self.assertInHTML('<li class="error">Could not join session, as it is in state &quot;Closed&quot;</li>', response.content)

class GridTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='george', email='george@gridmaker.com', password='123')
        self.grid = Grid.objects.create(usid='a1b2c3', name='TestGrid', user=self.user)

    def test_get_absolute_url(self):
        self.assertEquals('/grids/show/a1b2c3', self.grid.get_absolute_url())


class ShowGridTest(TestCase):

    path = '/grids/show/'

    def setUp(self):
        self.user = User.objects.create_user(username='george', email='george@gridmaker.com', password='123')
        Grid.objects.create(usid='a1b2c3', name='TestGrid', user=self.user)

    def __login(self):
        self.client.post('/accounts/login/', {'email': 'george@gridmaker.com', 'password': '123'})

    def test_get_not_logged_in(self):
        response = self.client.get(self.path + 'a1b2c3')
        self.assertRedirects(response, 'accounts/login/?next=/grids/show/a1b2c3')

    def test_get_unauthorized(self):
        other_user = User.objects.create_user(username='john', email='john@gridmaker.com', password='123')
        Grid.objects.create(usid='j0hN5gRiD', name='John\'s grid', user=other_user)

        self.__login()
        response = self.client.get(self.path + "j0hN5gRiD")
        self.assertEquals(404, response.status_code)

    def test_get_authorized(self):
        self.__login()
        response = self.client.get(self.path + 'a1b2c3')
        self.assertContains(response, "TestGrid")
        self.assertContains(response, "class=\"gridTable\"")

    def test_get_invalid_usid(self):
        self.__login()
        response = self.client.get(self.path + 'iNv41iD')
        self.assertEquals(404, response.status_code)
