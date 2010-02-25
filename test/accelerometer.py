#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      accelerometer.py
#
#      Copyright 2009 	Valerio Valerio <vdv100@gmail.com>
#						
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# -*- coding: utf-8 -*-
#inspired in..TBD

import ecore
import ecore.x
import os.path
from bluemaemo_edje_group import *


A_PRESS_DOWN = 5
A_PRESS_UP = 6

class Read_accelerometer:
    def __init__(self,profile):
        #setup accelerometer
        self.profile = profile
        self.accel = Accelerometer()
	self.x = self.y = self.z = 0
	self.x_init = self.y_init = self.z_init = 0
	
        self.last_direction = None
        self.l_left = 50
        self.l_right = 50
        self.l_up = 50
        self.l_down = 50
        self.oax = 0;
        self.oay = 0;
        self.oaz = 0;
        self.press = False;

	self.first_time = True
	self.send_event = False
	self.pass_event = False
	self.pass_event2 = False
	self.accel_on = False

    def read_dir(self, main):

	    self.main  = main
	    if self.send_event:
		if self.profile.key_pressed:
			self.main.connection.release_multiple_keyboard_event(self.profile.current_key)
		else:
			self.main.connection.release_keyboard_event()
		self.send_event = False
		if self.profile.key_pressed:
			self.main.connection.send_keyboard_event(self.profile.current_modif,self.profile.current_key)
		
		print "release"
	    else:

		if self.pass_event:
			self.pass_event = False
		else:

			self.pass_event2 = False
            direction=None
            event = []
            (a_x,a_y,a_z) = self.accel.position()
            roll = self.oax + (a_x-self.oax)*0.3
            pitch = self.oay + (a_y-self.oay)*0.3
            self.oax = a_x;
            self.oay = a_y;
            if abs(roll) > abs(pitch):
                if roll > self.l_left:

                    	key = self.main.left_key
			modif, val = key_dec(self,key)
			if self.profile.key_pressed:
				self.main.connection.send_multiple_keyboard_event(modif,val,self.profile.current_key)
			else:

				self.main.connection.send_keyboard_event(modif,val)
			self.send_event = True

                if roll < -self.l_right:
                   	key = self.main.right_key
			modif, val = key_dec(self,key)

			if self.profile.key_pressed:
				self.main.connection.send_multiple_keyboard_event(modif,val,self.profile.current_key)
			else:

				self.main.connection.send_keyboard_event(modif,val)

			self.send_event = True
            else:
                if pitch > self.l_up:
                   pass
                if pitch < -self.l_down:
		   pass
            if abs(a_x) > 100 or abs(a_y) > 100:
                press = True
            else:
                press = False
            if self.press == True and press == False:
                event.append(A_PRESS_UP)
            elif press == True:
                event.append(A_PRESS_DOWN)
            self.press = press

            if direction != None:
                event.append(direction)

            if self.accel_on:
		ecore.timer_add(0.0,self.read_dir, main)

    def air_mouse(self, main):

	    self.main  = main
	    direction=None
            (a_x,a_y,a_z) = self.accel.position()
            roll = self.oax + (a_x-self.oax)*0.3
            pitch = self.oay + (a_y-self.oay)*0.3
            self.oax = a_x;
            self.oay = a_y;
            if abs(roll) > abs(pitch):
                if roll > self.l_left:

			self.main.connection.send_mouse_event(00,-2,0,00)

                if roll < -self.l_right:
                   	
			self.main.connection.send_mouse_event(00,2,0,00)

            else:
                if pitch > self.l_up:
                    self.main.connection.send_mouse_event(00,0,-2,00)
                if pitch < -self.l_down:
                    self.main.connection.send_mouse_event(00,0,2,00)	
		
	    if self.profile.press:
		ecore.timer_add(0.001,self.air_mouse, self.main)


class Accelerometer:

    def __init__(self):
	self.accelerometer_path = '/sys/class/i2c-adapter/i2c-3/3-001d/coord'
	#os.path.isfile(ACCELEROMETER_PATH) can a app lock the accel ?
    
    def position(self):
        f = open(self.accelerometer_path, 'r')
        coords = [int(w) for w in f.readline().split()]
        f.close()
        return coords


