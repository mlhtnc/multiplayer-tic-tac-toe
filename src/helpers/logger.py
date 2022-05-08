import sys

def log(s):
    print(s)
    sys.stdout.flush()

def logError(s):
    print(s, file = sys.stderr)
    sys.stderr.flush()