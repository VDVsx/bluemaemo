#
#      bluemaemo_keyboard.py
#
#      Copyright 2008 -2009 	Valerio Valerio <vdv100@gmail.com>
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



import time
import e_dbus
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.x
import ecore.evas
from bluemaemo_edje_group import *


#----------------------------------------------------------------------------#
class keyboard_ui(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "keyboard_ui")
        self.alt = False
        self.ctrl = False
	self.fn = False
	self.tape_mouse_area = 0
	self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True
	self.shift = False
	self.sent_key = False

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
     	print self.focus_get()

    def onHide( self ):
	self.focus = False
	self.signal_emit("activate_keyboard_sw", "")
     

    @evas.decorators.key_up_callback
    def key_up_cb( self, event ):
	self.main.connection.release_keyboard_event()
        key = event.keyname

	if key == "Shift_L":
		self.shift = False

	elif key == "ISO_Level3_Shift":
		self.fn = False

	elif key == "Control_L" or key == "Control_R":
		self.ctrl = False

    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname
	
	try:
		if key == "Shift_L":
			self.shift = True
			
		elif key == "Control_L" or key == "Control_R":
			self.ctrl = True
			
		elif key == "Alt_L":
			self.alt = True

		elif key == "ISO_Level3_Shift":
			self.fn = True
			
		else:
			
			value = self.main.key_mapper.mapper[str(key)]
			
			if self.shift:
				self.main.connection.send_keyboard_event("02",value)
			
			elif self.alt and self.ctrl:
				self.main.connection.send_keyboard_event("05",value)
				self.ctrl = False
				self.alt = False
				
			elif self.ctrl:
				self.main.connection.send_keyboard_event("01",value)
				self.ctrl = False
				
			elif self.alt:
				self.main.connection.send_keyboard_event("04",value) 	
				self.alt = False
			
			elif str(key) == "plus" and not self.fn:

				self.main.connection.send_keyboard_event("02",value) 
			
			elif self.fn:
				modi = self.main.key_mapper.mapper["fn_m+"+str(key)]
				value2 = self.main.key_mapper.mapper["fn_k+"+str(key)]
				self.main.connection.send_keyboard_event(modi,value2) 	
			
			else:
				self.main.connection.send_keyboard_event("00",value)
	except:
		print "Key error --->>>"

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source == "task_switcher":

		self.main.task_switcher()


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

	if source == "mouse_switcher":

		self.signal_emit("mouse_sw_pressed","")   

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
	o.signal_emit("activated_key", subpart)

    @edje.decorators.signal_callback("mouse,down,1,*", "*")
    def on_edje_signal_mouse_down_multiple_key(self, emission, source):
        self.on_edje_signal_mouse_down_key(self, emission, source)
        
    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_mouse_up_key(self, emission, source):

	if source == "mouse_switcher":

		self.main.transition_to("mouse_ui")

        if ':' not in source:
            return
	self.main.connection.release_keyboard_event()   
        part, subpart = source.split(':', 1)
        o = self.obj[part]
        self.is_mouse_down = False
        if subpart in self.pressed_keys:
            del self.pressed_keys[subpart]
            o.signal_emit("release_key", subpart)
            


    @edje.decorators.signal_callback("key_down", "*")
    def on_edje_signal_key_down(self, emission, source):

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
		self.sent_key = True
		mod = self.main.key_mapper.mapper[key + "_m"]
		key_s = self.main.key_mapper.mapper[key + "_k"]
		
		self.main.connection.send_keyboard_event(mod,key_s)
        elif key == "space":
	    key_s = "space"
	elif key == "enter":
	    key_s = "Return"
	elif key == "backspace":
	    key_s = "BackSpace"
        else:
	    key_s = key

	if key_s == "NULL" or self.sent_key:
		self.sent_key = False
	else:

		
		val = self.main.key_mapper.mapper[key_s]
		
		if self.is_shift_down:
			self.main.connection.send_keyboard_event("02",val)
			self.release_shift()

		elif self.is_ctrl_down and self.is_alt_down:
			self.main.connection.send_keyboard_event("05",val)
			self.release_ctrl()
			self.release_alt()
				
		elif self.is_ctrl_down:
			self.main.connection.send_keyboard_event("01",val)
			self.release_ctrl()
				
		elif self.is_alt_down:
			self.main.connection.send_keyboard_event("04",val) 	
			self.release_alt()

		else:
			self.main.connection.send_keyboard_event("00",val)
            


######## Mouse Area ##############################

    @edje.decorators.signal_callback("mouse,down,1", "background")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True
		self.tape_mouse_area = time.time()

    @edje.decorators.signal_callback("mouse,up,1", "background")
    def on_mouse_up(self, emission, source):

		
		tape_time = time.time() - self.tape_mouse_area
		
		if tape_time < 0.2:

			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)	

		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down:
			
			if self.first_touch:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
					
				mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
				self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	


