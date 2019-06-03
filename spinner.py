import itertools
import sys
import time


def spin(shouldSpin, completeMessage):
    """
    Prints an ASCII-based spinner in the terminal, until the callback function
    returns False.

    :param shouldSpin: the callback function to determine if spinning should occur
    :param completeMessage: the message to print upon completion
    :return: nothing
    """
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while shouldSpin():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    print(completeMessage)
