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

from celery.utils.log import get_task_logger
from celery.decorators import task
import subprocess
import os
from uuid import uuid1
# import shlex

logger = get_task_logger(__name__)

DELAY_TASK = 5  # Seconds


@task()
def audio_convert_task(conv):
    """Convert audio files"""

    logger.info('[audio_convert_task] Received a request to convert audio file in %dsecs' % DELAY_TASK)
    run_convert_task.apply_async((conv,), countdown=DELAY_TASK)

    return True


@task()
def run_convert_task(conv):
    """
    Exec the audio convert
    This version use Bash to convert the audio as calling Sox directly fails
    """
    filebash = "/tmp/bash-%s.sh" % str(uuid1())

    logger.warning('Convert audio file :> %s' % str(conv))
    logger.warning('Filebash :> %s' % filebash)

    filename = conv.split(' ')[1].strip()
    if os.path.isfile(filename):
        logger.debug("File exists!")
    else:
        logger.error("Error: File don't exist!")
        return False

    with open(filebash, 'w') as mfile:
        mfile.write('#!/bin/bash\n')
        mfile.write(conv)
        mfile.write('\n')

    cmd = [
        'bash',
        filebash
    ]

    # output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = response.communicate()
    if error:
        logger.error('Error conversion : %s ' % error)

    return response


@task()
def old_run_convert_task(conv):
    """Exec the audio convert"""

    logger.warning('Convert audio file :> %s' % str(conv))

    filename = conv.split(' ')[1].strip()
    if os.path.isfile(filename):
        logger.debug("File exists!")
    else:
        logger.error("Error: File don't exist!")

    # Option 1 : Popen
    response = subprocess.Popen(conv.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = response.communicate()
    if error:
        logger.error('Conv :')
        logger.error(conv.split(' '))
        logger.error('Error conversion2 : %s ' % error)

    # Option 2 : Popen & Shlex
    # args = shlex.split(conv)
    # p = subprocess.Popen(args)

    return response
