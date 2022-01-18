'''Implementation of basic classes for programming discrete event simulations.
'''

import queue
from abc import ABC, abstractmethod


class Event(ABC):

    '''Base class of events. An event that occurs at a given time (a float
    value) and must be processed by a given server.
    '''

    def __init__(self, time, server):
        '''Create a new event for a given server at a given time.'''
        self._time = time
        self._server = server

    def time(self):
        '''Return event time.'''
        return self._time

    def server(self):
        '''Return server associated with the event.'''
        return self._server

    @abstractmethod
    def process(self):
        '''Execute the action associated with the event.'''
        pass

    # Operator < is used to order events in the calendar
    def __lt__(self, other):
        '''Order event by event time.'''
        return self.time() < other.time()


class Server:

    '''Servers are responsible for the implementation of the methods that will
    do the work associated with event processing. They can generate new events
    that are inserted into the calendar.
    '''

    def __init__(self, calendar):
        '''Initializes a server. Stores the calendar for reference.'''
        self._cal = calendar

    def calendar(self):
        '''Return the calendar associated with this server'''
        return self._cal


class Calendar:

    '''Event calendar. The event to be removed is always the one with smallest
    scheduled time.
    '''

    def __init__(self):
        '''Creates a new empty calendar. Start time at 0.0.'''
        self._queue = queue.PriorityQueue()
        self._current_time = 0.0

    def current_time(self):
        '''Return the current time (time of last removed event).'''
        return self._current_time

    def put(self, event):
        '''Insert event in the calendar.'''
        if not isinstance(event, Event):
            raise TypeError('Argument to Calendar.put must be an Event.')
        if event.time() < self._current_time:
            raise ValueError('New event is previous to last removed event.')
        self._queue.put(event)

    def get(self):
        '''Get next event and remove it from calendar.'''
        event = self._queue.get()
        self._current_time = event.time()
        return event

    def process_all_events(self):
        '''Keep processing events until eventually the calendar is empty.'''
        while not self._queue.empty():
            ev = self.get()
            ev.process()

    def process_events_until(self, timeout):
        '''Process events until the next event has timestamp larger than the
        specified timeout.'''
        while not self._queue.empty():
            event = self._queue.get()
            if event.time() <= timeout:
                self._current_time = event.time()
                event.process()
            else:  # Next event is after timeout
                self._queue.put(event)  # Put it back (not yet processed)
                break
