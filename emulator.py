import threading
import time
import random

class Emulator(object):
    def __init__(self, bin):
        self._bin = bin
        self._running = False
        self._thread = threading.Thread(target=self._loop)

        self._model = None
        self._events = ('modem_driver_read', 'Started new RenderThread',
                        '', 'akljflaj', 'lkjkljsdj', 'gps on', 'gps off')

    def run(self, model):
        self.start(model)
        self._thread.join()

    def start(self, model):
        if self._running:
            return
        self._model = model
        self._running = True
        self._thread.start()
        self._thread.join()

    def stop(self):
        self._running = False

    def _loop(self):
        for i in range(300):
            next_event = random.randint(1, 10)
            print 'next event in {}s'.format(next_event)
            time.sleep(next_event)
            e = random.choice(self._events)
            print 'send event "{}"'.format(e)
            self._model.on_event(e)
