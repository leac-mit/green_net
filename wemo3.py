import random
import datetime
import time
import ouimeaux
from ouimeaux.environment import Environment
import sys

NUM_DEVICES=5

def get_device(name):
    env = Environment()
    # TODO: run from 10am to 10pm
    env.start()
    print "Discovering Device %s" %name
    env.discover(5)
    this_switch = env.get(name)
    return this_switch

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
switches = {}

for device in range( NUM_DEVICES):
    try:
        switches[device] = get_device('switch_%d' % (device + 1) )
        print "connected device %d" %(device +1 )
    except:
        print "could not connect device %d " % (device +1 )
if len(switches.items())==0:
    print "could not connect all devices. are you on green_net?"
    sys.exit(1)


"""
try:
    switch_1 = get_device('switch_2')
    switch_2 = get_device('switch_3')
except:
    print "could not connect all devices. are you on green_net?"
    sys.exit(1)
"""
if __name__=="__main__":
#    get_help()
    for i in range (1000):
        cur_pwr_1 = switch_1.current_power
        cur_pwr_2 = switch_2.current_power
        print cur_pwr_1, cur_pwr_2
#        print get_power()
        time.sleep(0.01)
