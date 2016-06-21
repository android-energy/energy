import threading
import time

import Queue

from collections import namedtuple
from threading import _Event


class ComponentModel(object):

    def __init__(self):
        # self._tick = 1.0 #seconds
        self._running = False
        self._queue = Queue.Queue()
        self._thread = threading.Thread(target=self._loop)

    def get_current(self):
        raise NotImplementedError()

    def _handle_event(self, event):
        raise NotImplementedError()

    def _update(self):
        raise NotImplementedError()

    def _loop(self):
        while self._running:
            try:
                event = self._queue.get_nowait()
                self._handle_event(event)
            except Queue.Empty:
                pass
            self._update()
            # time.sleep(self._tick)

    def on_event(self, event):
        self._queue.put(event)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread.start()
        print '{s.__class__} started'.format(s=self)

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._thread.join()
        print '{s.__class__} halt'.format(s=self)


class Model(ComponentModel):

    def __init__(self, device):
        super(self.__class__, self).__init__()
        self._components = {}
        self.device = device

    def add_component(self, event, component):
        self._components[event] = component

    def get_current(self):
        return sum([c.get_current() for c in self._components.values()])

    def _handle_event(self, event):
        # TODO: accept regex
        # print '_handle_event {}'.format(event)
        for k, v in self._components.items():
            if k in event:
                v.on_event(k)

    def _update(self):
         pass

    def start(self):
        for component in self._components.values():
            component.start()
        super(self.__class__, self).start()

    def run(self):
        self.start()
        self.device.run(model=self)

    def stop(self):
        for component in self._components.values():
            component.stop()

        super(self.__class__, self).stop()
        #self.device.stop()
