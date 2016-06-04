import atexit
import json
import os
import socket;
import subprocess
import sys

from opt import pg_logger

try:
    from urllib2 import urlopen
    from urlparse import urlparse
    viewitems = lambda x: x.iteritems()
except ImportError:  # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlparse
    viewitems = lambda x: x.items()

# If you're hosting the server remotely, then change this address:
SERVER_ADDR = "http://localhost:8888/"
assert SERVER_ADDR[-1] == '/'

# Standardize display of floats to 3 significant figures
#
# Trick from:
# http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module
json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)

# INDENT_LEVEL = 2    # human-readable
INDENT_LEVEL = None  # compact

# TODO: support incremental pushes to the OPT frontend for efficiency
# and better "snappiness"
#
# I think the easiest way to do diffs is to set INDENT_LEVEL = 2 above
# and then simply send the diff of the JSON string to the server.
# It's WAY TOO COMPLICATED to try implementing semantic diffs of the
# OPT trace ourselves, since there are too many corner cases.
#
# text diffs are an elegant solution :)
#
# https://code.google.com/p/google-diff-match-patch/


class OptHistory(object):
    def __init__(self):
        self.executed_stmts = []

    def pop_last(self):
        self.executed_stmts.pop()

    def get_code(self):
        return '\n'.join(self.executed_stmts)

    def run_str_and_broadcast(self, stmt_str):
        """Run stmt_str and transmit trace to server"""

        self.executed_stmts.append(stmt_str)

        opt_trace = pg_logger.exec_script_str_local(
            self.get_code(), [], False, False, lambda cod, trace: trace)

        last_evt = opt_trace[-1]['event']
        if last_evt == 'exception':
            epic_fail = True
        else:
            assert last_evt == 'return'
            epic_fail = False

        trace_dict = dict(code=self.get_code(), trace=opt_trace)
        json_output = json.dumps(trace_dict, indent=INDENT_LEVEL)

        # if this statement ended in an exception, delete it from the
        # history and pretend it never happened
        if epic_fail:
            self.pop_last()

        urlopen(SERVER_ADDR + 'wholetrace', json_output.encode())


# called right before a statement gets executed
def opt_pre_run_code_hook(self):
    # when you run multiple statements on one line using a semicolon:
    # e.g., "print x; print y", this function will fire multiple times.
    # we want to avoid duplicates!
    last_cmd = self.history_manager.input_hist_parsed[-1]
    last_cmd_index = len(self.history_manager.input_hist_parsed) - 1

    # also don't intercept special ipython commands
    if 'get_ipython().' in last_cmd:
        return

    if self.meta.last_cmd_index == last_cmd_index:
        assert self.meta.last_cmd == last_cmd
        return  # punt!!!

    self.meta.last_cmd = last_cmd
    self.meta.last_cmd_index = last_cmd_index

    self.meta.opt_history.run_str_and_broadcast(last_cmd)


def opt_clear(self, params):
    ip = self.shell

    filtered_user_ns = set()
    for k, v in viewitems(ip.user_ns):
        if k[0] == '_':
            continue
        if k in ('In', 'Out', 'help', 'quit', 'exit', 'get_ipython'):
            continue
        filtered_user_ns.add(k)

    for k in filtered_user_ns:
        del ip.user_ns[k]

    ip.meta.opt_history = OptHistory()  # just create a new one!

    urlopen(SERVER_ADDR + 'clear', 'blub'.encode())  # need a non-empty POST body

    print("\n\tExtension reset!")


def run_server(self, params):

    try:
        null = subprocess.DEVNULL
    except:  # Python 2
        null = open(os.devnull, 'w')

    server = os.path.join(os.path.dirname(__file__),
                          'opt/server/opt_ipy_server.py')

    p = subprocess.Popen([sys.executable, server], stderr=null)
    atexit.register(lambda: p.terminate())

    sock = socket.socket()
    addr = urlparse(SERVER_ADDR)
    if not sock.connect_ex((addr.hostname, addr.port)):
        sock.close()

        print("\n\tTornado server started!")

        if sys.platform.startswith('darwin'):
            subprocess.Popen(('open', SERVER_ADDR))
        elif os.name == 'nt':
            os.startfile(SERVER_ADDR)
        elif os.name == 'posix':
            subprocess.Popen(('xdg-open', SERVER_ADDR))
    else:
        try:
            import tornado
            raise Exception('Server failed to start!')
        except ImportError:
            raise Exception('Tornado is required while it is not available!')


def usage():
    msg = """
    Online Python Tutor extension loaded!

    Additional commands:

        %clear      - Clear global namespace and reset history
        %run_server - Run tornado server and open default browser
    """
    return msg


def load_ipython_extension(ip):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.

    ip.meta.opt_history = OptHistory()
    ip.meta.last_cmd = None
    ip.meta.last_cmd_index = -1  # set to an impossible initial value

    # NB: spelling might be different in older IPython versions
    ip.set_hook('pre_run_code_hook', opt_pre_run_code_hook)
    ip.define_magic('run_server', run_server)
    ip.define_magic('clear', opt_clear)

    ip.write(usage())


def unload_ipython_extension(ip):
    # If you want your extension to be unloadable, put that logic here.
    pass
