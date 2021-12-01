import uuid
from unittest import TestCase

from authentication.models import User


class BaseTest(TestCase):

    def create(self, email='test@mail.com', password=None):
        if not password:
            password = str(uuid.uuid4())

        user = User.objects.create_user(
            email=email,
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.save()

        return user

    def create_and_login(self, email='test@mail.com', password=None):
        if not password:
            password = str(uuid.uuid4())
        user = self.create(email=email, password=password)
        self.login(email=email, password=password)
        return user

    def login(self, email, password):
        self.client.login(email=email, password=password)

    def logout(self):
        self.client.logout()
