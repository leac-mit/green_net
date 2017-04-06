import random
import datetime
import time
import ouimeaux
from ouimeaux.environment import Environment
import sys

def get_device(name):
    env = Environment()
    # TODO: run from 10am to 10pm
    env.start()
    print "Discovering Device"
    env.discover(5)
    h = env.get(name)
    return h

def get_help():
    help(h)

def turn_off():
    h.off()
def turn_on():
    h.on()
def toggle():
    h.toggle()

def get_power():
    return h.current_power



h = None
try:
    h = get_device('hello wemo')
except:
    print "could not connect device. are you on green_net?"
    sys.exit(1)

if __name__=="__main__":
    get_help()
    for i in range (100):
        print get_power()
        time.sleep(1)
