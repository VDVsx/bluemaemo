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
import elementary

from dbus import SystemBus, Interface
from dbus.exceptions import DBusException
from optparse import OptionParser

from bluemaemo_server import *
from bluemaemo_main import *
from bluemaemo_key_mapper import *
from bluemaemo_conf import *
from bluemaemo_edje_group import *
from bluemaemo_about import *
from bluemaemo_disconnect import *
from bluemaemo_connection_status import *
from bluemaemo_settings import *
from bluemaemo_menu import *
from bluemaemo_mouse import *
from bluemaemo_keyboard import *
from bluemaemo_presentation import *
from bluemaemo_multimedia import *
from bluemaemo_games import *
from bluemaemo_recon_list import *
from bluemaemo_confirm_conn import *
from bluemaemo_unable_conn import *
from bluemaemo_process_conn import *
from bluemaemo_hw_kb import *
from bluemaemo_ps3_control import *

WIDTH = 800
HEIGHT = 480

TITLE = "bluemaemo"
WM_NAME = "bluemaemo"
WM_CLASS = "bluemaemo"

elementary.init()

elementary_paths = "/home/valerio/bluemaemo/trunk/test/elementary_theme.edj  /root/test/elementary_theme.edj".split()

for i in elementary_paths:
    if os.path.exists( i ):
       elementary.c_elementary.theme_overlay_add(i)
       break
else:
    raise Exception( "elementary_theme.edj not found. looked in %s" % elementary_paths )

elementary.c_elementary.finger_size_set(62)

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
class wait_conn(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "wait_conn")
	self.part_text_set("menu_title", "Wait for connection" )
	self.part_text_set("label_waiting", "Waiting for connection ... ")
	self.main = main
	#ecore.timer_add(7.0,self.main.transition_to,"menu")
	#ecore.timer_add(1.0,self.main.transition_to,"rec_list")

	#ecore.timer_add(1.0,self.check_connection)
    

    def onShow( self ):
	self.focus = True
	self.main.initialize_bluemaemo_server()
	ecore.timer_add(1.0,self.check_connection)
    

    def onHide( self ):
	self.focus = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.connection.terminate_connection()
		self.main.transition_to("main")

	elif source == "task_switcher":

		self.main.task_switcher()

    def check_connection(self):

		if self.main.connection_processed:

			if not self.main.connection.connect:
				ecore.timer_add(1.0,self.check_connection)
				
			else:
			
				ecore.timer_add(1.0,self.check_client)
		else:
			ecore.timer_add(1.0,self.check_connection)

    def check_client(self):
		
		if self.main.connection.client_name == None:
			
			ecore.timer_add(1.0,self.check_client)
			
		else:

			self.main.current_adapter_name = self.main.connection.client_name
			self.main.current_adapter_addr = self.main.connection.client_addr
			self.main.check_first_time()
			self.main.connected = True
			self.main.transition_to("connection_status")
	
