#
#      bluemaemo_connection_status.py
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
class connection_status(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "connection_status")
	self.part_text_set( "menu_title", "Connected" )
	self.part_text_set("label_name", "")
	self.part_text_set("label_name_shadow", "")
        
    def onShow( self ):
	self.part_text_set("label_name", self.main.current_adapter_name)
	self.part_text_set("label_name_shadow", self.main.current_adapter_name)
	self.focus = True
	ecore.timer_add(3.0,self.main.transition_to,"menu")
    

    def onHide( self ):
	self.focus = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

	if key == "Escape":
		self.main.transition_to("menu")
		
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source == "task_switcher":

		self.main.task_switcher()

