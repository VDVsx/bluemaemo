#
#      bluemaemo_settings.py
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
class settings(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "settings")
        self.part_text_set( "menu_title", "Settings" )
	self.main = main
        self.part_text_set("fullscreen_option",str(self.main.bluemaemo_conf.fullscreen))
	self.part_text_set("scroll_option", str(self.main.bluemaemo_conf.scroll))
	self.part_text_set("auto_connect_option",str(self.main.bluemaemo_conf.autoconnect))
	self.part_text_set("current_device_icon",str(self.main.bluemaemo_conf.name))
	self.scroll_value = int(self.main.bluemaemo_conf.scroll)
	self.fscreen_option = str(self.main.bluemaemo_conf.fullscreen)
	self.autoconnect_option = str(self.main.bluemaemo_conf.autoconnect)
	if self.autoconnect_option == "No":
		self.signal_emit("hide_auto_conn_device","")

    def onShow( self ):
	self.part_text_set("current_device_icon",str(self.main.auto_name))
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

		self.main.transition_to("menu")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	 

	if source == "back":
		
		self.main.bluemaemo_conf.set_option("user","fullscreen",self.fscreen_option)
		self.main.bluemaemo_conf.set_option("user","scroll",self.scroll_value)
		self.main.bluemaemo_conf.set_option("user","autoconnect",self.autoconnect_option)
		self.main.bluemaemo_conf.set_option("autoconnect","name",self.main.auto_name)
		self.main.bluemaemo_conf.set_option("autoconnect","addr",self.main.auto_addr)
		self.main.bluemaemo_conf.save_options()
		self.main.scroll = self.scroll_value
		self.main.transition_to("menu")

	elif source == "fullscreen_option":
		
		if self.fscreen_option == "Yes":
			
			self.part_text_set("fullscreen_option","No")
			self.fscreen_option = "No"
			self.main.window.fullscreen = False

		else:
			
			self.part_text_set("fullscreen_option","Yes")
			self.fscreen_option = "Yes"
			self.main.window.fullscreen = True

	elif source == "scroll_right_icon":
		
		if self.scroll_value < 9:
			self.scroll_value += 1
			self.part_text_set("scroll_option", str(self.scroll_value))
	
	elif source == "scroll_left_icon":
		
		if self.scroll_value >= 1:
			self.scroll_value -= 1
			self.part_text_set("scroll_option", str(self.scroll_value))

	elif source == "auto_connect_option":

		if self.autoconnect_option == "Yes":
			self.part_text_set("auto_connect_option","No")
			self.autoconnect_option = "No"
			self.signal_emit("hide_auto_conn_device","")

		else:
			self.part_text_set("auto_connect_option","Yes")
			self.autoconnect_option = "Yes"
			self.signal_emit("show_auto_conn_device","")

	elif source == "current_device":
		self.main.transition_to("rec_list")

