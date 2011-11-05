import Queue
import threading

def synchronized (func):
    """
    Decorator for synchronized access to methods.
    """
    def wrapper (self, *args, **kwargs):
        self.mutex.acquire()

        value = func (self, *args, **kwargs)

        self.mutex.release()
        return value
    return wrapper

class SynchronizedStreamReader (threading.Thread):
    """
    Daemon that facilitates non-blocking synchronous access
    to a blocking stream.
    """
    def __init__ (self, stream):
        """
        Initializes a new instance from an open stream.
        """
        super (SynchronizedStreamReader, self).__init__()

        self.stream, self.daemon = stream, True
        self.mutex,  self.bytes  = threading.Lock(), Queue.Queue()
        self.lines = 0

    @synchronized
    def read (self):
        """
        Returns what has been read so far.
        """
        s = []

        try:
            while True:
                s.append (self.bytes.get_nowait ())
        except Queue.Empty:
            pass

        self.lines = 0

        return ''.join(s)

    @synchronized
    def readlines (self):
        """
        Returns the lines that have been read so far
        as a list of strings.
        """
        s, line = [], []

        try:
            while self.lines:
                byte = self.bytes.get_nowait ()

                line.append (byte)

                if byte == '\n':
                    self.lines -= 1
                    s.append (''.join(line))
                    line = []
        except Queue.Empty:
            pass

        return s

    def run (self):
        """
        Main loop of daemon.
        """
        s = True
        while s:
            s = self.stream.read(1)

            if s == '\n':
                self.lines += 1

            self.bytes.put(s)
