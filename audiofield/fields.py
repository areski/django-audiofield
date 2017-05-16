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

        convert_to = request and int(request.POST["convert_type"])
        ext = ext.split('.')[1]
        audio_type = CONVERT_TYPE_CHK[convert_to]
        error_msg = _("not allowed : file format conversion is not allowed for same audio type (except Wav)")
        if convert_to:
            if ext == audio_type and ext != 'wav':
                error_msg += ' %s format !!' % ext
                logger.error(error_msg)
                raise forms.ValidationError(error_msg)
            else:
                pass

        return data

    def _get_converted_filename(self, filename):
        # Not used
        '''Returns the audio converted name associated to the standard audio filename
        * Example: /var/www/myproject/media/audio/picture_1.wav
            will return /var/www/myproject/media/audio/picture_1.converted.wav
        '''
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.converted')
        logger.debug('converted file name')
        return ''.join(splitted_filename)

    def _convert_audio(self, filename, instance=None, ext=None):
        '''Convert uploaded audio file to selected format'''
        request = threadlocals.get_current_request()

        convert_type = 0
        channel_no = 0
        freq_value = 0
        nbchannels = 1
        remix = ''

        if 'convert_type' in request.POST:
            convert_type = int(request.POST["convert_type"])
        if 'channel_type' in request.POST:
            channel_no = int(request.POST["channel_type"])
        if 'freq_type' in request.POST:
            freq_value = int(request.POST["freq_type"])

        logger.info("convert audio : %s->%s" % (str(ext), CONVERT_TYPE_CHK[convert_type]))
        splitted_filename = list(os.path.splitext(filename))[0]  # converted filename without ext
        filename_temp = filename[:-4] + '_temp'

        # Find the number of channels
        if os.path.isfile(filename):
            command = "soxi -c %s" % filename
            response = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = response.communicate()
            nbchannels = (int(output))

        # prepare Sox parameters for Channels convertion
        conv_channel = "-e signed-integer -c %s" % str(channel_no) if channel_no > 0 else ''
        # prepare Sox parameters for Frequency convertion
        conv_freq = "-r %s" % str(freq_value) if freq_value > 0 else ''

        if nbchannels == 2:
            # sox input.wav output.wav `remix -` performs a mix-down of all input channels to mono.
            remix = 'remix -'

        # 1) MP3 TO WAV
        if ext == 'mp3' and CONVERT_TYPE_CHK[convert_type] == 'wav':
            logger.debug("convert MP3 to WAV - channel %s freq: %s" % (str(channel_no), str(freq_value)))
            conv = "sox %s %s %s %s.wav %s" % (filename, conv_freq, conv_channel, splitted_filename, remix)
            conv = conv.replace('  ', ' ')
            result = audio_convert_task.delay(conv)
            logger.debug("Sox command :> %s" % conv)

        # 2) MP3 TO OGG
        if ext == 'mp3' and CONVERT_TYPE_CHK[convert_type] == 'ogg':
            logger.debug('MP3 to OGG')
            conv = "dir2ogg -q 4 %s" % (filename)
            result = audio_convert_task.delay(conv)

        # 3) WAV TO MP3
        if ext == 'wav' and CONVERT_TYPE_CHK[convert_type] == 'mp3':
            logger.debug('WAV to MP3')
            conv = "sox %s %s.mp3 %s" % (filename, splitted_filename, remix)
            result = audio_convert_task.delay(conv)
            logger.debug("Sox command :> %s" % conv)

        # 3) WAV TO WAV
        if ext == 'wav' and CONVERT_TYPE_CHK[convert_type] == 'wav':
            # if nbchannels == 2:
            #     remix = 'remix 1,2i'
            filename_temp = filename_temp + '.wav'
            conv = "sox %s %s %s %s.wav %s" % (filename_temp, conv_freq, conv_channel, splitted_filename, remix)
            conv = conv.replace('  ', ' ')
            # cmd = 'sox /usr/share/newfies/../newfies/usermedia/upload/audiofiles/audio-file-XFPQN-6216731785_temp.wav -r 8000 -e signed-integer -c 1 /usr/share/newfies/../newfies/usermedia/upload/audiofiles/audio-file-XFPQN-6216731785.wav'
            # create a temp copy of the file
            shutil.copy2(filename, filename_temp)
            result = audio_convert_task.delay(conv)
            logger.debug("result :> %s" % str(result))

        # 4) WAV TO OGG
        if ext == 'wav' and CONVERT_TYPE_CHK[convert_type] == 'ogg':
            logger.debug('WAV to OGG')
            conv = "sox %s %s.ogg %s" % (filename, splitted_filename, remix)
            result = audio_convert_task.delay(conv)

        # 5) OGG TO MP3
        if ext == 'ogg' and CONVERT_TYPE_CHK[convert_type] == 'mp3':
            logger.debug('OGG to MP3')
            conv = "sox %s %s.mp3%s" % (filename, splitted_filename, remix)
            result = audio_convert_task.delay(conv)

        # 6) OGG TO WAV
        if ext == 'ogg' and CONVERT_TYPE_CHK[convert_type] == 'wav':
            logger.debug('OGG to WAV')
            # conv = "sox %s %s.wav" % (filename, splitted_filename)
            conv = "avconv -i %s -map_metadata 0:s:0 %s.wav" % (filename, splitted_filename)
            result = audio_convert_task.delay(conv)

    def _rename_audio(self, instance=None, **kwargs):
        '''Rename uploaded audio file & calls methods to convert audio file format if
        convert_to is selected'''
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path

            # Get the extension and limit to 3 chars
            ext = os.path.splitext(filename)[1].lower()[:4]
            # Get new file name and make sure it's unique
            dst = self.generate_filename(instance, '%s%s%s' % (self.filename_prefix, self.uuid, ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)

            # Same file should not exits
            if not os.path.isfile(dst_fullpath):

                if os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                    os.rename(filename, dst_fullpath)
                    self._convert_audio(dst_fullpath, instance, ext[1:4])

                    request = threadlocals.get_current_request()
                    convert_type = int(request.POST["convert_type"])

                    # 0 => Keep original
                    if convert_type > 0:
                        # Delete original audio file
                        if os.path.exists(dst_fullpath):
                            # Check for no .. and no *
                            # DISABLED Delete file
                            """
                            if dst_fullpath.find('../../') == -1 and dst_fullpath.find('*') == -1:
                                os.remove(dst_fullpath)
                            """
                        ext = '.' + CONVERT_TYPE_CHK[convert_type]
                        dst = self.generate_filename(instance, '%s%s%s' %
                                                    (self.filename_prefix, self.uuid, ext))
                    setattr(instance, self.attname, dst)
                    instance.save()
            else:
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
        signals.post_save.connect(self._rename_audio, sender=cls)
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
