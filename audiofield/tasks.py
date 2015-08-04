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
# import shlex

logger = get_task_logger(__name__)

DELAY_TASK = 5  # Seconds


@task()
def audio_convert_task(conv):
    """Convert audio files"""

    logger.info('Received a request to convert audio file in %dsecs' % DELAY_TASK)
    run_convert_task.apply_async((conv,), countdown=DELAY_TASK)

    return True


@task()
def run_convert_task(conv):
    """Exec the audio convert"""

    logger.info('Convert audio file :> %s' % str(conv))

    filename = conv.split(' ')[1].strip()
    if os.path.isfile(filename):
        logger.debug("File exists!")
    else:
        logger.error("Error: File don't exist!")

    # Option 1 : Popen
    response = subprocess.Popen(conv.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (filetype, error) = response.communicate()
    if error:
        logger.error('Error conversion : %s ' % error)

    # Option 2 : Popen & Shlex
    # args = shlex.split(conv)
    # p = subprocess.Popen(args)

    return response
