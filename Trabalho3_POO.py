'''Run jobs/processors simulations.'''

from queue import Queue
import random
from collections import namedtuple
import sys

from desimul import Calendar, Event, Server

# Auxiliary simulation classes

class Job:
	'''Implements methods to verify waiting times for each job.'''

	def __init__(self, processing_time, priority):
		'''Create a new job with the specified processing time and priority.'''
		self._arrival_time = None
		self._departure_time = None
		self._processing_time = processing_time
		self._priority = priority

	def arrival(self, time):
		'''Called when job arrives.'''
		self._arrival_time = time

	def departure(self, time):
		'''Called when job departs.'''
		self._departure_time = time

	def report(self):
		'''Report on arrival and departure times (for statistics).'''
		return self._arrival_time, self._departure_time
        
	def processing_time(self):
		'''Inform the time to process the job.'''
		return self._processing_time
    
	def priority(self):
		'''Inform the job's priority.'''
		return self._priority 

# Server classes

class QueueingSystem(Server):
    '''Abstract base class for job queueing system.'''

    def __init__(self, calendar):
        '''Creates a queue associated with the given calendar.'''
        Server.__init__(self, calendar)
        self._free_processors = Queue()  # This stores the free processors.
        self._queue_priority = Queue()   # This stores the priority jobs.
        self._queue_normal = Queue()     # This stores the normal jobs.

    def new_job(self, job):
        '''A new job to process. Either send it to a free processor (if
        available) or to the waiting queue.'''
        if self._free_processors.empty():
            # No free processors. Put job on the queue.
            self.enqueue(job)
        else:
            # There is a free processor. Send job to them.
            processor = self._free_processors.get()
            cal = self.calendar()
            now = cal.current_time()
            event = JobToProcessorEvent(now, processor, job)
            cal.put(event)

    def free_processor(self, processor):
        '''A new free processor. Send it a job (if one is waiting) or put it in
        the waiting queue.'''
        if self.has_waiting_job(processor):
            # There is a job waiting.
            job = self.get_next_job(processor)
            cal = self.calendar()
            now = cal.current_time()
            event = JobToProcessorEvent(now, processor, job)
            cal.put(event)
        else:
            # No job waiting. Put processor in the free processors queue.
            self._free_processors.put(processor)

    def enqueue(self, job):
        '''Put the job at the back of the queue according its priority.'''
        if job.priority() == 1:
            self._queue_priority.put(job)
        if job.priority() == 0:
            self._queue_normal.put(job)

    def has_waiting_job(self, processor):
        '''Verify if the processor has a waiting job.'''
        return not self._queue_priority.empty() or not self._queue_normal.empty()

    def get_next_job(self, processor):
        '''Get the next job for the given processor, first verifying if there are any priority jobs.'''
        if not self._queue_priority.empty():
            return self._queue_priority.get()
        elif not self._queue_normal.empty():
            return self._queue_normal.get()

class Processor(Server):
	'''Processors know how to process a job.'''

	def __init__(self, calendar, queue):
		'''Create a processor server associated with the given calendar and queue.'''
		Server.__init__(self, calendar)
		self._queue = queue
		self._free_time = []
		self._last_attending = 0.0
		self.quantity = 0
		self.priority_quantity = 0

	def attend_job(self, job):
		'''Do the process required by the job (takes time). Afterwards, notify
        queue about free status.'''
		curr_time = self.calendar().current_time()
		self._free_time.append(curr_time - self._last_attending)
		time_to_finish = job.processing_time()
		finish_time = curr_time + time_to_finish
		job.departure(finish_time)
		event = ProcessorFreeEvent(finish_time, self._queue, self)
		self.calendar().put(event)
		self._last_attending = finish_time
		self.quantity += 1
		if job.priority() == 1:
			self.priority_quantity += 1
        

	def free_times(self):
		'''Return a list of all idle interval lengths.'''
		return self._free_time


# Event types

