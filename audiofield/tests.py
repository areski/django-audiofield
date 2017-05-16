#
# django-audiofield License
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2014 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib.auth.models import User
from django.test import TestCase
from common.utils import BaseAuthenticatedClient
from audiofield.models import AudioFile
from audiofield.forms import CustomerAudioFileForm


class AudiofieldAdminInterfaceTestCase(BaseAuthenticatedClient):
    """Test cases for Audiofield Admin Interface."""

    def test_admin_audiofile_list(self):
        """Test Function to check admin audio file list"""
        response = self.client.get('/admin/audiofield/audiofile/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_audiofile_add(self):
        """Test Function to check admin audio file add"""
        response = self.client.get('/admin/audiofield/audiofile/add/')
        self.failUnlessEqual(response.status_code, 200)


class AudioFileModel(TestCase):
    """Test AudioFile model"""

    fixtures = ['auth_user.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.audiofile = AudioFile(
            name='MyAudio',
            user=self.user,
        )
        self.audiofile.save()

    def test_name(self):
        self.assertEqual(self.audiofile.name, "MyAudio")

    def test_audio_form(self):
        form = CustomerAudioFileForm(instance=self.audiofile)

        self.assertTrue(isinstance(form.instance, AudioFile))
        self.assertEqual(form.instance.pk, self.audiofile.pk)

    def teardown(self):
        self.audiofile.delete()
