#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      bluemaemo.py
#
#      Copyright 2008 - 2009 	Valerio Valerio <vdv100@gmail.com>
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

import os
import sys
import time
import e_dbus
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.x
import ecore.evas
from dbus import SystemBus, Interface
from dbus.exceptions import DBusException
from optparse import OptionParser

from bluemaemo_server import *
from bluemaemo_key_mapper import *
from bluemaemo_conf import *
from bluemaemo_edje_group import *
from bluemaemo_about import *
from bluemaemo_disconnect import *
from bluemaemo_connection_status import *
from bluemaemo_bluetooth_off import *
from bluemaemo_settings import *
from bluemaemo_menu import *
from bluemaemo_mouse import *
from bluemaemo_keyboard import *
from bluemaemo_presentation import *
from bluemaemo_multimedia import *
from bluemaemo_games import *

#from bluemaemo.bluemaemo_server import *
#from bluemaemo.bluemaemo_key_mapper import *
#from bluemaemo.bluemaemo_conf import *

WIDTH = 800
HEIGHT = 480

TITLE = "bluemaemo"
WM_NAME = "bluemaemo"
WM_CLASS = "bluemaemo"


edjepaths = "bluemaemo.edj themes/bluemaemo.edj /usr/share/bluemaemo/themes/bluemaemo.edj".split()

for i in edjepaths:
    if os.path.exists( i ):
       global edjepath
       edjepath = i
       break
else:
    raise Exception( "bluemaemo.edj not found. looked in %s" % edjepaths )


#----------------------------------------------------------------------------#
def translate_key(self,keyname, keystring):
#----------------------------------------------------------------------------#
	if keyname == "Tab":
		return "Tab"
	elif keyname == "Return":
		return "Return"
	elif keyname == "Escape":
		return "Escape"
	elif keyname == "BackSpace":
		return "BackSpace"
	elif keyname == "Insert":
		return "Insert"
	elif keyname == "Home":
		return "Home"
	elif keyname == "Prior":
		return "Prior"
	elif keyname == "Delete":
		return "Delete"
	elif keyname == "End":
		return "End"
	elif keyname == "Next":
		return "Next"
	elif keyname == "Right":
		return "Right"
	elif keyname == "Left":
		return "Left"
	elif keyname == "Down":
		return "Down"
	elif keyname == "Up":
		return "Up"
	elif keyname == "KP_Enter":
		return "Return"
	elif keyname == "space":
		return "space"
	elif keyname == "F1":
		return "F1"
	elif keyname == "F2":
		return "F2"
	elif keyname == "F3":
		return "F3"
	elif keyname == "F4":
		return "F4"
	elif keyname == "F5":
		return "F5"
	elif keyname == "F6":
		return "F6"
	elif keyname == "F7":
		return "F7"
	elif keyname == "F8":
		return "F8"
	elif keyname == "F9":
		return "F9"
	elif keyname == "F10":
		return "F10"
	elif keyname == "F11":
		return "F11"
	elif keyname == "F12":
		return "F12"

	else:
		return keystring

#----------------------------------------------------------------------------#
class main(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "main")

	self.part_text_set("label_waiting", "Waiting for connection ... ")
	#ecore.timer_add(1.0,self.main.transition_to,"menu")

	ecore.timer_add(1.0,self.check_connection)
    

    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

	if key == "F6":

		if self.main.bluemaemo_conf.fullscreen == "Yes":
			
			self.main.bluemaemo_conf.fullscreen = "No"
			self.main.window.fullscreen = False

		elif self.main.bluemaemo_conf.fullscreen == "No":
			
			self.main.bluemaemo_conf.fullscreen = "Yes"
			self.main.window.fullscreen = True

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "quit":
		
		self.main.connection.terminate_connection()
		self.main.on_exit()
		ecore.main_loop_quit()
		

    def check_connection(self):

		if self.main.connection_processed == True:

			if self.main.connection.connect == False:
				ecore.timer_add(1.0,self.check_connection)
				
			else:
			
				ecore.timer_add(1.0,self.check_client)
		else:
			ecore.timer_add(1.0,self.check_connection)

    def check_client(self):
		
		if self.main.connection.client_name == None:
			
			ecore.timer_add(1.0,self.check_client)
			
		else:
			
			self.part_text_set("label_waiting", "")
			self.part_text_set("label_connect_to", "Connected to: ")
			self.part_text_set("label_client", self.main.connection.client_name)
			ecore.idle_enterer_add( self.main.check_connection_status)
			ecore.timer_add(3.0,self.main.transition_to,"menu")
	
