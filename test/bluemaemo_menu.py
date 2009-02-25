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
	self.part_text_set( "label_title", "BlueMaemo" )

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


		elif source == "connection":

			if self.main.connection.connect == True:
				self.main.groups["connection_status"].part_text_set("label_connect_to","Connected to:")
    				self.main.groups["connection_status"].part_text_set("label_client", self.main.connection.client_name)
				self.main.groups["connection_status"].part_text_set("label_addr",self.main.connection.client_addr)
			else:
				self.part_text_set("label_not_connect","You are not connect to any device")
		
			self.main.transition_to("connection_status")

		elif source == "about":
			
			self.main.groups["about"].part_text_set("label_version","BlueMaemo v0.2")
			self.main.groups["about"].part_text_set("label_developed","Developed by:")
			self.main.groups["about"].part_text_set("label_name","Valerio Valerio")
			self.main.groups["about"].part_text_set("label_email","<vdv100@gmail.com>")

			
			self.main.transition_to("about")	

		elif source == "conf":

			self.main.transition_to("settings")			
		else:
			
			print "feature not implemented yet :) "

