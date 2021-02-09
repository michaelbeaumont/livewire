import os
import sys
from contextlib import contextmanager


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


@contextmanager
def open_or_stdout(filename=None):
    if filename and filename != "-":
        fh = open(filename, "w")
        os.chmod(fh.name, 0o600)
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


@contextmanager
def open_or_stdin(filename=None):
    if filename and filename != "-":
        fh = open(filename)
    else:
        fh = sys.stdin

    try:
        yield fh
    finally:
        if fh is not sys.stdin:
            fh.close()
