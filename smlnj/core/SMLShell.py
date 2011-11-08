import re
import signal
import sys
import smlnj

try:
    import readline
except ImportError:
    print >> sys.stderr, 'readline module not available on your system'
    exit(1)

NDEBUG = True

def debug (func):
    """
    Decorator function, prints debug information.
    """
    def wrapper (*args, **kwargs):
        print >> sys.stderr, 'calling %s' % func.__name__
        value = func(*args, **kwargs)
        print >> sys.stderr, 'done %s' % func.__name__
        return value
    return func if NDEBUG else wrapper

class SMLShell (object):
    """
    An SML shell.
    """

    matchidents = r'''
    val\s+(\S+)\s* |
    fun\s+(\S+)\s*\(.*\)
    '''
    matchregex = re.compile(matchidents, re.VERBOSE | re.LOCALE)
    prompt     = '(DEBUG) '

    def __init__ (self, sml):
        """
        Initializes a new console from an open sml process.
        """
        readline.parse_and_bind ('tab: complete')
        self.old_completer = readline.set_completer (self.complete)

        self.identifiers = smlnj.util.PrefixTree()
        self.matches, self.sml = [], sml

        self.stdout = smlnj.util.SynchronizedStreamReader(self.sml.stdout)
        self.stderr = smlnj.util.SynchronizedStreamReader(self.sml.stderr)

        self.stdout.start()
        self.stderr.start()

    def __del__ (self):
        readline.set_completer (self.old_completer)

    @debug
    def complete (self, text, state):
        """
        Readline completer function.
        """
        if not state:
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped

            self.matches = self.get_matches(text, line, begidx, endidx)
        return self.matches[state]

    @debug
    def get_matches (self, text, line, begidx, endidx):
        """
        Returns auto-completion matches for input.
        """
        if line == '' and self.prompt == '= ':
            return ['  ']

        return self.identifiers.prefix(text)

    @debug
    def main (self):
        """
        Main loop of shell.
        """
        while self.sml.poll() is None:
            try:
                self.pre_prompt()
                line = raw_input(self.prompt)
                self.post_prompt(line)
            except EOFError:
                self.terminate()
                self.sml.wait()
            except KeyboardInterrupt:
                pass

    @debug
    def pre_prompt (self):
        """
        Handles and parses output from underlying process.
        """
        read, line = '', ''

        while True:
            read += self.stdout.read()

            if read.startswith('- ') or read.startswith('= '):
                self.prompt = read
                break

            if '\n' in read:
                line, read = read.rsplit('\n', 1)
                sys.stdout.write(line + '\n')

                for match in self.matchregex.findall(line):
                    map (self.identifiers.add, match)

            map (sys.stderr.write, self.stderr.readlines())

    @debug
    def post_prompt (self, line):
        """
        Handles and parses input to the underlying process.
        """
        self.sml.stdin.write(line + '\n')
        for match in self.matchregex.findall(line):
            map (self.identifiers.add, match)

    @debug
    def terminate (self):
        """
        Terminates the underlying process.
        """
        self.sml.stdin.close()
