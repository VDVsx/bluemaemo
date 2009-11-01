#
#      bluemaemo_presentation.py
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
from bluemaemo_edje_group import *


#----------------------------------------------------------------------------#
class presentation(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation")
        self.part_text_set( "menu_title", "Presentation" )

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

	if key == "F6":

		if self.main.bluemaemo_conf.fullscreen == "Yes":
			
			self.main.bluemaemo_conf.fullscreen = "No"
			self.main.window.fullscreen = False

		elif self.main.bluemaemo_conf.fullscreen == "No":
			
			self.main.bluemaemo_conf.fullscreen = "Yes"
			self.main.window.fullscreen = True
	
	#elif key == "Escape":

	#	self.main.transition_to("menu")

	else:

		self.main.hw_kb.send_hw_kb_key(key)

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):


	if source == "conf_keys":
		
		self.main.transition_to("presentation_conf")

	elif source == "previous":


		key = self.main.previous_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "next":

		key = self.main.next_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "fullscreen":

		key = self.main.fullscreen_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_button_released(self, emission, source):

	if source =="back":

		self.main.transition_to("menu")	

	elif source == "task_switcher":

		self.main.task_switcher()

	elif source == "settings":

		self.main.transition_to("presentation_conf")

	else:
		self.main.connection.release_keyboard_event()

#----------------------------------------------------------------------------#
class presentation_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation_conf")
	self.part_text_set( "menu_title", "Presentation settings" )
	count = 0
	self.key_value = ""    
	self.constructed = False
	self.prev_key = ""
	self.next_key = ""
	self.full_key = ""
	self.no_full_key = ""


	self.prev_key_lb = elementary.Label(self)
	self.next_key_lb = elementary.Label(self)
	self.full_key_lb = elementary.Label(self)
	self.no_full_key_lb = elementary.Label(self)
	

	for i in (self.main.previous_key,self.main.next_key,self.main.fullscreen_key, self.main.no_fullscreen_key):
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
			self.prev_key = text_value
		elif count == 2:
			self.next_key = text_value
		elif count == 3:
			self.full_key = text_value
		elif count == 4:
			self.no_full_key = text_value

	self.prev_key_lb.label_set(self.prev_key)
	self.next_key_lb.label_set(self.next_key)
	self.full_key_lb.label_set(self.full_key)
	self.no_full_key_lb.label_set(self.no_full_key)			
	
	self.labels = {"Previous":self.prev_key_lb,
		"Next":self.next_key_lb,
		"Fullscreen":self.full_key_lb,
		"No fullscreen":self.no_full_key_lb}

	self.items = {"Previous":self.prev_key,
		"Next":self.next_key,
		"Fullscreen":self.full_key,
		"No fullscreen":self.no_full_key}

	self.key_value = ""

    def list_item_cb(self,obj, event, data):

	self.obj = obj
	label = obj.label_get()
	label_obj = self.labels[label]
	current_conf = self.items[label]
	self.main.current_conf_screen = "presentation"
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
		
	elif key == "Escape":

		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("presentation")	

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("presentation")	
	
	elif source == "task_switcher":

		self.main.task_switcher()
	else:

		self.main.current_conf_screen = "presentation"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value+ "  ")
		self.main.transition_to("conf_keys")	
	

