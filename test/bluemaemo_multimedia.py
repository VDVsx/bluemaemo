#
#      bluemaemo_multimedia.py
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
from bluemaemo_edje_group import *

#----------------------------------------------------------------------------#
class multimedia(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "multimedia")

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
	if source == "back":
		
		self.main.transition_to("menu")	
		
	elif source ==	"conf_keys":
		
		self.main.transition_to("multimedia_conf")


	elif source == "play":

		key = self.main.play_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "pause":

		key = self.main.pause_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "stop":

		key = self.main.stop_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "forward":

		key = self.main.forward_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "backward":

		key = self.main.backward_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "volume-":

		key = self.main.volume_m_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "volume+":

		key = self.main.volume_p_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "fullscreen":

		key = self.main.fullscreen_key_m
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key_m
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_button_released(self, emission, source):

	if source =="back" or source == "conf_keys":
		pass
	else:
		self.main.connection.release_keyboard_event()


#----------------------------------------------------------------------------#
class multimedia_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "multimedia_conf")
	count = 0
	self.play_key = ""
	self.pause_key = ""
	self.stop_key = ""
	self.forw_key = ""
	self.backw_key = ""
	self.vol_m_key = ""
	self.vol_p_key = ""
	self.full_key = ""
	self.no_full_key = ""

	for i in (self.main.play_key,self.main.pause_key,self.main.stop_key,self.main.forward_key,self.main.backward_key, self.main.volume_m_key,self.main.volume_p_key,self.main.fullscreen_key_m, self.main.no_fullscreen_key_m):
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
			self.play_key = text_value
		elif count == 2:
			self.pause_key = text_value
		elif count == 3:
			self.stop_key = text_value
		elif count == 4:
			self.forw_key = text_value
		elif count == 5:
			self.backw_key = text_value
		elif count == 6:
			self.vol_m_key = text_value
		elif count == 7:
			self.vol_p_key = text_value
		elif count == 8:
			self.full_key = text_value
		elif count == 9:
			self.no_full_key = text_value
				
		 
	self.part_text_set("play_key_icon", self.play_key)
	self.part_text_set("pause_key_icon", self.pause_key)
	self.part_text_set("stop_key_icon", self.stop_key)
	self.part_text_set("forward_key_icon", self.forw_key)
	self.part_text_set("backward_key_icon", self.backw_key)
	self.part_text_set("volume_m_key_icon", self.vol_m_key)
	self.part_text_set("volume_p_key_icon", self.vol_p_key)
	self.part_text_set("fullscreen_key_m_icon", self.full_key)
	self.part_text_set("no_fullscreen_key_m_icon", self.no_full_key)
	self.key_value = ""
	self.signal_emit("hide_screen_2", "")
	self.signal_emit("show_screen_1", "")


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

	elif key == "Escape":

		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("multimedia")	

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":

		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("multimedia")	

	elif source == "1":

		self.signal_emit("hide_screen_2", "")
		self.signal_emit("show_screen_1", "")

	elif source == "2":

		self.signal_emit("hide_screen_1", "")
		self.signal_emit("show_screen_2", "")
	
	else:
		
		if source == "play_key":

			self.key_value = self.part_text_get("play_key_icon")
			self.main.key_text = self.key_value

		elif source == "pause_key":

			self.key_value = self.part_text_get("pause_key_icon")
			self.main.key_text = self.key_value

		if source == "stop_key":

			self.key_value = self.part_text_get("stop_key_icon")
			self.main.key_text = self.key_value

		elif source == "forward_key":

			self.key_value = self.part_text_get("forward_key_icon")
			self.main.key_text = self.key_value

		if source == "backward_key":

			self.key_value = self.part_text_get("backward_key_icon")
			self.main.key_text = self.key_value

		elif source == "volume_m_key":

			self.key_value = self.part_text_get("volume_m_key_icon")
			self.main.key_text = self.key_value

		elif source == "volume_p_key":

			self.key_value = self.part_text_get("volume_p_key_icon")
			self.main.key_text = self.key_value


		elif source == "fullscreen_key_m":

			self.key_value = self.part_text_get("fullscreen_key_m_icon")
			self.main.key_text = self.key_value

		elif source == "no_fullscreen_key_m":

			self.key_value = self.part_text_get("no_fullscreen_key_m_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "multimedia"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value + "  ")
		self.main.transition_to("conf_keys")	
	
