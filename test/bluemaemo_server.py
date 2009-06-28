#
#      bluemaemo_server.py
#
#      Copyright 2008 - 2009 	Valerio Valerio <vdv100@gmail.com>
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
import time
import os
import socket
import sys
from threading import Thread
import hidserver
from bluemaemo_known_devices_conf import *


class Connect:
	
	def __init__(self):

		self.input_connect = False
		self.connect = False
		self.sock_open = False
		self.client_name = None
		self.client_addr = None
		self.adapter_addr = None
		self.error = False
		self.bluez_subsystem = False
		self.quit_server = False
		self.known_dev = None
		self.devices_conf = bluemaemo_known_devices()
		
		
		self.bus = dbus.SystemBus()
		self.input = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez/service_input'), 'org.bluez.Service')
		
		self.adapter = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')

		self.adapter_addr = self.adapter.GetAddress()
		print self.adapter_addr
		
		# Read record file
		file_read = open('service_record.xml','r')
		#file_read = open('/usr/share/bluemaemo/data/service_record.xml','r')
		xml = file_read.read()

		# Check if input service is running, if yes terminate the service

		try:

                       input_status = self.input.IsRunning()

                except:
		       print "ERROR: isRunning d-bus call not present"

		       try:
				os.system("/etc/init.d/bluetooth stop")
		       except:
				print "can't stop bluetooth services"
		       try:
				os.system("mv /usr/lib/bluetooth/plugins/libinput.so /usr/lib/bluetooth/plugins/libinput.so_back")
		       except:
				print "can't move input plugin"

		       try:
			
				os.system("/etc/init.d/bluetooth start")
		       except:
				print "can't start bluetooth services"

		       try:
				os.system("mv /usr/lib/bluetooth/plugins/libinput.so_back /usr/lib/bluetooth/plugins/libinput.so")
				self.bluez_subsystem = True
		       except:
				print "can't move input plugin"
			
				
				
                       input_status = False

                       self.input_connect = False

		if input_status:
			
			try:
				cenas = self.input.Stop()
				self.input_connect = True
				print "--> BlueZ input service stopped"

			except:

			       try:
					os.system("/etc/init.d/bluetooth stop")
		       	       except:
					print "can't stop bluetooth services"
			       try:
					os.system("mv /usr/lib/bluetooth/plugins/libinput.so /usr/lib/bluetooth/plugins/libinput.so_back")
			       except:
					print "can't move input plugin"

			       try:
			
					os.system("/etc/init.d/bluetooth start")
			       except:
					print "can't start bluetooth services"

			       try:
					os.system("mv /usr/lib/bluetooth/plugins/libinput.so_back /usr/lib/bluetooth/plugins/libinput.so")
					self.bluez_subsystem = True
			       except:
					print "can't move input plugin"
				
			       self.input_connect = False

		else:
			
			self.input_connect = False
		try:
			
			
			# Add service record to the BlueZ database
			self.database = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez'),'org.bluez.Database')
			self.handle = self.database.AddServiceRecordFromXML(xml)

		except:
			print "Error in d-bus system"
	
	
	def start_connection(self,addr):	
		
		self.deamon = start_deamon(self,addr)
		self.deamon.start()

	
	def send_mouse_event(self,btn,mov_x,mov_y, scroll):
		
		try:
			
			n = hidserver.send_mouse_ev(btn,mov_x,mov_y,scroll)
			if n < 0:
				self.connect = False
				print "Disconnected"
		except:
			self.connect = False
			print "Disconnected"
		
	def send_keyboard_event(self,modifier,key):
		
		try:
			mod = int(modifier)
			key = int(key)
			n = hidserver.send_key(mod,key)
			if n < 0:
				self.connect = False
				print "Disconnected"
				
		except:
			self.connect = False
			print "Disconnected"

	def release_keyboard_event(self):

		try:	
			n = hidserver.release_key()

		except:
			self.connect = False
			print "Disconnected"
			
	def send_event(self, event):
		
		try:
			
			self.sock.send(event)
			
		except:
			self.connect = False
			print "disconnected"

			
	def terminate_connection(self):
		
		try:
			if not self.connect:
				hidserver.quit()
				n = hidserver.quit_server()
				print "killed"
			else:
				n = hidserver.quit_server()
				if n < 0:
					self.connect = False
					print "Error closing sockets"
		except:
			self.connect = False
			print "Error closing sockets"

		self.database.RemoveServiceRecord(self.handle)

		# Restore initial input service condition
		if self.input_connect:
			self.input.Start()
			print "--> BlueZ input service started"

		if self.bluez_subsystem:

			try:
				os.system("/etc/init.d/bluetooth stop")
			except:
				print "can't stop bluetooth services"

			try:
			
				os.system("/etc/init.d/bluetooth start")
			except:
				print "can't start bluetooth services"

		self.quit_server = True
		print "Connection terminated"
			
				
class start_deamon(Thread):
	
	def __init__(self,bluemaemo,addr):
		
		self.bluemaemo = bluemaemo
		self.addr = addr
		self.state = 1
		Thread.__init__(self)
		print "initializing daemon ..."
		
	def run(self):
		
		try:
			if self.addr==1:

				hidserver.init_hidserver()
			else:
				
				self.state = hidserver.reConnect(self.bluemaemo.adapter_addr,self.addr)
				#hidserver.reConnect("00:1D:6E:9D:42:9C","00:21:4F:57:93:C8")
		
			while not self.bluemaemo.connect  and not self.bluemaemo.error:
				time.sleep(1)
				n = hidserver.connec_state()
				print "Waiting for a connection..."
				if n == 1:
					self.bluemaemo.connect = True

				elif self.bluemaemo.quit_server:
					print "Exit"
					bluemaemo.shutdown()

				elif self.state == 0:
					print "error reconneting"
					self.bluemaemo.error = True

				elif n == 0:
					pass
					
				else:
					print "Error"
					self.bluemaemo.error = True

			if self.bluemaemo.error:
				pass
			else:
				try:		
					
					input_status = self.bluemaemo.adapter.ListConnections()
					print input_status
					print "You are connect to the address: " + str(input_status[-1])
					client_name = self.bluemaemo.adapter.GetRemoteName(input_status[-1])
					self.bluemaemo.client_name = str(client_name)
					self.bluemaemo.client_addr = str(input_status[-1])
					if self.bluemaemo.devices_conf.known_devices_list.has_key(self.bluemaemo.client_addr):
						print "device already existent"
					else:
						self.bluemaemo.devices_conf.add_new_dev(self.bluemaemo.client_addr +'='+ self.bluemaemo.client_name + "\n")
						self.bluemaemo.devices_conf.known_devices_list[self.bluemaemo.client_addr] = self.bluemaemo.client_name
					print "connected to: " + str(client_name)
				except:
			
					self.bluemaemo.error = True
					print 'ERROR: Bluetooth is off'
		except:
			
			print "Exit"
