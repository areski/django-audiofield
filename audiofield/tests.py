from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.http import HttpRequest
from audiofield.test_utils import build_test_suite_from
import base64
import simplejson


class BaseAuthenticatedClient(TestCase):
    """Common Authentication"""

    def setUp(self):
        """To create admin user"""
        self.client = Client()
        self.user = \
        User.objects.create_user('admin', 'admin@world.com', 'admin')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()
        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }


class AudiofieldAdminInterfaceTestCase(BaseAuthenticatedClient):
    """Test cases for Audiofield Admin Interface."""

    def test_admin_index(self):
        """Test Function to check Admin index page"""
        response = self.client.get('/admin/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.login(username=self.user.username,
                                     password='admin')
        self.assertEqual(response, True)

    def test_admin_audiofield(self):
        """Test Function to check Audiofield/ Admin pages"""
        response = self.client.get('/admin/audiofield/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get('/admin/audiofield/audiofile/')
        self.failUnlessEqual(response.status_code, 200)


test_cases = [
    AudiofieldAdminInterfaceTestCase,
]


def suite():
    return build_test_suite_from(test_cases)
