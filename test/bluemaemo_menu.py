#
#      bluemaemo_menu.py
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
class menu(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "menu")
	self.part_text_set( "menu_title", "Main Menu" )
	self.part_text_set( "mouse_text2", "Mouse")
	self.part_text_set( "mouse_text", "Mouse")
	self.part_text_set( "keyboard_text", "Keyboard")
	self.part_text_set( "keyboard_text2", "Keyboard")
	self.part_text_set( "presentation_text", "Presentation")
	self.part_text_set( "presentation_text2", "Presentation")
	self.part_text_set( "multimedia_text", "Media Remote")
	self.part_text_set( "multimedia_text2", "Media Remote")
	self.part_text_set( "games_text", "Gamepad")
	self.part_text_set( "games_text2", "Gamepad")
	self.part_text_set( "ps3_text", "PS3 Control")
	self.part_text_set( "ps3_text2", "PS3 Control")
	self.part_text_set( "conf_text", "Settings")
	self.part_text_set( "conf_text2", "Settings")
	self.part_text_set( "about_text", "About")
	self.part_text_set( "about_text2", "About")

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
        
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
 
		if source == "quit":
		
			self.main.connection.terminate_connection()
			self.main.on_exit()
			ecore.main_loop_quit()

		elif source == "task_switcher":

			self.main.task_switcher()
			
		elif source == "mouse":
			
			self.main.transition_to("mouse_ui")

		elif source == "keyboard":
			
			self.main.transition_to("keyboard_ui")

		elif source == "presentation":
			
			self.main.transition_to("presentation")

		elif source == "multimedia":
			
			self.main.transition_to("multimedia")

		elif source == "games":
			
			self.main.transition_to("games")
		
		elif source == "ps3":
			
			self.main.transition_to("ps3_control")


		elif source == "connection":

			if self.main.connection.connect:
				self.main.groups["connection_status"].part_text_set("label_connect_to","Connected to:")
    				self.main.groups["connection_status"].part_text_set("label_client", self.main.connection.client_name)
				self.main.groups["connection_status"].part_text_set("label_addr",self.main.connection.client_addr)
			else:
				self.part_text_set("label_not_connect","You are not connect to any device")
		
			self.main.transition_to("connection_status")

		elif source == "about":
			
			self.main.transition_to("about")	

		elif source == "conf":

			self.main.transition_to("settings")			
		else:
			print source
			print "feature not implemented yet :) "

