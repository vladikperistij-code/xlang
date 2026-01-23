# runtime.py
import time

def x_print(*args):
    print("".join(str(a) for a in args))

def x_input(prompt=""):
    return input(prompt)

def x_sleep(sec=1):
    time.sleep(sec)
