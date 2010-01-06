#
#      bluemaemo_recon_list.py
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
import time
import sys
import os
import elementary
from bluemaemo_edje_group import *

#----------------------------------------------------------------------------#
class reconnect_list(edje_group):
#----------------------------------------------------------------------------#


	def __init__(self,main):

        	edje_group.__init__(self, main, "reconnect_list")
		self.main = main
		self.part_text_set( "menu_title", "Paired Devices" )
					
		self.constructed = False
		self.labels = {}

	def list_item_cb(self,obj, event, data):
		self.obj = obj
		label = obj.label_get()
		client_addr = self.main.paired_devices[label]
		self.main.current_adapter_addr = client_addr
		self.main.current_adapter_name = label
		self.main.transition_to("process_conn")
		self.obj.selected_set(0)
			
	def onShow( self ):
		self.focus = True
		self.main.update_paired_devices()
		
		self.li = elementary.List(self)
	    	self.li.size_hint_weight_set(1.0, 1.0)
	    	self.li.size_hint_align_set(-1.0, -1.0)
		self.li.geometry_set(0,54, 800,372)
		self.li.show()

		labels_sorted = self.main.paired_devices.keys()
		labels_sorted.sort()
		for item in labels_sorted:

			item_list = self.li.item_append(item, None, None , self.list_item_cb)
			
	
	    	self.li.go()


    	def onHide( self ):
		self.focus = False
		self.li.hide()


	@evas.decorators.key_down_callback
    	def key_down_cb( self, event ):
		key = event.keyname

	
		if key == "Escape":
			
			
			self.main.transition_to("main")
    
	@edje.decorators.signal_callback("mouse,clicked,1", "*")
        def on_edje_signal_button_pressed(self, emission, source):

		if source == "back":
		
			self.main.transition_to("main")

		elif source == "task_switcher":

			self.main.task_switcher()

