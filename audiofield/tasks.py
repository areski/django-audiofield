from celery.task import Task
from models import *
import commands
import logging
import subprocess
import shlex

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
        
        logger.info('\n\n\n\n Got request to convertion audio file :> ' + str(conv))
        return response
