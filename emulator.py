import textwrap
import threading

from subprocess import Popen, PIPE

GRANULARITY = 1024

class Emulator(object):
    def __init__(self, bin, *args):
        self._running = False
        self._model = None
        self._buffer = ''
        self._thread = threading.Thread(target=self._loop)
        # self._process = Popen([bin]+list(args), stderr=PIPE)
        self._proc = Popen(['/home/diego/studio-dev/external/qemu/objs/emulator',
                            '-verbose', '@Nexus4'], stderr=PIPE, stdout=None)

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

    # TODO: register observer/listener
    def _loop(self):
        while self._running:
            # wait log buffer to fill
            # time.sleep(1)
            for log in self._proc.stderr.read(GRANULARITY):
                self._buffer += log

            lines = self._buffer.splitlines()

            # last line may be incomplete
            events = '\n'.join(lines[:-1])
            # left the last line in the buffer
            self._buffer = lines[-1]

            if events:
                # print textwrap.dedent('''
                # ---------------------------------------------------
                # {}
                # ---------------------------------------------------
                # ''').strip().format(events)
                self._model.on_event(events)
