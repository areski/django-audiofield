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
from __future__ import unicode_literals

import six
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from audiofield.fields import AudioField

try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


@six.python_2_unicode_compatible
class AudioFile(models.Model):
    """
    This Model describe the Audio used on the platform,
    this allow to upload audio file and configure
    alternate Text2Speech System
    """
    name = models.CharField(max_length=150, blank=False, verbose_name=_('audio name'),
                            help_text=_('audio file label'))
    audio_file = AudioField(upload_to='upload/audiofiles', blank=True,
                            ext_whitelist=('.mp3', '.wav', '.ogg'),
                            verbose_name=_('audio file'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'),
                             help_text=_('select user'))
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_audiofile', _('can see Audio Files')),
        )
        db_table = 'audio_file'
        verbose_name = _('audio file')
        verbose_name_plural = _('audio files')

    def __str__(self):
        return '[%s] %s' % (self.id, self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Call the "real" save() method
        super(AudioFile, self).save(force_insert, force_update, using, update_fields)

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % \
                (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = _('audio file player')
