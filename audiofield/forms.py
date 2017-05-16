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
from django import forms
from django.forms.fields import FileField
from django.forms import ModelForm
from audiofield.models import AudioFile
from audiofield.widgets import CustomerAudioFileWidget


class AudioFormField(FileField):
    """
    Field Class to upload audio file
    """
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(AudioFormField, self).clean(data, initial)
        else:
            return '__deleted__'


class AdminAudioFileForm(ModelForm):
    """
    This form aims to be used in the django admin, support
    all the features for convertion per default
    """
    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']


class CustomerAudioFileForm(ModelForm):
    """
    The following form aims to be used on frontend to power
    simple upload of audio files without convertion
    """
    audio_file = forms.FileField(widget=CustomerAudioFileWidget)

    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']
        exclude = ('user',)
