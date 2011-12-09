from django import forms
from django.forms.fields import FileField
from django.forms import ModelForm
from audiofield.models import AudioFile
from audiofield.widgets import AdminAudioFileWidget, CustomerAudioFileWidget
import os.path


class AudioFormField(FileField):
    
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(AudioFormField, self).clean(data, initial)
        else:
            return '__deleted__'


class AdminAudioFileForm(ModelForm):
    """AudioFile ModelForm"""

    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']


class CustomerAudioFileForm(ModelForm):
    """CustomerAudioForm"""
    audio_file = forms.FileField(widget=CustomerAudioFileWidget)
    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']
        exclude = ('user',)