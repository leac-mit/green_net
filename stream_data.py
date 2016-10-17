#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Real time plot of serial data
#
# Copyright (C) 2012 Asaf Paris Mandoki http://asaf.pm
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from pygame.locals import *
from numpy import array, arange, zeros, roll
import numpy as np
import threading
from serial import Serial
from struct import unpack

import sys
import os
import time

from wemo3 import *
colors= [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 0)
        ]
pygame.init()


def say (text):
    os.system("espeak -a 200 -s 100 '%s'   2>/dev/null  &" % text)

class Oscilloscope():
    
    def __init__(self):
        self.w,self.h = (600, 400)
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.clock = pygame.time.Clock()
        self.data_buff_size = 200
        self.Y = {x:zeros(self.data_buff_size) for x in switches}
        self.y = zeros(self.data_buff_size)
        self.y2 = zeros(self.data_buff_size)
        self.x = arange(self.data_buff_size)
        self.run()
        


        
    def plot(self, x, Y, xmin, xmax, ymin, ymax):
        w, h =(self.w,400) # self.screen.get_size()
        for n in Y:
            y = array(Y[n])
            x = array(x)
            
            #Scale data
            xspan = abs(xmax-xmin)
            yspan = abs(ymax-ymin)
            xsc = 1.0*(w+1)/xspan
            ysc = 1.0*h/yspan
            xp = (x-xmin)*xsc
            yp = h-(y-ymin)*ysc
            
            #Draw grid
            for i in range(10):
                pygame.draw.line(self.screen, (210, 210, 210), (0,int(h*0.1*i)), (w-1,int(h*0.1*i)), 1)
                pygame.draw.line(self.screen, (210, 210, 210), (int(w*0.1*i),0), (int(w*0.1*i),h-1), 1)
                
            #Plot data
            for i in range(len(xp)-1):
                pygame.draw.line(self.screen, colors[n], (int(xp[i]), int(yp[i])), 
                                                         (int(xp[i+1]),int(yp[i+1])), 5)
                


    def run(self):

        #Things we need in the main loop
        font = pygame.font.Font(pygame.font.match_font(u'mono'), 20)
        i = 0
        while 1:
            #Process events
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            """if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
            """
            
            self.screen.fill((255,255,255))     
            # Display fps
            font = pygame.font.Font(pygame.font.match_font(u'mono'), 30)
            font.set_bold(True)
            title = "green_net"
		
            text1= font.render(title, True, (255, 10, 10))
            self.screen.blit(text1, (10, 10))
            for y in self.Y:
                self.Y[y] = roll(self.Y[y], -1)
                self.Y[y][-1] = switches[y].current_power

            xmin=0.
            ymin=0.
            xmax=float(self.data_buff_size)
            ymax=100000.
            self.plot(self.x,self.Y,xmin,xmax,ymin,ymax)
            pygame.display.flip()
            self.clock.tick(0)
            pygame.time.wait(1000)
            i += 1
            if i % 5 == 0:
                i = 0
                with open('data.csv', 'a') as f:
                    data = time.strftime("%Y%m%d-%H:%M:%S,")
                    for j, n in enumerate(range(NUM_DEVICES)):
                        if n  in switches:
                            data += "%.5f" % self.Y[n][-1]# switches[n].current_power
                            #data += "%.5f" % switches[n].current_power
                        else:
                            data += "-1"
                        
                        if j == NUM_DEVICES-1:
                            data += "\n"
                        else:
                            data += ","
                    f.write(data)


osc = Oscilloscope()

