from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
import os.path


CHANNEL_TYPE = (
    ('0', ('Keep original')),
    ('1', ('Mono')),
    ('2', ('Stereo')),
)

FREQ_TYPE = (
    ('0', ('Keep original')),
    ('8000', ('8000 Hz')),
    ('16000', ('16000 Hz')),
    ('22050', ('22050 Hz')),
    ('44100', ('44100 Hz')),
    ('48000', ('48000 Hz')),
)

CONVERT_TYPE = (
    ('0', ('Keep original audio file')),
    ('1', ('Convert to MP3')),
    ('2', ('Convert to WAV')),
    ('3', ('Convert to OGG')),
)


def add_select_box(select_name, select_value):
    '''
    function to create Html select option
    '''
    select_box = '<select name="%s">' % (select_name)
    for i in select_value:
        select_box += '<option value="'+i[0]+'">' + i[1] + '</option>'
    select_box += '</select>'
    return select_box


class AdminAudioFileWidget(AdminFileWidget):
    '''
    A AdminFileWidget that shows
        - audio player to play uploaded file
        - file browser
        - audio type conversion
        - If conversion is mp3 to wav, you can add channel type & frequency 
        - a delete checkbox
    '''
    input_type = 'file'
    
    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)
        
        file_select_box = add_select_box('convert_type', CONVERT_TYPE)
        channel_select_box = add_select_box('channel_type', CHANNEL_TYPE)
        freq_select_box = add_select_box('freq_type', FREQ_TYPE)
        
        file_url = ''
        item = '<tr><td style="vertical-align: middle;">%s</td><td>%s</td>'
        output = []
        output.append('<table style="border-style: none;">')

        if value and type(value).__name__ != 'str':
            file_url = settings.MEDIA_URL + str(value)
            output.append(item % (_('Currently:'),
                                  '<ul class="playlist" style="margin-left: 0em;padding-left: 0px;"><li style="width:250px;"><a href="%s">%s</a></li></ul>' \
                                  % (file_url, os.path.basename(value.name))))
            output.append(item % (_('Change:'), input + '<br/>Allowed type - .mp3, .wav, .ogg'))
        else:
            output.append(item % (_('Upload:'), input + '<br/>Allowed type - .mp3, .wav, .ogg'))

        output.append(item % (_('Convert To') + ':', file_select_box))
        output.append(item % (_('Channel') + ':', channel_select_box))
        output.append(item % (_('Frequecy') + ':', freq_select_box))

        if value:
            output.append(item % (_('Delete') + ':', '<input type="checkbox" name="%s_delete"/>' % name)) # split colon to force "Delete" that is already translated
        output.append('</table>')

        return mark_safe(u''.join(output))

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(AdminAudioFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'

        
class CustomerAudioFileWidget(AdminFileWidget):
    '''
    A CustomerAudioFileWidget that shows
        - audio player to play uploaded file
        - file browser
        - hidden variables which are set in settings.py
            - audio type conversion
            - If conversion is mp3 to wav, you can add channel type & frequency
    '''
    input_type = 'file'
    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)

        file_url = ''
        item = '<tr><td style="vertical-align: middle;">%s</td><td>%s</td>'
        
        file_select_box = '<input type="hidden" name="convert_type" value="' + str(settings.CONVERT_TYPE_VALUE) + '"/>'
        channel_select_box = '<input type="hidden" name="channel_type" value="' + str(settings.CHANNEL_TYPE_VALUE) + '"/>'
        freq_select_box = '<input type="hidden" name="freq_type" value="' + str(settings.FREQ_TYPE_VALUE) + '"/>'

        output = []
        output.append('<table style="border-style: none;width:300px;">')

        if value and type(value).__name__ != 'str':
            file_url = settings.MEDIA_URL + str(value)
            output.append(item % (_('Currently:'),
                                  '<ul class="playlist" style="margin-left: 0em;padding-left: 0px;"><li style="width:250px;"><a href="%s">%s</a></li></ul>' \
                                  % (file_url, os.path.basename(value.name))))
            output.append(item % (_('Change:'), input + '<br/>Allowed type - .mp3, .wav, .ogg'))
        else:
            output.append(item % (input + '<br/>Allowed type - .mp3, .wav, .ogg', ''))

        output.append(item % (file_select_box, ''))
        output.append(item % (channel_select_box, ''))
        output.append(item % (freq_select_box, ''))

        output.append('</table>')

        return mark_safe(u''.join(output))

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(CustomerAudioFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'
