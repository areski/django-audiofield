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

from django.db.models.fields.files import FileField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _
from django import forms
from celery.utils.log import get_task_logger
from audiofield.middleware import threadlocals
from audiofield.tasks import audio_convert_task
import os
import subprocess
import shutil
from random import choice, seed

seed()
logger = get_task_logger(__name__)
CONVERT_TYPE_CHK = {0: 'org', 1: 'mp3', 2: 'wav', 3: 'ogg'}


def random_string(char_length=5, digit_length=10):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit = "1234567890"
    pass_str_char = ''.join([choice(chars) for i in range(char_length)])
    pass_str_digit = ''.join([choice(digit) for i in range(digit_length)])
    return pass_str_char + '-' + pass_str_digit


class StdAudioField:
    '''
    Instances of this class will be used to access data of the converted
    audio files
    '''
    def __init__(self, name):
        self.name = name
        self.storage = FileSystemStorage()

    def path(self):
        return self.storage.path(self.name)

    def url(self):
        return self.storage.url(self.name)

    def size(self):
        return self.storage.size(self.name)


class AudioField(FileField):
    '''
    Django field that behaves as FileField, with some extra features like:
        - Audio Player
        - Delete specific file
        - Convert to specific format
    '''
    size = None
    uuid = None
    filename_prefix = 'audio-file-'

    def __init__(self, *args, **kwargs):
        """Get allowed file extension type (ex. mp3, wav)"""
        ext_whitelist = kwargs.pop("ext_whitelist", tuple())
        self.ext_whitelist = [i.lower() for i in ext_whitelist]
        super(AudioField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Audio field validation for file extension"""
        data = super(AudioField, self).clean(data, initial)

        request = threadlocals.get_current_request()

        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
            error_msg = _("not allowed filetype!")
            logger.error(error_msg)
            raise forms.ValidationError(error_msg)

        ext = ext.split('.')[1]
        audio_type = CONVERT_TYPE_CHK[convert_to]
        error_msg = _("not allowed : file format conversion is not allowed for same audio type (except Wav)")
        if request:
            if ext == audio_type and ext != 'wav':
                error_msg += ' %s format !!' % ext
                logger.error(error_msg)
                raise forms.ValidationError(error_msg)

        return data

    def _get_converted_filename(self, filename):
        # Not Used
        pass

    def _convert_audio(self, filename, instance=None, ext=None):
        pass

    def _check_if_exists(self, instance=None, **kwargs):
        '''Rename uploaded audio file & calls methods to convert audio file format if
        convert_to is selected'''
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path

            # Same file should not exist
            if os.path.isfile(filename):
                error_msg = ("file already exists!")
                logger.error(error_msg)

    def _set_audio_converted(self, instance=None, **kwargs):
        '''Creates a "audio_field" object as attribute of the FileField instance
        audio_field attribute will be of the same class of original file, so
        "path", "url", "name"... properties can be used'''
        if getattr(instance, self.name):
            filename = self.generate_filename(instance, os.path.basename(getattr(instance, self.name).path))
            audio_field = StdAudioField(filename)
            setattr(getattr(instance, self.name), 'audio_converted', audio_field)

    def formfield(self, **kwargs):
        '''Specify form field and widget to be used on the forms'''
        from audiofield.widgets import AdminAudioFileWidget
        from audiofield.forms import AudioFormField
        kwargs['widget'] = AdminAudioFileWidget
        kwargs['form_class'] = AudioFormField

        return super(AudioField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        '''Overwrite save_form_data to delete audio files if "delete" checkbox
        is selected'''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                # Check for no .. and no *
                if filename.find('../../') == -1 and filename.find('*') == -1:
                    os.remove(filename)
            setattr(instance, self.name, None)
        else:
            self.uuid = random_string(5, 10)
            super(AudioField, self).save_form_data(instance, data)

    def contribute_to_class(self, cls, name):
        '''Call methods for generating all operations on specified signals'''
        super(AudioField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._check_if_exists, sender=cls)
        signals.post_init.connect(self._set_audio_converted, sender=cls)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([(
            [AudioField],
            [],
            {
                "ext_whitelist": ["ext_whitelist", {}],
            },
        ),
    ], ["^audiofield\.fields\.AudioField"])
except ImportError:
    # South is not enabled
    pass
