from django.test import TestCase
from django.contrib.auth.models import User
from models import Session, Facilitator, State, Grid


class SessionTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Facilitator", first_name="Frank", last_name="Facilitator")
        facilitator = Facilitator.objects.create(user=user)
        state = State.objects.create(name='initial')
        self.session = Session.objects.create(facilitator=facilitator, state=state, name="Session1")

    def test_get_descriptive_name(self):
        self.assertEqual("Frank Facilitator: Session1", self.session.get_descriptive_name())

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

    def test_get_invalid_usid(self):
        self.__login()
        response = self.client.get(self.path + 'iNv41iD')
        self.assertEquals(404, response.status_code)
