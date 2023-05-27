import getopt
import winsound
import sys
import win_precise_time as wpt

DEFAULT_FREQ = 440.0
DEFAULT_LEN = 200
DEFAULT_REQ = 1
DEFAULT_DELAY = 100

STDIN_BEEP_NONE = 0
STDIN_BEEP_LINE = 1
STDIN_BEEP_CHAR = 2

def parse_args():
    optlist, args = getopt.gnu_getopt(sys.argv[1:], "f:l:r:d:D:schvVn", ['help', 'version', 'new', 'verbose'])

    results = []
    freq = DEFAULT_FREQ
    len = DEFAULT_LEN
    req = DEFAULT_REQ
    delay = DEFAULT_DELAY
    ddmode = False
    stdinmode = STDIN_BEEP_NONE

    for arg, val in optlist:
        arg = arg.lstrip('-')
        match arg[0]:
            case 'f':
                freq = float(val)
            case 'l':
                len = round(float(val))
            case 'r':
                req = int(val)
            case 'd': # delay between
                ddmode = False
                delay = round(float(val))
            case 'D': # delay after
                ddmode = True
                delay = round(float(val))
            case 's':
                stdinmode = STDIN_BEEP_LINE
            case 'c':
                stdinmode = STDIN_BEEP_CHAR
            case 'n':
                results.append([freq, len, req, delay, ddmode])
                freq = DEFAULT_FREQ
                len = DEFAULT_LEN
                req = DEFAULT_REQ
                dval = 0
                ddval = 0
            case ch:
                print('Unknown arg', ch, file=sys.stderr)

    results.append([freq, len, req, delay, ddmode])
    return (results, stdinmode)

def play(beeps: list):
    for beep in beeps:
        freq, len, req, delay, isD = beep
        for idx in range(req):
            f = round(freq)
            if f > 32767 or f < 37:
                print('Ignore Freq', freq)
            else:
                winsound.Beep(f, len)
            if isD or idx < req-1:
                wpt.sleep(delay / 1000)

args = parse_args()
if args[1] == STDIN_BEEP_NONE:
    play(args[0])
else:
    while True:
        if args[1] == STDIN_BEEP_LINE:
            result = sys.stdin.readline()
        elif args[1] == STDIN_BEEP_CHAR:
            result = sys.stdin.read(1)
        else:
            raise RuntimeError
        play(args[0])
