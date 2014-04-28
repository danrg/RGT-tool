from django.test import TestCase
from django.contrib.auth.models import User
from models import Session, Facilitator, State

class SessionTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Facilitator", first_name="Frank", last_name="Facilitator")
        facilitator = Facilitator.objects.create(user=user)
        state = State.objects.create(name='initial')
        self.session = Session.objects.create(facilitator=facilitator, state=state, name="Session1")

    def test_get_descriptive_name(self):
        self.assertEqual("Frank Facilitator: Session1", self.session.get_descriptive_name())