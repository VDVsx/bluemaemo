#
#      bluemaemo_disconnect.py
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
class disconnect(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "disconnect")
        
	self.part_text_set("label_error","Error: Disconnected by remote device")
	self.part_text_set("label_connect", "Try to reconnect ?")


    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):

	if source == "no_option":
		
		self.main.connection.terminate_connection()
		self.main.transition_to("main")

	elif source == "quit":

		self.main.connection.terminate_connection()
		self.main.on_exit()
		ecore.main_loop_quit()

	elif source == "yes_option":
	
		self.main.connection.terminate_connection()
		self.main.transition_to("process_conn")

	elif source == "task_switcher":

		self.main.task_switcher()
		