class JobArrivalEvent(Event):
    '''A job has arrived.'''

    def __init__(self, time, queue, job):
        '''Creates an event of the given job arriving at the given queue at
        the given time'''
        Event.__init__(self, time, queue)
        self._job = job

    def process(self):
        '''Record arrival time in the job and insert it in the queue.'''
        self._job.arrival(self.time())
        self.server().new_job(self._job)


class JobToProcessorEvent(Event):
    '''Job is sent to a free processor.'''

    def __init__(self, time, processor, job):
        '''Create an event of a given processor starting to execute a given
        job at a given time.'''
        Event.__init__(self, time, processor)
        self._job = job

    def process(self):
        '''Processor should attend to job.'''
        self.server().attend_job(self._job)


class ProcessorFreeEvent(Event):
    '''A processor has become free.'''

    def __init__(self, time, queue, processor):
        '''Creates an event of a given processor becoming free.'''
        Event.__init__(self, time, queue)
        self._free_processor = processor

    def process(self):
        '''Notify queueing system of the free processor.'''
        self.server().free_processor(self._free_processor)


# Simulations

Job_par = namedtuple('Job_par', ['number', 'time', 'arrival', 'priority'])
Processor_par = namedtuple('Processor_par', ['number'])

# Auxiliary writing functions


def write_job_data(jobs):
    '''Writes job timing and priority information to file 'jobs.dat'.'''

    with open('jobs.dat', 'w') as outfile:
        for job in jobs:
            arrival, departure = job.report()
            print(arrival, job.priority(), job.processing_time(), departure - job.processing_time(), file=outfile)


def write_free_times(processors):
    '''"Writes processor information to file 'processors.dat'.'''

    with open('processors.dat', 'w') as outfile:
        for processor in processors:
            freetimes = processor.free_times()
            total_free_time = sum(freetimes)
            print(processor.quantity, processor.priority_quantity, total_free_time, file=outfile)


# Perform a simulation and save results

def simple_simulation(processors_p, jobs_p):
    '''Perform simulation for the given queueing system, processor and job
    parameters. Save the results in files 'processors.dat' and 'jobs.dat'.'''

    # Create simulation infrastructure.
    calendar = Calendar()
    queue = QueueingSystem(calendar)

    # Create all processors.
    processors = [Processor(calendar, queue)
               for i in range(processors_p.number)]

    # Insert initial events of free processor for all processors (ready to work).
    for processor in processors:
        calendar.put(ProcessorFreeEvent(0.0, queue, processor))

    # Create all jobs.
    jobs = [Job(next(jobs_p.time), next(jobs_p.priority)) for i in range(jobs_p.number)]

    # Create the events of job arrival for all jobs.
    for i, job in enumerate(jobs):
        calendar.put(JobArrivalEvent(next(jobs_p.arrival), queue, job))

    # Process all events until finished.
    calendar.process_all_events()

    # Write results to files.
    write_job_data(jobs)
    write_free_times(processors)

    print('Total simulation time for this test is', calendar.current_time())


# Code to run

if __name__ == '__main__':
	
	#Read the parameters from command line.
	p, tau, sigma, T, m, alpha = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
	p, tau, sigma, T, m, alpha = int(p), float(tau), float(sigma), float(T), int(m), int(alpha)
	
	def get_collection_number(collection):
		'''Yields a number that could be the arrival time, the processing time or the priority.'''
		counter = 1
		while counter <= len(collection):
			yield collection[counter - 1]
			counter += 1
	
	#List that contains the processing times.		
	collection_time = [random.gauss(tau, sigma) for i in range(m + m//alpha)]
	
	#List that contains the arrival times.
	collection_arrival_time = [T*random.random() for x in range(m + m//alpha)]
	collection_arrival_time.sort()
	
	#List of job's priority, where shuffle() make the senquence of priorities be random.
	collection_zero = [0]*m
	collection_one = [1]*(m//alpha)
	collection_priority = collection_zero + collection_one
	random.shuffle(collection_priority)

	# Run simulation configurations.
	simple_simulation(Processor_par(p), Job_par(m + m//alpha, get_collection_number(collection_time), get_collection_number(collection_arrival_time), get_collection_number(collection_priority)))
