import threading
import time
import random

from subprocess import Popen, PIPE

class Emulator(object):
    def __init__(self, bin, *args):
        self._running = False
        self._model = None
        self._thread = threading.Thread(target=self._loop)
        # self._process = Popen([bin]+list(args), stderr=PIPE)
        self._proc = Popen(['/home/diego/studio-dev/external/qemu/objs/emulator',
                            '-verbose', '@Nexus4'], stderr=PIPE)

    def run(self, model):
        self.start(model)
        self._thread.join()

    def start(self, model):
        if self._running:
            return
        self._model = model
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            for e in self._proc.stderr.readline():
                self._model.on_event(e)
