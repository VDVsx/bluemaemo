#
#      bluemaemo_main.py
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

import dbus
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
class main(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "main")
	self.part_text_set( "menu_title", "BlueMaemo" )
	self.part_text_set( "wait_connection_text2", "Wait for connection")
	self.part_text_set( "wait_connection_text", "Wait for connection")
	self.part_text_set( "connect_text2", "Establish connection")
	self.part_text_set( "connect_text", "Establish connection")
	self.part_text_set( "reconnect_text2", "Reconnect")
	self.part_text_set( "reconnect_text", "Reconnect")
	self.main = main
	
	ecore.timer_add(1.0,self.main.transition_to,"menu")
    
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
		
		self.main.on_exit()
		ecore.main_loop_quit()

	elif source == "connect":

		self.bus = self.main.bus
		manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
		
		self.path = manager.DefaultAdapter()
		self.adapter = dbus.Interface(self.bus.get_object("org.bluez", self.path),"org.bluez.Adapter")
		self.adapter.connect_to_signal("DeviceCreated", self._device_created)

		os.system("dbus-send --system --print-reply --dest=com.nokia.bt_ui /com/nokia/bt_ui com.nokia.bt_ui.show_search_dlg string: string: array:string: string:require")
		#self.dbus_bt_dialog = dbus.Interface(self.bus.get_object("com.nokia.bt_ui", "/"),"com.nokia.bt_ui")
		#bt_dialog = self.dbus_bt_dialog.show_search_dlg("","",[""],"require")
		self.dbus_manager = self.bus.get_object("com.nokia.bt_ui", "/com/nokia/bt_ui")
		self.dbus_manager.connect_to_signal("search_result", self._device_selected)

	elif source == "reconnect":
		self.main.transition_to("reconnect_list")
		#wainting for connection

	elif source == "wait_connection":

		self.main.transition_to("wait_conn")

	elif source == "task_switcher":

		self.main.task_switcher()

    def _device_selected(self, address, name, icon, major_class, minor_class, trusted, services):
		if trusted ==1:

			self.main.current_adapter_addr = address
			self.main.current_adapter_name = name
			self.main.transition_to("confirm_conn")
		else:
			print address
			print trusted

		#if device is paired, connect, if not wait for device created

    def _device_created(self, device_path):

		device = dbus.Interface(self.bus.get_object("org.bluez", device_path),"org.bluez.Device")
		properties = device.GetProperties()
		self.client_name = properties["Name"]
		self.client_addr =  properties["Address"]
		print self.client_addr
		#try to connect here
    
