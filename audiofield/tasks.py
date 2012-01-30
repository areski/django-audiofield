from celery.task import Task
from models import *
import commands
import logging


class AudioConvertTask(Task):
    """
    Convert audio files
    """

    def run(self, conv, **kwargs):
        response = commands.getoutput(conv)
        logging.debug("command :> %s" % conv)
        return response
