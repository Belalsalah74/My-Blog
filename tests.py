from enum import unique
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase
from django.conf import settings

class SECRET_KEY_strong(TestCase):
    def test_SECRET_KEY(self):
        try:
            validate_password(settings.SECRET_KEY)
        except :
            msg = 'bad secret key'
            self.fail(msg)

