# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- 7oars.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""pyjobs is library for getting more out of pyprocessing (soon
to become included in the Python standard library as multiprocessing).
"""

import threading
import processing
import stopwatch

__version__ = '0.1.0'
__author__ = 'John Paulett <http://blog.7oars.com>'
__all__ = ['LocalJobRunner']


class LocalJobRunner(threading.Thread):
    """Maximizes CPU resources to run processing.Process instances.
    The LocalJobRunner takes FIFO queue of processes that need to 
    be run, and starts them so that (by default) each core or 
    processor is running a single job.  As processes finish, new
    ones are pulled from the queue and started.
    
    Once finished, LocalJobRunner.times provides a dictionary
    of run times for each individual process, keyed by the process
    name.  LocalJobRunner.finished indicates whether all the 
    processes are finished.  LocalJobRunner.runtime provides to 
    overall runtime of the LocalJobRunner.
    
    Gracefully kills all running processes upon sys.exit() or a
    KeyboardInterrupt.
    """
    def __init__(self, jobs, nprocesses=processing.cpuCount()):
        """
        Parameters:
        jobs - an FIFO list of instances of processing.Process that the 
            JobRunner will start
        nprocesses - the number of processes to have concurrently running.  
            Default: the number of processors on the machine
        
        """
        super(LocalJobRunner, self).__init__()
        self._nprocesses = nprocesses
        # make copy to use as a FIFO queue
        self._queue = jobs[:]
        self._queue.reverse()
        
        self._running = []
        self.times = {}
        self.__finished = False
        
    def run(self):
        self.runtime = stopwatch.Timer()
        try:
            while len(self._queue) > 0 or len(self._running) > 0:
                # currently asymmetric (multiple jobs can be removed, 
                # only a single one can be started within a loop
                self.__handle_finished()
                self.__start_job()
        except (KeyboardInterrupt, SystemExit):
            # make sure to kill processes to avoid runaways
            for job in self._running:
                try:
                    job.terminate()
                except:
                    # ignore
                    pass
                self.times[job.getName()].stop()
            raise
        finally:
            self.__finished = True
            self.runtime.stop()
        
    def __handle_finished(self):
        """If anyone of the processes are finished, we make space for
        new processes to run.
        """
        remove_jobs = []
        for job in self._running:
            if not job.isAlive():
                self.times[job.getName()].stop()
                # avoid removing finished jobs from list while iterating
                remove_jobs.append(job)
                
        for job in remove_jobs:
            self._running.remove(job)
    
    def __start_job(self):
        """Starts up a process if the resources are available.        
        """
        if len(self._running) <  self._nprocesses and len(self._queue) > 0:
            job = self._queue.pop()
            self._running.append(job)
            self.times[job.getName()] = stopwatch.Timer()
            job.start()
            
    @property
    def finished(self):
        return self.__finished


