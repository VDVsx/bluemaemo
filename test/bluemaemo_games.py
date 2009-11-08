#
#      bluemaemo_games.py
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



import e_dbus
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.x
import ecore.evas
import elementary
from accelerometer import *
from bluemaemo_edje_group import *


#----------------------------------------------------------------------------#
class games(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games")
	self.part_text_set( "menu_title", "Gamepad" )
	self.key_pressed = False
	self.current_key= ""
	self.current_modif= ""
	self.press = False
	self.first_time = True

	self.accel = Read_accelerometer(self)

    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False

    @evas.decorators.key_up_callback
    def key_up_cb( self, event ):
	self.main.connection.release_keyboard_event()
        key = event.keyname

	if key == "Shift_L":
		self.main.hw_kb.shift = False

	elif key == "ISO_Level3_Shift":
		self.main.hw_kb.fn = False
	
	elif key == "Control_L" or key == "Control_R":
		self.main.hw_kb.ctrl = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

	self.main.hw_kb.send_hw_kb_key(key)

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	
	if source == "up":


		key = self.main.up_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		self.key_pressed = True
		self.current_key= val  #check if this is in use
		self.current_modif= modif

	elif source == "down":


		key = self.main.down_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif

	elif source == "left":


		key = self.main.left_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		self.current_key= val
		self.current_modif= modif

	elif source == "right":


		key = self.main.right_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif

	elif source == "A":
		
		#self.main.transition_to("games_conf")

		if self.accel.accel_on:
			 self.accel.accel_on = False
		else:
			self.accel.accel_on = True
			self.accel.read_dir(self.main)
			
		#key = self.main.a_key
		#modif, val = key_dec(self,key)
		#self.main.connection.send_keyboard_event(modif,val)
		#self.key_pressed = True
		#self.current_key= val
		#self.current_modif= modif
	
	elif source == "B":

		if not self.press:
			self.press = True
			self.accel.air_mouse(self.main)
			self.first_time = False

		else:
			self.press = False
			self.first_time = True
		#key = self.main.b_key
		#modif, val = key_dec(self,key)
		#self.main.connection.send_keyboard_event(modif,val)
		#self.key_pressed = True
		#self.current_key= val
		#self.current_modif= modif

	elif source == "C":


		key = self.main.c_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, val)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif

	elif source == "X":


		key = self.main.x_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif

	elif source == "Y":


		key = self.main.y_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, value)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif
	
	elif source == "Z":


		key = self.main.z_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,value)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif

	elif source == "one":


		key = self.main.one_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, value)
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif


	elif source == "two":


		key = self.main.two_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event('0','40')
		self.key_pressed = True
		self.current_key= val
		self.current_modif= modif






	elif source == "D":

		self.main.connection.send_mouse_event(1,0,0,0)
		self.main.connection.send_mouse_event(0,0,0,0)	
		#key = self.main.d_key
		#modif, val = key_dec(self,key)
		#self.main.connection.send_keyboard_event(modif,val)
		#self.key_pressed = True
		#self.current_key= val
		#self.current_modif= modif

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_button_released(self, emission, source):

	if source =="back":
		self.main.transition_to("menu")	
	
	elif source == "task_switcher":

		self.main.task_switcher()

	elif source == "settings":

		self.main.transition_to("games_conf")

	else:
		self.main.connection.release_keyboard_event()
		self.key_pressed = False

