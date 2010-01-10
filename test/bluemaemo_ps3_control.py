#
#      bluemaemo_ps3_control.py
#
#      Copyright 2009 Valerio Valerio <vdv100@gmail.com>
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
class ps3_control(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "ps3_control")
	self.part_text_set( "menu_title", "PS3 Control" )	

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

	elif source == "down":

		key = self.main.down_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		
	elif source == "left":


		key = self.main.left_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		
	elif source == "right":


		key = self.main.right_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "select":

		key = self.main.select_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
	
	elif source == "start":

		key = self.main.start_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "triangle":

		key = self.main.triangle_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, val)
		
	elif source == "square":

		key = self.main.square_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
	
	elif source == "circle":

		key = self.main.circle_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, val)
		
	elif source == "menu":


		key = self.main.menu_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)
		
	elif source == "cross":


		key = self.main.cross_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif, val)

	elif source == "L1":

		key = self.main.l1_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "L2":

		key = self.main.l2_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "R1":

		key = self.main.r1_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "R2":

		key = self.main.r2_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_button_released(self, emission, source):

	if source =="back":
		self.main.transition_to("menu")	
	
	elif source == "task_switcher":

		self.main.task_switcher()

	elif source == "settings":

		self.main.transition_to("ps3_control_conf")

	else:
		self.main.connection.release_keyboard_event()
		self.key_pressed = False

#----------------------------------------------------------------------------#
class ps3_control_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "ps3_control_conf")
	self.part_text_set( "menu_title", "PS3 Control settings" )
	count = 0
	self.key_value = ""    
	self.constructed = False
	self.up_p_key = ""
	self.down_p_key = ""
	self.right_p_key = ""
	self.left_p_key = ""
	self.select_key = ""
	self.start_key = ""
	self.triangle_key = ""
	self.square_key = ""
	self.circle_key = ""
	self.cross_key = ""
	self.menu_key = ""
	self.l1_key = ""
	self.l2_key = ""
	self.r1_key = ""
	self.r2_key = ""

	self.up_p_key_lb = elementary.Label(self)
	self.down_p_key_lb = elementary.Label(self)
	self.right_p_key_lb = elementary.Label(self)
	self.left_p_key_lb = elementary.Label(self)
	self.select_key_lb = elementary.Label(self)
	self.start_key_lb = elementary.Label(self)
	self.triangle_key_lb = elementary.Label(self)
	self.square_key_lb = elementary.Label(self)
	self.circle_key_lb = elementary.Label(self)
	self.cross_key_lb = elementary.Label(self)
	self.menu_key_lb = elementary.Label(self)
	self.l1_key_lb = elementary.Label(self)
	self.l2_key_lb = elementary.Label(self)
	self.r1_key_lb = elementary.Label(self)
	self.r2_key_lb = elementary.Label(self)

	for i in (self.main.up_p_key,self.main.down_p_key,self.main.right_p_key,self.main.left_p_key,self.main.select_key,self.main.start_key, self.main.triangle_key, self.main.square_key, self.main.circle_key, self.main.cross_key, self.main.menu_key, self.main.l1_key, self.main.l2_key, self.main.r1_key, self.main.r1_key ):

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
			self.up_p_key = text_value
		elif count == 2:
			self.down_p_key = text_value
		elif count == 3:
			self.right_p_key = text_value
		elif count == 4:
			self.left_p_key = text_value
		elif count == 5:
			self.select_key = text_value
		elif count == 6:
			self.start_key = text_value
		elif count == 7:
			self.triangle_key = text_value
		elif count == 8:
			self.square_key = text_value
		elif count == 9:
			self.circle_key = text_value
		elif count == 10:
			self.cross_key = text_value
		elif count == 11:
			self.menu_key = text_value
		elif count == 12:
			self.l1_key = text_value
		elif count == 13:
			self.l2_key = text_value
		elif count == 14:
			self.r1_key = text_value
		elif count == 15:
			self.r2_key = text_value

	self.up_p_key_lb.label_set(self.up_p_key)
	self.down_p_key_lb.label_set(self.down_p_key)
	self.right_p_key_lb.label_set(self.right_p_key)
	self.left_p_key_lb.label_set(self.left_p_key)
	self.select_key_lb.label_set(self.select_key)
	self.start_key_lb.label_set(self.start_key)
	self.triangle_key_lb.label_set(self.triangle_key)
	self.square_key_lb.label_set(self.square_key)
	self.circle_key_lb.label_set(self.circle_key)
	self.cross_key_lb.label_set(self.cross_key)
	self.menu_key_lb.label_set(self.menu_key)
	self.l1_key_lb.label_set(self.l1_key)
	self.l2_key_lb.label_set(self.l2_key)
	self.r1_key_lb.label_set(self.r1_key)
	self.r2_key_lb.label_set(self.r2_key)
	
	self.labels = {"Up":self.up_p_key_lb,
		"Down":self.down_p_key_lb,
		"Right":self.right_p_key_lb,
		"Left":self.left_p_key_lb,
		"Select":self.select_key_lb,
		"Start":self.start_key_lb,
		"Triangle":self.triangle_key_lb,
		"Square":self.square_key_lb,
		"Circle":self.circle_key_lb,
		"Cross":self.cross_key_lb,
		"Menu":self.menu_key_lb,
		"L1":self.l1_key_lb,
		"L2":self.l2_key_lb,
		"R1":self.r1_key_lb,
		"R2":self.r2_key_lb}

	self.items = {"Up":self.up_p_key,
		"Down":self.down_p_key,
		"Right":self.right_p_key,
		"Left":self.left_p_key,
		"Select":self.select_key,
		"Start":self.start_key,
		"Triangle":self.triangle_key,
		"Square":self.square_key,
		"Circle":self.circle_key,
		"Cross":self.cross_key,
		"Menu":self.menu_key,
		"L1":self.l1_key,
		"L2":self.l2_key,
		"R1":self.r1_key,
		"R2":self.r2_key,}

    def list_item_cb(self,obj, event, data):
	self.obj = obj
	label = obj.label_get()
	label_obj = self.labels[label]
	current_conf = self.items[label]
	self.main.current_conf_screen = "ps3_control"
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
		self.main.transition_to("ps3_control")

	elif source == "task_switcher":

		self.main.task_switcher()
	
	else:

		self.main.current_conf_screen = "ps3_control"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value + "  ")
		self.main.transition_to("conf_keys")	


