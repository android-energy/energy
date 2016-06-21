import threading
import time

from collections import namedtuple
from model import ComponentModel

ModemState = namedtuple('ModemState', 'name current timeout')

class Modem(ComponentModel):

    def __init__(self):
        super(self.__class__, self).__init__()

        self._states = [
            ModemState('DCH',  current=800,  timeout=5 ),
            ModemState('FACH', current=300,  timeout=10),
            ModemState('PCH',  current=100,  timeout=1 ),
            ModemState('OFF',  current=0,    timeout=0 ),
        ]
        self._set_state(-1)

    def get_current(self):
	return self.get_state().current

    def _handle_event(self, e):
        print 'modem: activated'
        self._set_state(0)

    def _update(self):
        print 'modem: {m._timeout:>3}s {s.name:>4} {s.current:>3}mA'.format(m=self, s=self.get_state())
        
        if self._timeout > 0:
            self._timeout -= 1
        else:
            self._next_state()
        time.sleep(1)

    def _next_state(self):
        if 'OFF' != self.get_state().name:
            self._set_state(self._current + 1)

    def _set_state(self, state):
        self._timeout = self._states[state].timeout
        self._current = state

    def get_state(self):
        return self._states[self._current]

