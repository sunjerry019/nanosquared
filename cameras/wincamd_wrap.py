import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.wincamd as wcd
import time

with wcd.WinCamD() as w:
    f = open('umu.txt', 'w')

    w.startDevice()
    x = w.getAxisProfile('x')
    y = w.getAxisProfile('y')

    f.write(f"x\n\n{x.tolist()}\n\n")
    f.write(f"y\n\n{y.tolist()}\n")

    f.close()


    