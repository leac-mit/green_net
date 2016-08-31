from wemo import *
import time
"""
def get_query(print_str):
    query = raw_input(print_str)
    return "y" in query or "Y" in query

if get_query("get help- press q to quit"):
    get_help()

if get_query("turn on"):
    turn_on()

if get_query("turn off"):
	turn_off()
"""
while True:
    query = raw_input ("\non or off\n\t")
    if query == "on":
        print "turning on"
        turn_on()
    elif query == "off":
        print "turning off"
        turn_off()
    else:
        print "I do not understand command %s " % query
        

