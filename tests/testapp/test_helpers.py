from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase

from gargoyle.helpers import MockRequest
from gargoyle.manager import SwitchManager
from gargoyle.models import Switch


class MockRequestTest(TestCase):
    def setUp(self):
        self.gargoyle = SwitchManager(Switch, key='key', value='value', instances=True)

    def test_empty_attrs(self):
        req = MockRequest()
        assert req.META['REMOTE_ADDR'] is None
        assert isinstance(req.user, AnonymousUser)

    def test_ip(self):
        req = MockRequest(ip_address='127.0.0.1')
        assert req.META['REMOTE_ADDR'] == '127.0.0.1'
        assert isinstance(req.user, AnonymousUser)

    def test_user(self):
        user = User.objects.create(username='foo', email='foo@example.com')
        req = MockRequest(user=user)
        assert req.META['REMOTE_ADDR'] is None
        assert req.user == user

    def test_as_request(self):
        user = User.objects.create(username='foo', email='foo@example.com')

        req = self.gargoyle.as_request(user=user, ip_address='127.0.0.1')

        assert req.META['REMOTE_ADDR'] == '127.0.0.1'
        assert req.user == user
