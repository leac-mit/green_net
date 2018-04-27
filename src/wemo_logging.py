#!/usr/bin/env python
# Author: Ariel Anders, Joseph Powell

import numpy as np
import datetime
import time
import ouimeaux
from ouimeaux.environment import Environment
import sys
from threading import Thread
import pdb
from argparse import ArgumentParser

from multiprocessing import Process, Queue


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def get_name(num):
    if num < 10:
        name = "switch_%d" % num
    else :
        name = "switch_%s" % alphabet[num-10] 
    return name

MAX_DEVICES = 15

class WemoLogger ():
    ASYNCH_RELOAD=10 # test reload switches every ASYNCH_RELOAD seconds
    LOG_FREQ = 5 # # log new data every LOG_FREQ seconds

    def __init__(self, num_devices=1, debug=True):
        self.debug = debug
        print "initalizing the wemos for %s devices" % (num_devices)
        self.NUM_DEVICES = num_devices
        self.switches = {}
        self.devices = range(0, self.NUM_DEVICES)
        self.q = Queue()
    
        try:
            self.env = Environment()
            self.env.start()
        except:
            print """
                Failed to access internet information. 
                Are you connected to green net?"""
            sys.exit(1)

        
        self.load_switches()
        
        if len(self.switches) == 0:
            print "could not connect any devices. are you on green_net?"
            sys.exit(1)

        print """
                Done connecting devices.  
                Starting asynchronous wemo reloader now!"""

        self.thread = Thread(target=self.reload_switch_spinner)
        self.thread.start()

    def reload_switch_spinner(self):
        while True:
            if len(self.switches) != self.NUM_DEVICES:
                self.load_switches()
            time.sleep(self.ASYNCH_RELOAD)

    def load_switches(self, timeout=90):
        print "Entering discovery mode for %s seconds" % timeout
        self.env.discover(timeout)
        print "Done with Discovery.  Starting to sync switches"
        
        for i in self.devices:
            if i in self.switches:
                #print "#XXX run test to make sure switch is active"
                active = True #XXX fix me
                if active: 
                    #print "skipping switch %s - already active" % get_name(i)
                    continue
                else:
                    del self.switches[i]

            try:
                self.switches[i] = self.env.get(get_name(i))
                print "\t\tsuccess! connected to switch %s " % get_name(i)
            except:
                print "\tfail! could not connect device %s " % get_name(i)
        if args.debug:
            for i in range(0, 15):
                if i in self.switches:
                    print i, get_name(i), self.switches[i]
            #raw_input("press enter if naming is correct")
    
    def get_switch_power(self, i):
        try:
            power = self.switches[i].current_power
            if self.debug: print "got data for %s , %s" % (get_name(i), power)
        except:
            power = -1
        self.q.put( (i, power))
    
    def get_data_old(self):
        data = [0.0]*self.NUM_DEVICES
        del_list = []
        for i in self.devices:
            if i in self.switches:
                #TODO Paralleize this
                p = Process(target=self.get_switch_power, args=(i,))
                p.start()
                p.join(3) # timeout 2 seconds
                if p.is_alive():
                    print "collecting data from %s took too long " % get_name(i)
                    p.terminate()
                    p.join()
                    del_list.append(i)
        for t in range(self.q.qsize()):
            i, power = self.q.get()
            data[i] = power
            if (power == -1) and (i in self.switches) and (i not in del_list):
                if self.debug: print "removing %s from list because power was 0" % get_name(i)
                del_list.append(i)

        for i in del_list:
            del self.switches[i]
        return data



    def get_data(self):
        data = [0.0]*self.NUM_DEVICES
        del_list = []
        p = [None]*self.NUM_DEVICES
        for i in self.devices:
            if i in self.switches:
                #TODO Paralleize this
                p[i] = Process(target=self.get_switch_power, args=(i,))
                p[i].start()
        time.sleep(self.LOG_FREQ)
        for i in self.devices:
            if i in self.switches:
                if p[i] and p[i].is_alive():
                    print "collecting data from %s took too long " % get_name(i)
                    p[i].terminate()
                    #p[i].join()
                    del_list.append(i)
        for t in range(self.q.qsize()):
            i, power = self.q.get()
            data[i] = power
            if (power == -1) and (i in self.switches) and (i not in del_list):
                if self.debug: print "removing %s from list because power was 0" % get_name(i)
                del_list.append(i)

        for i in del_list:
            del self.switches[i]
        return data

    '''def get_energy(self, data):
	energy = [0.0]*len(data)
		
	i = 0
	while i < len(data):
		energy[i] = data[i] * 0.1
		
	return energy'''
	
    def get_energy(dat, time):
	return dat*time
					    
    def write_data(self,data):
        string = ""
        for date, dat, energy in data:
            string += "%s%s\n" % (date, (",").join([str(d) for d in dat])) 
        with open('data.csv', 'a') as f:
            f.write(string)

    def run(self):
        iters = 1
        last_time = time.time()
        data = [] 
        while True:

            # only write data every 5 data points
            if iters % 1 == 0 : 
                self.write_data(data)
                iters=0
                data = []
            else:
                iters += 1

            # pause before collecting more data
            #time.sleep(self.LOG_FREQ)
            
            # get data
            dat = self.get_data()

            # get date and delta time
            date = time.strftime("%Y%m%d-%H:%M:%S,")
	    deltaT = time.time() - last_time
	    energy = self.get_energy(dat, deltaT)	
            date +="%s,"% (deltaT)
            last_time = time.time()

            # add date to list
            data.append ( (date, dat, energy))

parser = ArgumentParser(usage=\
	"""
	Welcome to wemo data logging by LEAC-MIT. 
	Enter the number of devices to log
	Use argument -d or --debug for printing debug statements
	eg: python wemo_logging.py 10 
	""")
parser.add_argument('num_devices', type=int)
parser.add_argument('-d',"--debug", action="store_true")
args = parser.parse_args()

try:
    assert args.num_devices > 0 and args.num_devices <= MAX_DEVICES
except:
    print """
    %s is an invalid number of devices. 
    The number must be between 1 and %d """ %\
    (args.num_devices, MAX_DEVICES)
    sys.exit(1)

def getWL():
    wl = WemoLogger(args.num_devices, args.debug)
    return wl

if __name__=="__main__":
    wl = getWL()
    wl.run()
    sys.exit(0)
