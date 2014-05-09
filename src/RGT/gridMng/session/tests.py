from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.unittest.case import skip

from RGT.gridMng.models import Grid, Session


class CreateSessionTest(TestCase):
    """ Tests ajaxCreateSession from views.py """

    path = '/sessions/create/'

    def setUp(self):
        self.user = User.objects.create_user(username='fred', email='fred@facilitator.com', password='123')
        Grid.objects.create(usid='a1b2c3', name='TestGrid', user=self.user)

    def __login(self):
        self.client.post('/accounts/login/', {'email': 'fred@facilitator.com', 'password': '123'})

    def __assert_session_created(self, response, name='untitled', show_result=False):
        session = Session.objects.get(pk=1)
        self.assertContains(response, "Session was created.")
        self.assertEquals(self.user, session.facilitator.user)
        self.assertEquals(0, session.iteration)
        self.assertEquals(name, session.name)
        self.assertEquals('initial', session.state.name)
        self.assertEquals(show_result, session.showResult)
        self.assertIsNone(session.description)

    def test_get_unauthorized(self):
        response = self.client.get(self.path, follow=True)
        self.assertRedirects(response, 'accounts/login/?next=/sessions/create/')

    def test_get_authorized(self):
        self.__login()
        response = self.client.get(self.path, follow=True)
        self.assertContains(response, "Create session")

    def test_post_minimal_params(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'a1b2c3'})
        self.__assert_session_created(response)

    def test_post_with_invalid_gridusid(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'abcdef'})
        self.assertContains(response, "Grid was not found")
        self.assertEquals(0, Session.objects.count())

    def test_post_with_other_grid(self):
        other_user = User.objects.create_user(username='john', email='john@example.com', password='123')
        Grid.objects.create(usid='0th3r', name='NotFredsGrid', user=other_user)

        self.__login()
        response = self.client.post(self.path, {'gridUSID': '0th3r'})
        self.assertEquals(0, Session.objects.count())
        self.assertContains(response, "Grid was not found")

    def test_post_with_name(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'a1b2c3', 'sessionName': 'TestSession'})
        self.__assert_session_created(response, name='TestSession')

    def test_post_with_invalid_name(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'a1b2c3', 'sessionName': ''})
        self.assertContains(response, "Name can not be empty")
        self.assertEquals(0, Session.objects.count())

    def test_post_with_show_results(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'a1b2c3', 'showResults': 'Y'})
        self.__assert_session_created(response, show_result=True)

    def test_post_with_invalid_show_results(self):
        self.__login()
        response = self.client.post(self.path, {'gridUSID': 'a1b2c3', 'showResults': ''})
        self.assertContains(response, "Invalid value for showResults given")
        self.assertEquals(0, Session.objects.count())

    def test_post_no_params(self):
        self.__login()
        response = self.client.post(self.path)
        self.assertContains(response, "gridUSID can not be empty")
        self.assertEquals(0, Session.objects.count())

class ShowSessionTest(TestCase):
    """ Tests show_session from views.py """

    def setUp(self):
        self.user = User.objects.create_user(username='fred', email='fred@facilitator.com', password='123')
        self.grid = Grid.objects.create(usid='a1b2c3', name='TestGrid', user=self.user)
        self.session = Session.objects.create_session(facilitating_user=self.user, original_grid=self.grid)
        self.session.usid = "a1b2c3"

    def __login(self):
        self.client.post('/accounts/login/', {'email': 'fred@facilitator.com', 'password': '123'})

    def test_get_not_logged_in(self):
        response = self.client.get(self.session.get_absolute_url())
        self.assertRedirects(response, 'accounts/login/?next=/sessions/show/a1b2c3')

    def test_get_unauthorized(self):
        other_user = User.objects.create_user(username='john', email='john@gridmaker.com', password='123')
        other_grid = Grid.objects.create(usid='j0hN5gRiD', name='John\'s grid', user=other_user)
        session = Session.objects.create_session(facilitating_user=other_user, original_grid=other_grid)

        self.__login()
        response = self.client.get(session.get_absolute_url())
        self.assertEquals(404, response.status_code)

    def test_get_authorized(self):
        self.__login()
        response = self.client.get(self.session.get_absolute_url())
        # self.assertContains(response, "Session administration")
        # self.assertContains(response, "untitled")
        # self.assertContains(response, "<div id=\"sessionDetails\">")

    def test_get_invalid_usid(self):
        self.__login()
        invalid_url = self.session.get_absolute_url()
        self.session.usid = "abcdef"
        response = self.client.get(invalid_url)
        self.assertEquals(404, response.status_code)
