import random
import datetime
import time
import ouimeaux
from ouimeaux.environment import Environment
def get_device(name):
    env = Environment()
    # TODO: run from 10am to 10pm
    env.start()
    print "hi"
    env.discover(1)
    h = env.get(name)
    return h

def get_power():
    return h.current_power
h = None
try:
    h = get_device('hello wemo')
except:
    print "could not connect device. are you on green_net?"
    
if __name__=="__main__":
    for i in range (100):
        print get_power()
        time.sleep(1)
