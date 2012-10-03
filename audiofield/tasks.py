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

from celery.task import Task
import commands
#import subprocess
#import shlex


class audio_convert_task(Task):
    """
    Convert audio files
    """
    def run(self, conv, **kwargs):
        """Run conversion"""

        logger = self.get_logger(**kwargs)

        #Option 1 : command
        response = commands.getoutput(conv)

        #Option 2 : Popen
        #response = subprocess.Popen(conv.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #Option 3 : Popen & Shlex
        #args = shlex.split(conv)
        #p = subprocess.Popen(args)

        logger.info('Received a request to converte audio file :> ' + str(conv))
        return response