#----------------------------------------------------------------------------#
class conf_keys(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "conf_keys")
	self.shift = False
	self.ctrl = False
	self.alt = False
	self.press_f = False
	self.press_fpp = False
	self.press_w = False
	self.press_wi = False
	self.press_win = False
	self.hit = False
	self.fn = False
	self.shift = False
	self.special_key = False

	self.obj = {
            "alpha": self.part_swallow_get("alpha"),
            "special-1": self.part_swallow_get("special-1"),
            "special-2": self.part_swallow_get("special-2"),
            }
        self.pressed_keys = {}
        self.is_shift_down = False
        self.is_mouse_down = False
    
    def onShow( self ):
        self.focus = True
        
    def onHide( self ):
        self.focus = False

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		prev = self.main.current_conf_screen + "_conf"
		prev_source = self.main.current_source + "_icon"
		local_key = str(self.main.current_source)
		
		if self.hit == False:
			
			self.hit = False
			self.main.transition_to(prev)
		
		elif len(self.main.key_text) > 3:
			

			if self.main.key_text == "space":
				text_value = self.main.key_mapper.mapper["space_t"]
				self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	

			#shift translation	
			elif self.main.key_text[0] == "s":
				text_value = self.main.key_mapper.mapper[self.main.key_text]
				self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	
			elif self.main.key_text[0] == "f" and self.main.key_text[1] == "n":
				val = str(self.main.key_text) + "+u"
				text_value = self.main.key_mapper.mapper[val]
				self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	

			elif self.main.key_text[0] == "s" and self.main.key_text[1] == "p":
				val = str(self.main.key_text)
				text_value = self.main.key_mapper.mapper[val]
				self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(local_key,self.main.key_text)					
				
			else:
				self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	
		elif self.main.key_text == "-":
			self.main.groups[prev].part_text_set(prev_source,"minus")
			self.main.save_local_conf(local_key,"minus")
		else:
			self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
			self.main.save_local_conf(local_key,self.main.key_text)
		self.hit = False
		self.main.transition_to(prev)

    #hardware keyboard
    @evas.decorators.key_down_callback
    def on_key_down( self, event ):
        key = event.string
	key_key = event.key
	key_value = event.keyname
	print(key_value)
	self.hit = True

	if key_value == "Shift_L":
		self.shift = True
			
	elif key_value == "Control_L":
		self.ctrl = True

	elif key_value == "Control_R":
		self.ctrl = True
			
	elif key_value == "Alt_L":
		self.alt = True

	elif key_key == "ISO_Level3_Shift":
		self.fn = True

	else:

		if self.shift == True:
			
			self.part_text_set("value","  "+ str(key)+ "  ")
			self.shift = False
			self.main.key_text = "shift+"+str(key_value)
		
		elif self.alt == True and self.ctrl == True:

			self.part_text_set("value","ctrl+alt+" + str(key_key))
			self.ctrl = False
			self.alt = False
			self.main.key_text = "ctrl+alt+" + str(key_key)

		elif self.ctrl == True:

			self.part_text_set("value","ctrl+" + str(key_key))
			self.ctrl = False
			self.main.key_text = "ctrl+" + str(key_key)
	
		elif self.fn == True:
			if key_key == "EuroSign":
				self.part_text_set("value","  "+"€"+ " ")
				self.fn = False
				self.main.key_text = "fn_k+" + str(key_value)	
			elif key_key == "sterling":
				self.part_text_set("value","  "+"£"+ " ")
				self.fn = False
				self.main.key_text = "fn_k+" + str(key_value)	
			elif self.press_f == True:
				self.main.key_text = translate_key(self,key_value,key)

				if self.main.key_text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
					if self.main.key_text == "1":
						self.press_fpp = True
					self.main.key_text = "f" + self.main.key_text
					self.part_text_set("value","  " + self.main.key_text+" ")
					self.press_f = False
					self.fn = False
				else:
					
						self.press_f = False
						self.alt = False
						self.part_text_set("value","  " +self.main.key_text+ " ")
						self.fn = False

			elif self.press_fpp == True:
				self.main.key_text = translate_key(self,key_value,key)
				if self.main.key_text in ("0", "1", "2"):
					self.main.key_text = "f1" + self.main.key_text
					self.part_text_set("value","  " + self.main.key_text+" ")
					self.press_fpp = False
					self.fn = False
						
				else:
					
					self.press_fpp = False
					self.part_text_set("value","  " + self.main.key_text+" ")
					self.fn = False
				

			else:
				self.part_text_set("value","  "+ str(key)+ " ")
				self.fn = False
				self.main.key_text = "fn_k+" + str(key_value)		

		elif self.alt == True:

			if key_value == "Tab":

				self.part_text_set("value","alt+" + str(key_value))	
				self.alt = False
				self.main.key_text = "alt+" + str(key_value)	
			else:
				

				self.main.key_text = translate_key(self,key_value,key)
				if self.main.key_text == "f":
					self.press_f = True
					self.part_text_set("value","alt+" + self.main.key_text)
				
				elif self.press_f == True:
					if self.main.key_text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
						if self.main.key_text == "1":
							self.press_fpp = True
						self.main.key_text = "alt+f" + self.main.key_text
						self.part_text_set("value",self.main.key_text)
						self.press_f = False
					
					else:
					
						self.press_f = False
						self.alt = False
						self.part_text_set("value","  " +self.main.key_text+ " ")
					
					
				elif self.press_fpp == True:
					if self.main.key_text in ("0", "1", "2"):
						self.main.key_text = "alt+f1" + self.main.key_text
						self.part_text_set("value",self.main.key_text)
						self.press_fpp = False
						self.alt = False
						
					else:
					
						self.press_fpp = False
						self.alt = False
						self.part_text_set("value","  " + self.main.key_text+" ")
					
				
				else:
					self.part_text_set("value","alt+" + str(key))	
					self.alt = False
					self.main.key_text = "alt+" + str(key)			

		else:
			self.main.key_text = translate_key(self,key_value,key)

			if self.main.key_text =="w":
				self.press_w = True
				self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_w == True:

				if self.main.key_text == "i":
					self.press_wi = True
					self.press_w = False
					self.part_text_set("value","w" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_wi == True:	

				if self.main.key_text == "n":
					self.press_win = True
					self.press_wi = False
					self.part_text_set("value","wi" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_win == True:

				self.press_win = False	
				self.part_text_set("value","win+" + self.main.key_text+" ")
				self.main.key_text = "win+" + self.main.key_text


			elif self.main.key_text == "f":
				self.press_f = True
				self.part_text_set("value","  " + self.main.key_text+" ")
				
			#elif self.press_f == True:
			#	if self.main.key_text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
			#		if self.main.key_text == "1":
			#			self.press_fpp = True
			#		self.main.key_text = "f" + self.main.key_text
			#		self.part_text_set("value","  " + self.main.key_text+" ")
			#		self.press_f = False
			#		
			#	else:
			#		
			#		self.press_f = False
			#		self.part_text_set("value","  " + self.main.key_text+" ")
					
					
			#elif self.press_fpp == True:
			#	if self.main.key_text in ("0", "1", "2"):
			#		self.main.key_text = "f1" + self.main.key_text
			#		self.part_text_set("value","  " + self.main.key_text+" ")
			#		self.press_fpp = False
			#			
			#	else:
			#		
			#		self.press_fpp = False
			#		self.part_text_set("value","  " + self.main.key_text+" ")

			
			else:
				self.part_text_set("value","  " + self.main.key_text+" ")
				
	
    @edje.decorators.signal_callback("mouse_over_key", "*")
    def on_edje_signal_mouse_over_key(self, emission, source):
        if not self.is_mouse_down:
            return
        if ':' not in source:
            return
        part, subpart = source.split(':', 1)
        o = self.obj[part]

        if subpart in self.pressed_keys:
            return

        for k in self.pressed_keys.values():
            o.signal_emit("release_key", k)
        self.pressed_keys.clear()
        self.pressed_keys[subpart] = subpart
        o.signal_emit("press_key", subpart)

    @edje.decorators.signal_callback("mouse_out_key", "*")
    def on_edje_signal_mouse_out_key(self, emission, source):
        if not self.is_mouse_down:
            return
        if ':' not in source:
            return
        part, subpart = source.split(':', 1)
        o = self.obj[part]

        if subpart in self.pressed_keys:
            del self.pressed_keys[subpart]
            o.signal_emit("release_key", subpart)

    @evas.decorators.mouse_down_callback
    def on_mouse_down(self, event):
        if event.button != 1:
            return
        self.is_mouse_down = True

    @evas.decorators.mouse_up_callback
    def on_mouse_up(self, event):
        if event.button != 1:
            return
        self.is_mouse_down = False

    def press_shift(self):
    	
        self.obj["alpha"].signal_emit("press_shift", "")
        self.is_shift_down = True

    def release_shift(self):
        self.obj["alpha"].signal_emit("release_shift", "")
        self.is_shift_down = False

    def toggle_shift(self):
        if self.is_shift_down:
            self.release_shift()
        else:
            self.press_shift()

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_edje_signal_mouse_down_key(self, emission, source):
        if ':' not in source:
            return
        part, subpart = source.split(':', 1)
        o = self.obj[part]
        self.is_mouse_down = True

        if subpart in self.pressed_keys:
            return

        for k in self.pressed_keys.values():
            o.signal_emit("release_key", k)
        self.pressed_keys.clear()
        self.pressed_keys[subpart] = subpart
        o.signal_emit("press_key", subpart)

    @edje.decorators.signal_callback("mouse,down,1,*", "*")
    def on_edje_signal_mouse_down_multiple_key(self, emission, source):
        self.on_edje_signal_mouse_down_key(self, emission, source)
        
    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_mouse_up_key(self, emission, source):
        if ':' not in source:
            return
        part, subpart = source.split(':', 1)
        o = self.obj[part]
        self.is_mouse_down = False
        if subpart in self.pressed_keys:
            del self.pressed_keys[subpart]
            o.signal_emit("release_key", subpart)
            o.signal_emit("activated_key", subpart)


    @edje.decorators.signal_callback("key_down", "*")
    def on_edje_signal_key_down(self, emission, source):
	self.hit = True
        if ':' in source:
            key = source.split(":", 1)[1]
	    screen = source.split(":", 1)[0]
        else:
            key = source
        if key == "shift":
            self.toggle_shift()
	    key_s = "NULL"
	elif screen == "alpha":
	    
	    if key == "space":
	    	key_s = "space"
	    elif key == "enter":
	    	key_s = "Return"	    
	    elif key == "backspace":
	    	key_s = "BackSpace"
	    elif key in (".?123", "ABC", "#+=", ".?12"):
		key_s = "NULL"
	    else:
		key_s = key.lower()
	elif key in (".?123", "ABC", "#+=", ".?12"):
		key_s = "NULL"
	elif key in (":","(",")","$","&","@","?","!","\"","*","+","_","#","%","~","|","<",">","{","}","^"):
		self.special_key = True
		key_s = "sp+" + key
		
        elif key == "space":
	    key_s = "space"
	elif key == "enter":
	    key_s = "Return"
	elif key == "backspace":
	    key_s = "BackSpace"
        else:
	    key_s = key

	if key_s == "NULL":
		pass
	else:
		if self.is_shift_down:

			self.part_text_set("value","  "+ str(key_s.upper())+ "  ")
			self.main.key_text = "shift+"+str(key_s)
			self.release_shift()
		else:
			if self.special_key == True:
				self.part_text_set("value","  "+ str(key)+ "  ")
				self.main.key_text = str(key_s)
				self.special_key = False
			else:

				self.part_text_set("value","  "+ str(key_s)+ "  ")
				self.main.key_text = str(key_s)
#----------------------------------------------------------------------------#
class GUI(object):
#----------------------------------------------------------------------------#
    def __init__( self, options, args ):
	
	self.bluemaemo_conf = bluemaemo_conf()
	self.load_local_confs()
	if self.fullscreen == "Yes":
		opt_fullscreen = True
	else:
		opt_fullscreen = False 
        edje.frametime_set(1.0 / options.fps)

        self.evas_canvas = EvasCanvas(
            fullscreen = opt_fullscreen,
            engine = options.engine,
            size = options.geometry
        )
	self.evas_canvas.main = self
	self.canvas = self.evas_canvas.evas_obj.evas
	self.window = self.evas_canvas.evas_obj
	self.connection_processed = False
	self.restore_conditions = False
	self.try_framework = 0
	self.key_text = ""
	self.bluetooth_obj = True
	self.edje_obj = ""
		
	self.key_mapper = key_mapper()
	

        self.groups = {}

        self.groups["swallow"] = edje_group(self, "swallow")
        self.evas_canvas.evas_obj.data["swallow"] = self.groups["swallow"]

        for page in ("main","mouse_ui", "menu", "disconnect", "connection_status", "keyboard_ui","about","bluetooth_off_alert","settings","games", "games_conf","multimedia","multimedia_conf","presentation","presentation_conf","conf_keys"):
		ctor = globals().get( page, None )
		if ctor:
			self.groups[page] = ctor( self )
			self.evas_canvas.evas_obj.data[page] = self.groups[page]


        self.groups["swallow"].show()

        self.groups["swallow"].part_swallow("area1", self.groups["main"])
        self.current_group = self.groups["main"]
        self.previous_group = self.groups["menu"]
        self.in_transition = False
	self.current_conf_screen = None
	self.current_source = None
	self.initialize_bluemaemo_server()

    def check_connection_status(self):
	if self.connection.connect == False:
		self.transition_to("disconnect")
		print "->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DISC"

	else:
		ecore.timer_add( 10.0, self.check_connection_status)
	
	
    def check_bt_status(self):
		
	file = open("/sys/bus/platform/devices/neo1973-pm-bt.0/power_on")
	status = file.readline()
	if status.find('0') > -1:
		print "off"
		return "off"
	else:
		print "on"
		return "on"
		
	file.close()

    def power_on_bt(self):
	
	self.restore_conditions = True
	os.system("echo 1 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/power_on")
	os.system("echo 0 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/reset")
	
    def dbus_objectInit( self ):
        
	
	self.bluetooth_obj = True
	return False
        
    def on_exit(self):
	
	if self.restore_conditions == True:

		os.system("echo 1 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/reset")
	
        

    def initialize_bluemaemo_server(self):

	if self.bluetooth_obj == True:

		self.connection = Connect()
		ecore.timer_add(1.0,self.connection.start_connection)
		self.connection_processed = True
        else:
		ecore.timer_add(1.0,self.initialize_bluemaemo_server)
	
    def load_local_confs(self):
	#settings
	self.fullscreen = self.bluemaemo_conf.fullscreen
	self.scroll = int(self.bluemaemo_conf.scroll)
	#presentation
	self.previous_key = self.bluemaemo_conf.previous_key
	self.next_key = self.bluemaemo_conf.next_key
	self.fullscreen_key = self.bluemaemo_conf.fullscreen_key
	self.no_fullscreen_key = self.bluemaemo_conf.no_fullscreen_key
	#multimedia profile
	self.play_key = self.bluemaemo_conf.play_key
	self.pause_key = self.bluemaemo_conf.pause_key
	self.stop_key = self.bluemaemo_conf.stop_key
	self.forward_key = self.bluemaemo_conf.forward_key
	self.backward_key = self.bluemaemo_conf.backward_key
	self.volume_m_key = self.bluemaemo_conf.volume_m_key
	self.volume_p_key = self.bluemaemo_conf.volume_p_key
	self.fullscreen_key_m = self.bluemaemo_conf.fullscreen_key_m
	self.no_fullscreen_key_m = self.bluemaemo_conf.no_fullscreen_key_m
	#games profile
	self.up_key = self.bluemaemo_conf.up_key
	self.down_key = self.bluemaemo_conf.down_key
	self.right_key = self.bluemaemo_conf.right_key
	self.left_key = self.bluemaemo_conf.left_key
	self.a_key = self.bluemaemo_conf.a_key
	self.b_key = self.bluemaemo_conf.b_key
	self.c_key = self.bluemaemo_conf.c_key
	self.d_key = self.bluemaemo_conf.d_key
	

    def save_local_conf(self, button_name, key):
	
	if button_name == "previous_key":

		self.previous_key = key
		self.bluemaemo_conf.set_option("presentation","previous_key",key)

	elif button_name == "next_key":

		self.next_key = key
		self.bluemaemo_conf.set_option("presentation","next_key",key)

	elif button_name == "fullscreen_key":

		self.fullscreen_key = key
		self.bluemaemo_conf.set_option("presentation","fullscreen_key",key)

	elif button_name == "no_fullscreen_key":

		self.no_fullscreen_key = key
		self.bluemaemo_conf.set_option("presentation","no_fullscreen_key",key)

	elif button_name == "play_key":

		self.play_key = key
		self.bluemaemo_conf.set_option("multimedia","play_key",key)

	elif button_name == "pause_key":

		self.pause_key = key
		self.bluemaemo_conf.set_option("multimedia","pause_key",key)

	elif button_name == "stop_key":

		self.stop_key = key
		self.bluemaemo_conf.set_option("multimedia","stop_key",key)

	elif button_name == "forward_key":

		self.forward_key = key
		self.bluemaemo_conf.set_option("multimedia","forward_key",key)

	elif button_name == "backward_key":

		self.backward_key = key
		self.bluemaemo_conf.set_option("multimedia","backward_key",key)

	elif button_name == "volume_p_key":

		self.volume_p_key = key
		self.bluemaemo_conf.set_option("multimedia","volume_p_key",key)

	elif button_name == "volume_m_key":

		self.volume_m_key = key
		self.bluemaemo_conf.set_option("multimedia","volume_m_key",key)
	
	
	elif button_name == "fullscreen_key_m":

		self.fullscreen_key_m = key
		self.bluemaemo_conf.set_option("multimedia","fullscreen_key_m",key)

	elif button_name == "no_fullscreen_key_m":

		self.no_fullscreen_key_m = key
		self.bluemaemo_conf.set_option("multimedia","no_fullscreen_key_m",key)

	elif button_name == "up_key":

		self.up_key = key
		self.bluemaemo_conf.set_option("games","up_key",key)

	elif button_name == "down_key":

		self.down_key = key
		self.bluemaemo_conf.set_option("games","down_key",key)

	elif button_name == "right_key":

		self.right_key = key
		self.bluemaemo_conf.set_option("games","right_key",key)

	elif button_name == "left_key":

		self.left_key = key
		self.bluemaemo_conf.set_option("games","left_key",key)
	
	elif button_name == "a_key":

		self.a_key = key
		self.bluemaemo_conf.set_option("games","a_key",key)

	elif button_name == "b_key":

		self.b_key = key
		self.bluemaemo_conf.set_option("games","b_key",key)
	
	elif button_name == "c_key":

		self.c_key = key
		self.bluemaemo_conf.set_option("games","c_key",key)

	elif button_name == "d_key":

		self.d_key = key
		self.bluemaemo_conf.set_option("games","d_key",key)

    def run( self ):
        ecore.main_loop_begin()
	
    def shutdown( self ):
        ecore.main_loop_quit()

    def transition_to(self, target):
        if self.current_group == self.groups[target]:
            return
        print "transition to", target
        self.in_transition = True

        self.previous_group = self.current_group

        self.current_group = self.groups[target]
        self.current_group.onShow()
        self.current_group.signal_emit("visible", "")
        self.groups["swallow"].part_swallow("area1", self.current_group)
        self.previous_group.signal_emit("fadeout", "")

    def transition_finished(self):
        print "finished"
        self.previous_group.onHide()
        self.previous_group.hide()
        self.groups["swallow"].part_swallow("area1", self.current_group)
        self.in_transition = False
            
#----------------------------------------------------------------------------#
class EvasCanvas(object):
#----------------------------------------------------------------------------#
    def __init__(self, fullscreen, engine, size):
        if engine == "x11":
            f = ecore.evas.SoftwareX11
        elif engine == "x11-16":
            if ecore.evas.engine_type_supported_get("software_x11_16"):
                f = ecore.evas.SoftwareX11_16
            else:
                print "warning: x11-16 is not supported, fallback to x11"
                f = ecore.evas.SoftwareX11

        self.evas_obj = f(w=size[0], h=size[1])
        self.evas_obj.callback_delete_request = self.on_delete_request
        self.evas_obj.callback_resize = self.on_resize

        self.evas_obj.title = TITLE
        self.evas_obj.name_class = (WM_NAME, WM_CLASS)
        self.evas_obj.fullscreen = fullscreen
        self.evas_obj.size = size
        self.evas_obj.evas.image_cache_set( 6*1024*1024 )
        self.evas_obj.evas.font_cache_set( 2*1024*1024 )
        self.evas_obj.show()

    def on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        evas_obj.data["swallow"].size = size

    def on_delete_request(self, evas_obj):

	self.main.connection.terminate_connection()
	self.main.on_exit()
	ecore.main_loop_quit()
#----------------------------------------------------------------------------#
class MyOptionParser(OptionParser):
#----------------------------------------------------------------------------#
    def __init__(self):
        OptionParser.__init__(self)
        self.set_defaults(fullscreen = False)
        self.add_option("-e",
                      "--engine",
                      type="choice",
                      choices=("x11", "x11-16"),
                      default="x11-16",
                      help=("which display engine to use (x11, x11-16), "
                            "default=%default"))
        self.add_option("--fullscreen",
                      action="store_true",
                      dest="fullscreen",
                      help="launch in fullscreen")
        self.add_option("--no-fullscreen",
                      action="store_false",
                      dest="fullscreen",
                      help="launch in a window")
        self.add_option("-g",
                      "--geometry",
                      type="string",
                      metavar="WxH",
                      action="callback",
                      callback=self.parse_geometry,
                      default=(WIDTH, HEIGHT),
                      help="use given window geometry")
        self.add_option("-f",
                      "--fps",
                      type="int",
                      default=20,
                      help="frames per second to use, default=%default")
        self.add_option("-s",
                      "--start",
                      type="string",
                      default=None,
                      help="start with the given page")

    def parse_geometry(option, opt, value, parser):
        try:
            w, h = value.split("x")
            w = int(w)
            h = int(h)
        except Exception, e:
            raise optparse.OptionValueError("Invalid format for %s" % option)
        parser.values.geometry = (w, h)


if __name__ == "__main__":

    options, args = MyOptionParser().parse_args()
    dbus_object = None
    gui = GUI( options, args )
    try:
        gui.run()
    except KeyboardInterrupt:
        gui.shutdown()
        del gui




