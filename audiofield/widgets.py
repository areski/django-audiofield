#
# django-audiofield License
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2012 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
import os.path


CHANNEL_TYPE = (
    ('0', _('Keep original')),
    ('1', _('Mono')),
    ('2', _('Stereo')),
)

FREQ_TYPE = (
    ('0', _('Keep original')),
    ('8000', _('8000 Hz')),
    ('16000', _('16000 Hz')),
    ('22050', _('22050 Hz')),
    ('44100', _('44100 Hz')),
    ('48000', _('48000 Hz')),
)

CONVERT_TYPE = (
    ('0', _('Keep original audio file')),
    ('1', _('Convert to MP3')),
    ('2', _('Convert to WAV')),
    ('3', _('Convert to OGG')),
)


def add_select_box(select_name, select_value):
    '''
    function to create Html select option
    '''
    select_box = u'<select name="%s">' % (select_name)
    for i in select_value:
        select_box += u'<option value="%s">%s</option>' % (i[0], i[1])
    select_box += u'</select>'
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
        item = u'<tr><td style="vertical-align: middle;">%s</td><td>%s</td>'
        output = []
        output.append(u'<table style="border-style: none;">')
        help_text = _('Allowed format - mp3 wav and ogg')
        if value and type(value).__name__ != 'str':
            file_url = settings.MEDIA_URL + str(value)
            output.append(item % (_('Currently:'),
                                  u'<ul class="playlist" style="margin-left: 0em;padding-left: 0px;"><li style="width:250px;"><a href="%s">%s</a></li></ul>' \
                                  % (file_url, os.path.basename(value.name))))
            output.append(item % (_('Change:'), input + '<br/>%s' % help_text))
        else:
            output.append(item % (_('Upload:'), input + '<br/>%s' % help_text))

        output.append(item % (_('Convert To:'), file_select_box))
        output.append(item % (_('Channel:'), channel_select_box))
        output.append(item % (_('Frequency:'), freq_select_box))

        if value:
            # split colon to force "Delete" that is already translated
            output.append(item % (_('Delete:'), '<input type="checkbox" name="%s_delete"/>' % name))
        output.append(u'</table>')

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

        file_select_box = u'<input type="hidden" name="convert_type" value="%s"/>' % settings.CONVERT_TYPE_VALUE
        channel_select_box = u'<input type="hidden" name="channel_type" value="%s"/>' % settings.CHANNEL_TYPE_VALUE
        freq_select_box = u'<input type="hidden" name="freq_type" value="%s"/>' % settings.FREQ_TYPE_VALUE

        output = []

        label_style = 'float:left;line-height:18px;padding-top:6px;text-align:right;'
        input_div_style = 'width:300px;margin-left:70px;'

        item = u'<div style="' + label_style + '">%s</div><div style="' + input_div_style + '">%s</div>'
        help_text = u'<span class="help-block">%s</span>' % _('Allowed format - mp3, wav and ogg')

        if value and type(value).__name__ != 'str':
            file_url = settings.MEDIA_URL + str(value)
            output.append(item % (_('Currently:'),
                                  u'<ul class="playlist" style="margin-left: 0em;padding-left: 0px;"><li style="width:250px;"><a href="%s">%s</a></li></ul>' \
                                  % (file_url, os.path.basename(value.name))))
            output.append(item % (_('Change:'), input + help_text))
        else:
            input_div_style = 'width:300px;'
            item = '<div style="' + label_style + '">%s</div><div style="' + input_div_style + '">%s</div>'
            output.append(item % ('', input + help_text))

        output.append(item % (file_select_box, ''))
        output.append(item % (channel_select_box, ''))
        output.append(item % (freq_select_box, ''))

        return mark_safe(u''.join(output))

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(CustomerAudioFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'
