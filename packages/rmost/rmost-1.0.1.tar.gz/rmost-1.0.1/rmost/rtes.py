import sys


def start(filename):
    sys.stdin = open(filename)


def run(function, count):
    [function() for _ in range(count - 1)]


def finish():
    sys.stdin.close()
    sys.stdin = sys.__stdin__