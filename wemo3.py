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
    switch = env.get(name)
    return switch

def get_help():
    help(switch_1)

def turn_off():
    switch_1.off()
def turn_on():
    switch_1.on()
def toggle():
    switch_1.toggle()

def get_power():
    return switch_1.current_power



switch_1 = None
try:
    switch_1 = get_device('switch_1')
    switch_2 = get_device('switch_2')
except:
    print "could not connect all devices. are you on green_net?"
    sys.exit(1)

if __name__=="__main__":
#    get_help()
    for i in range (1000):
        cur_pwr_1 = switch_1.current_power
        cur_pwr_2 = switch_2.current_power
        print cur_pwr_1, cur_pwr_2
#        print get_power()
        time.sleep(0.01)