#----------------------------------------------------------------------------#
class games_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games_conf")
	self.part_text_set( "menu_title", "Multimedia settings" )
	count = 0
	self.key_value = ""    
	self.constructed = False
	self.up_key = ""
	self.down_key = ""
	self.right_key = ""
	self.left_key = ""
	self.a_key = ""
	self.b_key = ""
	self.c_key = ""
	self.x_key = ""
	self.y_key = ""
	self.z_key = ""
	self.one_key = ""
	self.two_key = ""

	self.up_key_lb = elementary.Label(self)
	self.down_key_lb = elementary.Label(self)
	self.right_key_lb = elementary.Label(self)
	self.left_key_lb = elementary.Label(self)
	self.a_key_lb = elementary.Label(self)
	self.b_key_lb = elementary.Label(self)
	self.c_key_lb = elementary.Label(self)
	self.x_key_lb = elementary.Label(self)
	self.y_key_lb = elementary.Label(self)
	self.z_key_lb = elementary.Label(self)
	self.one_key_lb = elementary.Label(self)
	self.two_key_lb = elementary.Label(self)
	
	for i in (self.main.up_key,self.main.down_key,self.main.right_key,self.main.left_key,self.main.a_key,self.main.b_key, self.main.c_key, self.main.x_key, self.y_key, self.z_key, self.one_key, self.two_key ):

		if len(i) > 6 and i[0] == "s":
			#shift translation
			
			text_value = self.main.key_mapper.mapper[i]
			count +=1

		elif len(i) > 5 and i[0] == "f" and i[1] == "n":
				val = str(i) + "+u"
				text_value = self.main.key_mapper.mapper[val]
				count +=1
		elif len(i) == 4 and i[0] == "s" and i[1] == "p":
				text_value = self.main.key_mapper.mapper[i]
				count +=1

		else:
			text_value = i
			count +=1
		if count == 1:
			self.up_key = text_value
		elif count == 2:
			self.down_key = text_value
		elif count == 3:
			self.right_key = text_value
		elif count == 4:
			self.left_key = text_value
		elif count == 5:
			self.a_key = text_value
		elif count == 6:
			self.b_key = text_value
		elif count == 7:
			self.c_key = text_value
		elif count == 8:
			self.x_key = text_value
		elif count == 9:
			self.y_key = text_value
		elif count == 10:
			self.z_key = text_value
		elif count == 11:
			self.one_key = text_value
		elif count == 12:
			self.two_key = text_value
				
	self.up_key_lb.label_set(self.up_key)
	self.down_key_lb.label_set(self.down_key)
	self.right_key_lb.label_set(self.right_key)
	self.left_key_lb.label_set(self.left_key)
	self.a_key_lb.label_set(self.a_key)
	self.b_key_lb.label_set(self.b_key)
	self.c_key_lb.label_set(self.c_key)
	self.x_key_lb.label_set(self.x_key) 
	self.y_key_lb.label_set(self.y_key) 
	self.z_key_lb.label_set(self.z_key) 
	self.one_key_lb.label_set(self.one_key) 
	self.two_key_lb.label_set(self.two_key) 
	
	self.labels = {"Up":self.up_key_lb,
		"Down":self.down_key_lb,
		"Right":self.right_key_lb,
		"Left":self.left_key_lb,
		"A":self.a_key_lb,
		"B":self.b_key_lb,
		"C":self.c_key_lb,
		"X":self.x_key_lb,
		"Y":self.y_key_lb,
		"Z":self.z_key_lb,
		"1":self.one_key_lb,
		"2":self.two_key_lb}

	self.items = {"Up":self.up_key,
		"Down":self.down_key,
		"Right":self.right_key,
		"Left":self.left_key,
		"A":self.a_key,
		"B":self.b_key,
		"C":self.c_key,
		"X":self.x_key,
		"Y":self.y_key,
		"Z":self.z_key,
		"1":self.one_key,
		"2":self.two_key}

    def list_item_cb(self,obj, event, data):
	self.obj = obj
	label = obj.label_get()
	label_obj = self.labels[label]
	current_conf = self.items[label]
	self.main.current_conf_screen = "games"
	self.main.current_source = label_obj
	self.main.current_label = label
	self.main.groups["conf_keys"].part_text_set("value","  "+current_conf + "  ")
	self.main.transition_to("conf_keys")
	self.obj.selected_set(0)
	
	
    def onShow( self ):

	self.focus = True
	if self.constructed:
		self.li.go()
		self.li.show()
	else:
		self.li = elementary.List(self)
	    	self.li.size_hint_weight_set(1.0, 1.0)
	    	self.li.size_hint_align_set(-1.0, -1.0)
		self.li.geometry_set(0,54, 800,372)
		self.li.show()
	
		labels_sorted = self.labels.keys()
		labels_sorted.sort()
		for item in labels_sorted:

			item_list = self.li.item_append(item, None, self.labels[item] , self.list_item_cb)
				
		
	    	self.li.go()
		self.constructed = True
	
    
    def onHide( self ):
	self.focus = False
     	self.li.hide()

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":

		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("games")

	elif source == "task_switcher":

		self.main.task_switcher()
	
	else:

		self.main.current_conf_screen = "games"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value + "  ")
		self.main.transition_to("conf_keys")	