#----------------------------------------------------------------------------#
class conf_keys(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "conf_keys")
	self.part_text_set( "menu_title", "Multimedia settings" )
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
	self.is_ctrl_down = False
	self.is_alt_down = False
        self.is_mouse_down = False
    
    def onShow( self ):
        self.focus = True
        
    def onHide( self ):
        self.focus = False

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):

	if source == "task_switcher":

		self.main.task_switcher()

	elif source == "back":
		
		prev = self.main.current_conf_screen + "_conf"
		#prev_source = self.main.current_source + "_icon"
		#local_key = self.main.current_source
		
		if not self.hit:
			
			self.hit = False
			self.main.transition_to(prev)
		
		elif len(self.main.key_text) > 3:
			
			print self.main.key_text
			if self.main.key_text == "space":
				text_value = self.main.key_mapper.mapper["space_t"]
				self.main.current_source.label_set(text_value)
				#self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)	

			#shift translation	
			elif self.main.key_text[0] == "s":
				text_value = self.main.key_mapper.mapper[self.main.key_text]
				self.main.current_source.label_set(text_value)
				self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)	
			elif self.main.key_text[0] == "f" and self.main.key_text[1] == "n":
				val = str(self.main.key_text) + "+u"
				text_value = self.main.key_mapper.mapper[val]
				self.main.current_source.label_set(text_value)
				self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)	

			elif self.main.key_text[0] == "s" and self.main.key_text[1] == "p":
				val = str(self.main.key_text)
				text_value = self.main.key_mapper.mapper[val]
				self.main.current_source.label_set(text_value)
				self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)	
				
			else:
				self.main.current_source.label_set(self.main.key_text)
				#self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
				self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)	
		elif self.main.key_text == "-":
			self.main.current_source.label_set("minus")
			#self.main.groups[prev].part_text_set(prev_source,"minus")
			self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,"minus")
		else:
			self.main.current_source.label_set(self.main.key_text)
			#self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
			self.main.save_local_conf(self.main.current_label,self.main.current_conf_screen,self.main.key_text)
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

		if self.shift:
			
			self.part_text_set("value","  "+ str(key)+ "  ")
			self.shift = False
			self.main.key_text = "shift+"+str(key_value)
		
		elif self.alt and self.ctrl:

			self.part_text_set("value","ctrl+alt+" + str(key_key))
			self.ctrl = False
			self.alt = False
			self.main.key_text = "ctrl+alt+" + str(key_key)

		elif self.ctrl:

			self.part_text_set("value","ctrl+" + str(key_key))
			self.ctrl = False
			self.main.key_text = "ctrl+" + str(key_key)
	
		elif self.fn:
			if key_key == "EuroSign":
				self.part_text_set("value","  "+"€"+ " ")
				self.fn = False
				self.main.key_text = "fn_k+" + str(key_value)	
			elif key_key == "sterling":
				self.part_text_set("value","  "+"£"+ " ")
				self.fn = False
				self.main.key_text = "fn_k+" + str(key_value)	
			elif self.press_f:
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

			elif self.press_fpp:
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

		elif self.alt:

			if key_value == "Tab":

				self.part_text_set("value","alt+" + str(key_value))	
				self.alt = False
				self.main.key_text = "alt+" + str(key_value)	
			else:
				

				self.main.key_text = translate_key(self,key_value,key)
				if self.main.key_text == "f":
					self.press_f = True
					self.part_text_set("value","alt+" + self.main.key_text)
				
				elif self.press_f:
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
					
					
				elif self.press_fpp:
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

			elif self.press_w:

				if self.main.key_text == "i":
					self.press_wi = True
					self.press_w = False
					self.part_text_set("value","w" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_wi:	

				if self.main.key_text == "n":
					self.press_win = True
					self.press_wi = False
					self.part_text_set("value","wi" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_win:

				self.press_win = False	
				self.part_text_set("value","win+" + self.main.key_text+" ")
				self.main.key_text = "win+" + self.main.key_text


			elif self.main.key_text == "f":
				self.press_f = True
				self.part_text_set("value","  " + self.main.key_text+" ")
			
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

    #shift
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

    #ctrl
    def press_ctrl(self):
    	
        self.obj["alpha"].signal_emit("press_ctrl", "")
        self.is_ctrl_down = True

    def release_ctrl(self):
        self.obj["alpha"].signal_emit("release_ctrl", "")
        self.is_ctrl_down = False

    def toggle_ctrl(self):
        if self.is_ctrl_down:
            self.release_ctrl()
        else:
            self.press_ctrl()
    #alt
    def press_alt(self):
    	
        self.obj["alpha"].signal_emit("press_alt", "")
        self.is_alt_down = True

    def release_alt(self):
        self.obj["alpha"].signal_emit("release_alt", "")
        self.is_alt_down = False

    def toggle_alt(self):
        if self.is_alt_down:
            self.release_alt()
        else:
            self.press_alt()

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
	    elif key == "ctrl":
		self.toggle_ctrl()
	    	key_s = "NULL"
	    elif key == "alt":
		self.toggle_alt()
	    	key_s = "NULL"
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

		elif self.is_ctrl_down and self.is_alt_down:
			self.part_text_set("value","ctrl+alt+" + str(key_s))
			self.main.key_text = "ctrl+alt+"+str(key_s)
			self.release_ctrl()
			self.release_alt()
				
		elif self.is_ctrl_down:
			self.part_text_set("value","ctrl+"+ str(key_s)+ "  ")
			self.main.key_text = "ctrl+"+str(key_s)
			self.release_ctrl()
				
		elif self.is_alt_down:
			self.part_text_set("value","alt+"+ str(key_s)+ "  ")
			self.main.key_text = "alt+"+str(key_s)
			self.release_alt()
		
		else:
			if self.special_key:
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
	#opt_fullscreen = False
	opt_fullscreen = True
        edje.frametime_set(1.0 / options.fps)
        self.evas_canvas = EvasCanvas(
            fullscreen = opt_fullscreen,
            engine = options.engine,
            size = options.geometry
        )
	
	self.evas_canvas.main = self
	self.canvas = self.evas_canvas.evas_obj.evas
	self.window = self.evas_canvas.evas_obj
	#self.window.focus_set(1)
	print self.window.focus_get()
	self.connection_processed = False
	self.restore_conditions = False
	self.key_text = ""
	self.bluetooth_obj = True
	self.edje_obj = ""
	self.adapter_on = False
	self.current_adapter_name = None
	self.current_adapter_addr = None
	self.hw_kb = bluemaemo_hw_kb(self)
		
	self.key_mapper = key_mapper()
	

        self.groups = {}

        self.groups["swallow"] = edje_group(self, "swallow")
        self.evas_canvas.evas_obj.data["swallow"] = self.groups["swallow"]

        for page in ("main","mouse_ui", "menu", "disconnect", "keyboard_ui","about","settings","games", "games_conf","multimedia","multimedia_conf","presentation","presentation_conf","conf_keys", "reconnect_list","confirm_conn","unable_conn","process_conn","wait_conn", "connection_status","new_device", "ps3_control", "ps3_control_conf"):
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
	self.current_label = None
	self.reconnect = True
	self.error = False
	self.connected = False
	self.bluez_version = 3
	self.power = False
	self.discoverable = False
	self.pairable = False
	self.new_device = False
	self.paired_devices = {}
	self.initialize_dbus()
	self.check_bluez_version()
	self.check_bt_status()
	self.check_autoconnect()
	self.export_session_bus()

    def check_bluez_version(self):

		try:

			manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
			path = manager.DefaultAdapter()
			self.bluez_version = 4
			print "Running BlueZ 4"

		except:

			print "Running BlueZ 3"
	

    def check_connection_status(self):
	if not self.connection.connect:
		self.error = False
		self.connected = False
		self.transition_to("disconnect")
		print "->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DISC"

	else:
		ecore.timer_add( 10.0, self.check_connection_status)


    def check_connection(self):

	if self.connection.error:
		self.error = True
	else:

		if not self.connection.connect:
			ecore.timer_add(1.0,self.check_connection)
		else:
			self.connected = True
			ecore.timer_add(10.0, self.check_connection_status)
		
	
    def check_autoconnect(self):
	if self.autoconnect == "Yes":
		self.current_adapter_name = self.auto_name
		self.current_adapter_addr = self.auto_addr
		self.transition_to("process_conn")
	else:
		pass
	
    def check_bt_status(self):

	if self.bluez_version == 3:

		adapter = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')
		state = adapter.GetMode()
		if state == "discoverable":
		
			self.adapter_on = True

		elif state == "off":

			self.power_on_bt()
			self.restore_conditions = "off"

		elif state == "connectable":
		
			self.power_on_bt()
			self.restore_conditions = "connectable"

	else: 

		manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
		path = manager.DefaultAdapter()
		adapter = dbus.Interface(self.bus.get_object("org.bluez", path),"org.bluez.Adapter")
		properties = adapter.GetProperties()
		self.power = properties["Powered"]
		self.discoverable = properties["Discoverable"]
		self.pairable = properties["Pairable"]

		if not self.power:

			adapter.SetProperty("Powered", dbus.Boolean(1))
			adapter.SetProperty("Discoverable", dbus.Boolean(1) )
			adapter.SetProperty("Pairable", dbus.Boolean(1) )
			self.adapter_on = True
			print "off"
			
		elif not self.discoverable:

			adapter.SetProperty("Discoverable", dbus.Boolean(1) )
			adapter.SetProperty("Pairable", dbus.Boolean(1) )
			self.adapter_on = True
			print "dis"

		elif not self.pairable:
		
			adapter.SetProperty("Pairable", dbus.Boolean(1) )
			self.restore_conditions = "connectable"
			self.adapter_on = True
			print "connect"
		else:
			self.adapter_on = True

		self.paired_devs = adapter.ListDevices()
		for item in self.paired_devs:
			
			device = dbus.Interface(self.bus.get_object("org.bluez", item),"org.bluez.Device")
			properties = device.GetProperties()
			client_name = properties["Name"].encode('utf8')
			client_addr =  properties["Address"]
			if str(client_name) == "":
				self.paired_devices["PlayStation 3"] = str(client_addr)
			else:
				self.paired_devices[str(client_name)] = str(client_addr)

    def update_paired_devices(self):

	manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
	path = manager.DefaultAdapter()
	adapter = dbus.Interface(self.bus.get_object("org.bluez", path),"org.bluez.Adapter")	

	self.paired_devs = adapter.ListDevices()

	for item in self.paired_devs:
		
		device = dbus.Interface(self.bus.get_object("org.bluez", item),"org.bluez.Device")
		properties = device.GetProperties()
		client_name = properties["Name"].encode('utf8')
		client_addr =  properties["Address"]
		if str(client_name) == "":
			self.paired_devices["PlayStation 3"] = str(client_addr)
		else:
			self.paired_devices[str(client_name)] = str(client_addr)
	print "devices list updated"


    def check_first_time(self):

	if self.firsttime == 0:
		self.firsttime = 1
		self.auto_name = self.current_adapter_name
		self.auto_addr = self.current_adapter_addr
		self.bluemaemo_conf.set_option("user","firsttime",self.firsttime)
		self.bluemaemo_conf.set_option("autoconnect","name",self.auto_name)
		self.bluemaemo_conf.set_option("autoconnect","addr",self.auto_addr)
		self.bluemaemo_conf.save_options()

	else:
		pass	
		
	
    def initialize_dbus( self ):

        try:
            self.bus = SystemBus( mainloop=e_dbus.DBusEcoreMainLoop() )
	    
        except DBusException, e:
            print "Error: Could not connect to dbus_object system bus:", e
            return False

    def export_session_bus(self):

	if self.bluez_version == 3:
		pass

	else:
		try:
			session_bus_file = open('/tmp/session_bus_address.user', 'r')
			session_bus_command = session_bus_file.readline()
			b = session_bus_command.split('=')
			var = b[1] + "=" + b[2] + "=" + b[3] 
			var = var.split('\'')
			print var
			os.putenv("DBUS_SESSION_BUS_ADDRESS", var[1])

		except:
			
			print "ERROR: Could not export the session bus"

		
    def power_on_bt(self):
	
	os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0 org.bluez.Adapter.SetMode string:discoverable")
	self.adapter_on = True
	print "Bluetooth turned on"
	
        
    def on_exit(self):
	if self.bluez_version == 3:
		if self.restore_conditions == "off":

			os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0 org.bluez.Adapter.SetMode string:connectable")
			os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0 org.bluez.Adapter.SetMode string:off")

		elif self.restore_conditions == "connectable":

			os.system("dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0 org.bluez.Adapter.SetMode string:connectable")

		else:
			pass

	else:
		try:
			manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
			path = manager.DefaultAdapter()
			adapter = dbus.Interface(self.bus.get_object("org.bluez", path),"org.bluez.Adapter")
			if not self.pairable:
				adapter.SetProperty("Pairable", dbus.Boolean(0))
				print "restored pair"

			if not self.discoverable:
				adapter.SetProperty("Discoverable", dbus.Boolean(0))
				print "restored dis"

			if not self.power:
				adapter.SetProperty("Powered", dbus.Boolean(0))
				print "restored power"

			
		except:
			print "Error: Can't restore bluetooth settings"
        

    def initialize_bluemaemo_server(self,addr=1, name=""):

	if self.adapter_on:
		
			self.connection = Connect(self.bluez_version)
			self.connection.start_connection(addr, name)
			self.connection_processed = True

        else:
		ecore.timer_add(1.0,self.initialize_bluemaemo_server)

    def initialize_new_bluemaemo_server(self,addr=1, name=""):

	if self.adapter_on:
		
			self.connection.start_connection(addr, name)
			self.connection_processed = True

        else:
		ecore.timer_add(1.0,self.initialize_bluemaemo_server)
	
    def load_local_confs(self):
	#settings
	self.scroll = int(self.bluemaemo_conf.scroll)
	self.firsttime = int(self.bluemaemo_conf.firsttime)
	self.autoconnect = self.bluemaemo_conf.autoconnect
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
	self.rewind_key = self.bluemaemo_conf.rewind_key
	self.volume_m_key = self.bluemaemo_conf.volume_m_key
	self.volume_p_key = self.bluemaemo_conf.volume_p_key
	self.fullscreen_key_m = self.bluemaemo_conf.fullscreen_key_m
	self.no_fullscreen_key_m = self.bluemaemo_conf.no_fullscreen_key_m
	self.mute_key = self.bluemaemo_conf.mute_key
	self.previous_key_m = self.bluemaemo_conf.previous_key_m
	self.next_key_m = self.bluemaemo_conf.next_key_m
	#games profile
	self.up_key = self.bluemaemo_conf.up_key
	self.down_key = self.bluemaemo_conf.down_key
	self.right_key = self.bluemaemo_conf.right_key
	self.left_key = self.bluemaemo_conf.left_key
	self.a_key = self.bluemaemo_conf.a_key
	self.b_key = self.bluemaemo_conf.b_key
	self.c_key = self.bluemaemo_conf.c_key
	self.x_key = self.bluemaemo_conf.x_key
	self.y_key = self.bluemaemo_conf.y_key
	self.z_key = self.bluemaemo_conf.z_key
	self.one_key = self.bluemaemo_conf.one_key
	self.two_key = self.bluemaemo_conf.two_key
	#ps3 profile
	self.up_p_key = self.bluemaemo_conf.up_p_key
	self.down_p_key = self.bluemaemo_conf.down_p_key
	self.right_p_key = self.bluemaemo_conf.right_p_key
	self.left_p_key = self.bluemaemo_conf.left_p_key
	self.select_key = self.bluemaemo_conf.select_key 
	self.start_key = self.bluemaemo_conf.start_key
	self.triangle_key = self.bluemaemo_conf.triangle_key
	self.square_key = self.bluemaemo_conf.square_key
	self.circle_key = self.bluemaemo_conf.circle_key
	self.cross_key = self.bluemaemo_conf.cross_key
	self.menu_key = self.bluemaemo_conf.menu_key
	self.l1_key = self.bluemaemo_conf.l1_key
	self.l2_key = self.bluemaemo_conf.l2_key
	self.r1_key = self.bluemaemo_conf.r1_key
	self.r2_key = self.bluemaemo_conf.r2_key
	#autoconnect options
	self.auto_name = self.bluemaemo_conf.name
	self.auto_addr = self.bluemaemo_conf.addr
	

    def save_local_conf(self, button_name, profile, key):
	
	if button_name == "Previous" and profile == "presentation":

		self.previous_key = key
		self.bluemaemo_conf.set_option("presentation","previous_key",key)

	elif button_name == "Next" and profile == "presentation":

		self.next_key = key
		self.bluemaemo_conf.set_option("presentation","next_key",key)

	elif button_name == "Fullscreen" and profile == "presentation":

		self.fullscreen_key = key
		self.bluemaemo_conf.set_option("presentation","fullscreen_key",key)

	elif button_name == "No fullscreen" and profile == "presentation":

		self.no_fullscreen_key = key
		self.bluemaemo_conf.set_option("presentation","no_fullscreen_key",key)

	elif button_name == "Play":

		self.play_key = key
		self.bluemaemo_conf.set_option("multimedia","play_key",key)

	elif button_name == "Pause":

		self.pause_key = key
		self.bluemaemo_conf.set_option("multimedia","pause_key",key)

	elif button_name == "Stop":

		self.stop_key = key
		self.bluemaemo_conf.set_option("multimedia","stop_key",key)

	elif button_name == "Forward":

		self.forward_key = key
		self.bluemaemo_conf.set_option("multimedia","forward_key",key)

	elif button_name == "Rewind":

		self.rewind_key = key
		self.bluemaemo_conf.set_option("multimedia","rewind_key",key)

	elif button_name == "Volume +":

		self.volume_p_key = key
		self.bluemaemo_conf.set_option("multimedia","volume_p_key",key)

	elif button_name == "Volume -":

		self.volume_m_key = key
		self.bluemaemo_conf.set_option("multimedia","volume_m_key",key)

	elif button_name == "Mute":

		self.mute_key = key
		self.bluemaemo_conf.set_option("multimedia","mute_key",key)
	
	
	elif button_name == "Fullscreen" and profile == "multimedia":

		self.fullscreen_key_m = key
		self.bluemaemo_conf.set_option("multimedia","fullscreen_key_m",key)

	elif button_name == "No fullscreen" and profile == "multimedia":

		self.no_fullscreen_key_m = key
		self.bluemaemo_conf.set_option("multimedia","no_fullscreen_key_m",key)

	elif button_name == "Previous" and profile == "multimedia":

		self.previous_key_m = key
		self.bluemaemo_conf.set_option("multimedia","previous_key_m",key)

	elif button_name == "Next" and profile == "multimedia":

		self.next_key_m = key
		self.bluemaemo_conf.set_option("multimedia","next_key_m",key)

	elif button_name == "Up":

		self.up_key = key
		self.bluemaemo_conf.set_option("games","up_key",key)

	elif button_name == "Down":

		self.down_key = key
		self.bluemaemo_conf.set_option("games","down_key",key)

	elif button_name == "Right":

		self.right_key = key
		self.bluemaemo_conf.set_option("games","right_key",key)

	elif button_name == "Left":

		self.left_key = key
		self.bluemaemo_conf.set_option("games","left_key",key)
	
	elif button_name == "A":

		self.a_key = key
		self.bluemaemo_conf.set_option("games","a_key",key)

	elif button_name == "B":

		self.b_key = key
		self.bluemaemo_conf.set_option("games","b_key",key)
	
	elif button_name == "C":

		self.c_key = key
		self.bluemaemo_conf.set_option("games","c_key",key)

	elif button_name == "X":

		self.x_key = key
		self.bluemaemo_conf.set_option("games","x_key",key)

	elif button_name == "y":

		self.y_key = key
		self.bluemaemo_conf.set_option("games","y_key",key)

	elif button_name == "Z":

		self.z_key = key
		self.bluemaemo_conf.set_option("games","z_key",key)

	elif button_name == "1":

		self.one_key = key
		self.bluemaemo_conf.set_option("games","one_key",key)

	elif button_name == "2":

		self.two_key = key
		self.bluemaemo_conf.set_option("games","two_key",key)

	elif button_name == "Up" and profile == "ps3_control":

		self.up_p_key = key
		self.bluemaemo_conf.set_option("ps3","up_p_key",key)

	elif button_name == "Down" and profile == "ps3_control":

		self.down_p_key = key
		self.bluemaemo_conf.set_option("ps3","down_p_key",key)

	elif button_name == "Right" and profile == "ps3_control":

		self.right_p_key = key
		self.bluemaemo_conf.set_option("ps3","right_p_key",key)

	elif button_name == "Left" and profile == "ps3_control":

		self.left_p_key = key
		self.bluemaemo_conf.set_option("ps3","left_p_key",key)

	elif button_name == "Select":

		self.select_key = key
		self.bluemaemo_conf.set_option("ps3","select_key",key)

	elif button_name == "Start":

		self.start_key = key
		self.bluemaemo_conf.set_option("ps3","start_key",key)

	elif button_name == "Triangle":

		self.triangle_key = key
		self.bluemaemo_conf.set_option("ps3","triangle_key",key)

	elif button_name == "Square":

		self.square_key = key
		self.bluemaemo_conf.set_option("ps3","square_key",key)

	elif button_name == "Circle":

		self.circle_key = key
		self.bluemaemo_conf.set_option("ps3","circle_key",key)

	elif button_name == "Menu":

		self.menu_key = key
		self.bluemaemo_conf.set_option("ps3","menu_key",key)

	elif button_name == "Cross":

		self.cross_key = key
		self.bluemaemo_conf.set_option("ps3","cross_key",key)

	elif button_name == "L1":

		self.l1_key = key
		self.bluemaemo_conf.set_option("ps3","l1_key",key)

	elif button_name == "L2":

		self.l2_key = key
		self.bluemaemo_conf.set_option("ps3","l2_key",key)

	elif button_name == "R1":

		self.r1_key = key
		self.bluemaemo_conf.set_option("ps3","r1_key",key)

	elif button_name == "R2":

		self.r2_key = key
		self.bluemaemo_conf.set_option("ps3","r2_key",key)


    def task_switcher(self):

	os.system("dbus-send --type=signal --session /com/nokia/hildon_desktop com.nokia.hildon_desktop.exit_app_view")
        print "app minimized"

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
            if ecore.evas.engine_type_supported_get("software_16_x11"):
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
	#self.evas_obj.focus_set(1)
        self.evas_obj.evas.image_cache_set( 6*1024*1024 )
        self.evas_obj.evas.font_cache_set( 2*1024*1024 )
        self.evas_obj.show()

    def on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        evas_obj.data["swallow"].size = size

    def on_delete_request(self, evas_obj):

	try:
		self.main.connection.terminate_connection()
	except:
		print "INFO: Connection is not initialized"

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




