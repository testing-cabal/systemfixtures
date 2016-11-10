from fixtures import MonkeyPatch


class FakeThreads(MonkeyPatch):

    def __init__(self):
        super(FakeThreads, self).__init__("threading.Thread", self)
        self._threads = []
        self._hang = False

    def hang(self, flag=True):
        self._hang = flag

    def __getitem__(self, index):
        return self._threads[index]

    def __call__(self, *args, **kwargs):
        thread = _Thread(*args, **kwargs)
        if not thread.name:
            thread.name = "fake-thread-{}".format(len(self._threads))
        thread.hang = self._hang
        self._threads.append(thread)
        return thread


class _Thread(object):

    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs={}, daemon=None):
        self.group = group
        self.target = target
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.daemon = daemon
        self.alive = None  # None -> not started, True/False -> started stopped
        self.hang = None

    def start(self):
        if self.alive is not None:
            raise RuntimeError("threads can only be started once")
        self.alive = True
        if not self.hang:
            self.target(*self.args, **self.kwargs)
            self.alive = False

    def join(self, timeout=None):
        if self.alive is None:
            # It's an an error to join() a thread before it has been started
            raise RuntimeError("cannot join thread before it is started")
        if self.hang:
            if timeout is None:
                raise AssertionError(
                    "can't simulate hung thread with no timeout")

    def isAlive(self):
        return bool(self.alive)

    is_alive = isAlive
