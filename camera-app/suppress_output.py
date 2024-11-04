import os
import sys
from contextlib import contextmanager

@contextmanager
def suppress_output():
    """標準出力とエラー出力を一時的に無効化"""
    with open(os.devnull, 'w') as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
