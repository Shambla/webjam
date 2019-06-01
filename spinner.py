import itertools
import sys
import time


def spin(check):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while check():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
