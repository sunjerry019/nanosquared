#!/usr/bin/env python3

# __getattr__ only gets called for attributes that don't actually exist. 
# If you set an attribute directly, referencing that attribute will retrieve 
# it without calling __getattr__.

# __getattribute__ is called all the times.

class A():
    def __init__(self) -> None:
        self.B = B()

    def __getattr__(self, name):
        def send(*args, **kwargs):
            return getattr(self.B, name)(*args, **kwargs)
        return send

    def func_a(self):
        print("A: func a")

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass


class B():
    def __init__(self) -> None:
        pass

    def func_a(self):
        print("B: func a")

    def func_b(self):
        print("B: func a")

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

if __name__ == '__main__':
    with A() as M:
        print("with A() as M")
        import code; code.interact(local=locals())
