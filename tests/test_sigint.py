import signal
from time import sleep

# https://stackoverflow.com/a/4205386/3211506

def _handler(sig, frame):
    print(f"Handling {sig}")
    raise KeyboardInterrupt

signals = [signal.SIGINT, signal.SIGABRT, signal.SIGFPE, signal.SIGILL, signal.SIGSEGV, signal.SIGTERM]

for i in signals:
    signal.signal(i, _handler)

class A():
    def __init__(self) -> None:
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, e_type, e_val, traceback):
        print("Exit")
        return
    
with A() as a:
    sleep(1)
    raise IOError