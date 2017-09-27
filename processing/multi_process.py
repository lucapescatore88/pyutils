#!/usr/bin/env python

import subprocess, shlex, logging, os, select, threading, logging

def _call(popenargs, logger, stdout_log_level=logging.DEBUG, stderr_log_level=logging.ERROR, **kwargs):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    """
    child = subprocess.Popen(popenargs, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, **kwargs)
    
    log_level = {child.stdout: stdout_log_level,
                    child.stderr: stderr_log_level}
        
    def check_io():
        ready_to_read = select.select([child.stdout, child.stderr], [], [], 1000)[0]
        for io in ready_to_read:
            line = io.readline()
            if line != '':
                logger.log(log_level[io], line[:-1])
            
    # keep checking stdout/stderr until the child exits
    while child.poll() is None:
        check_io()
        
    check_io() # check again to catch anything after the process exits
    return child.wait()


def runCommand(command, logger=None):
    '''
    Execute shell command, a logger can be given,
    interpet directly command with shell (possibly dangerous) 
    '''
    if logger:
        _call(command, logger, shell=True)
    else:
        FNULL = open(os.devnull, 'w')
        subprocess.call(command, shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)
    return


class MultiProcess:
    '''
    Class to run in parallel various command, wait when they are done and then run in parallel next chunck and so on
    logFile is the name of the logfile
    commands is a list of lists or dictionaries
    eg commands = [
                   [com1, com2],
                   {'com3' : com3, 'com4' : com4}
                   ]
    and executes in parallel com1 and com2, waits that they are done and then executes com3 and com4
    '''
    def __init__(self, commands = None, logFile = None):
        self.commands = commands
        self.logFile = logFile

    def run(self):

        # if needed define logger
        if self.logFile:
            if os.path.exists(self.logFile):
                os.remove(self.logFile)
            logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                filename=self.logFile,
                )

            logger = logging.getLogger('MyLogger')
        else:
            logger = None

        for chunk in self.commands:

            toRun = []
            
            if isinstance(chunk, dict):
                for key, command in chunk.items():
                    toRun.append(threading.Thread(name= key, target=runCommand, args=[command, logger]))

            elif isinstance(chunk, list):
                for command in chunk:
                    toRun.append(threading.Thread(target=runCommand, args=[command, logger]))

            else:
                raise TypeError('I want a list or a dictionary!')

            for t in toRun:
                t.start()
            for t in toRun:
                t.join()

        
