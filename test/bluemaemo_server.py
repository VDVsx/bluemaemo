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
#from bluemaemo_bluez_conf import *

class Connect:
	
	def __init__(self, version):

		self.input_connect = False
		self.connect = False
		self.sock_open = False
		self.client_name = None
		self.client_addr = None
		self.adapter_addr = None
		self.error = False
		self.bluez_subsystem = False
		self.quit_server = False
		self.bluez_version = version
		#self.bluez_conf = Bluez_conf()
	
		
		# Read record file
		file_read = open('service_record.xml','r')
		#file_read = open('/usr/share/bluemaemo/data/service_record.xml','r')
		xml = file_read.read()

		self.bus = dbus.SystemBus()

		if self.bluez_version == 3:

			self.input = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez/service_input'), 'org.bluez.Service')
		
			self.adapter = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')

			self.adapter_addr = self.adapter.GetAddress()
			
			input_status = self.input.IsRunning()
		

		# Check if input service is running, if yes terminate the service

		else:	
			
			#try:
			#	os.system("/etc/init.d/bluetooth stop")
			#	self.bluez_conf.check_conf()
			#except:
				#print "can't stop bluetooth services"

			#if self.bluez_conf.restart_bluez:

			#	try:
		
			#		os.system("/etc/init.d/bluetooth start")
			#		self.bluez_conf.restore_options()
			#		print "Bluez configurations restored"
			#		self.bluez_subsystem = True
			#	except:
			#		print "can't start bluetooth services"
			#else:
			#	try:
			#		os.system("/etc/init.d/bluetooth start")
			#	except:
			#		print "can't start bluetooth services"
					
				
                        input_status = False

                        self.input_connect = False

		if input_status:
			
			try:
				cenas = self.input.Stop()
				self.input_connect = True
				print "--> BlueZ input service stopped"

			except:
				
			       self.input_connect = False
			       print "Error in d-bus system - input service"
	

		else:
			
			self.input_connect = False
		try:
			
			if self.bluez_version == 3:
				# Add service record to the BlueZ database
				self.database = dbus.Interface(self.bus.get_object('org.bluez', '/org/bluez'),'org.bluez.Database')
				self.handle = self.database.AddServiceRecordFromXML(xml)
				print "Info: SDP record added"

			else:

				# Add service record to the BlueZ database
				manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),"org.bluez.Manager")
		
				self.path = manager.DefaultAdapter()
				self.adapter = dbus.Interface(self.bus.get_object("org.bluez", self.path),"org.bluez.Adapter")
				properties = self.adapter.GetProperties()
				self.adapter_addr = properties["Address"]
				self.service = dbus.Interface(self.bus.get_object("org.bluez", self.path),"org.bluez.Service")
				self.handle = self.service.AddRecord(xml)
				print "Info: SDP record added"
				#self.adapter.connect_to_signal("DeviceCreated", self._device_created)
				
		except:
			print "Error in d-bus system - database"

	#def _device_created(self, device_path):

	#	device = dbus.Interface(self.bus.get_object("org.bluez", device_path),"org.bluez.Device")
	#	properties = device.GetProperties()
	#	self.client_name = properties["Name"]
	#	self.client_addr =  properties["Address"]
	#	print self.client_addr
	
	def get_device_info(self,addr):

		path = self.adapter.FindDevice(addr)
		device = dbus.Interface(self.bus.get_object("org.bluez", path),"org.bluez.Device")
		properties = device.GetProperties()
		self.client_name = properties["Name"]
		self.client_addr =  properties["Address"]
		print self.client_addr
	
	def start_connection(self,addr, name):	
		
		self.deamon = start_deamon(self,addr, name)
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

	def send_multiple_keyboard_event(self,modifier,key, key2):
		
		try:
			mod = int(modifier)
			key = int(key)
			n = hidserver.send_multiple_key(mod,key, key2)
			if n < 0:
				self.connect = False
				print "Disconnected"
				
		except:
			self.connect = False
			print "Disconnected"

	def release_multiple_keyboard_event(self, key):

		try:	
			n = hidserver.release_multiple_key(key)

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

			if self.bluez_version == 3:
				self.database.RemoveServiceRecord(self.handle)

				if self.input_connect:
					self.input.Start()
					print "--> BlueZ input service started"

			else: 

				self.service.RemoveRecord(self.handle)
				print "Info: SDP record removed"
				# Restore initial input service condition

				if self.bluez_subsystem:
					try:
						os.system("/etc/init.d/bluetooth stop")
					except:
						print "can't stop bluetooth services"

					try:
			
						os.system("/etc/init.d/bluetooth start")
					except:
						print "can't start bluetooth services"

			if not self.connect:

				#hidserver.quit()
				n = hidserver.quit_server()

			else:
				n = hidserver.quit_server()
				if n < 0:
					self.connect = False
					print "Error closing sockets"
		except:
			self.connect = False
			print "Error closing sockets"

		self.quit_server = True
		print "Connection terminated"
			
				
class start_deamon(Thread):
	
	def __init__(self,bluemaemo,addr, name):
		
		self.bluemaemo = bluemaemo
		self.addr = addr
		self.name = name
		self.state = 1
		Thread.__init__(self)
		print "initializing daemon ..."
		
	def run(self):

		try:

			if self.addr==1:

				hidserver.init_hidserver()
			else:
				
				self.state = hidserver.reConnect(self.bluemaemo.adapter_addr,self.addr)
				self.bluemaemo.client_addr = self.addr
				self.bluemaemo.client_name = self.name
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
				if self.bluemaemo.bluez_version == 3:
					try:		
					
						input_status = self.bluemaemo.adapter.ListConnections()
						print input_status
						print "You are connect to the address: " + str(input_status[-1])
						client_name = self.bluemaemo.adapter.GetRemoteName(input_status[-1])
						self.bluemaemo.client_name = str(client_name)
						self.bluemaemo.client_addr = str(input_status[-1])
						print "connected to: " + str(client_name)

					except:
			
						self.bluemaemo.error = True
						print 'ERROR: Bluetooth is off'

				else:
					
					try:	
						if self.addr==1:

							self.bluemaemo.client_addr = hidserver.get_client_addr()
						else:
							self.bluemaemo.client_addr = self.addr
						try:
							self.bluemaemo.get_device_info(self.bluemaemo.client_addr)

						except:
							print "Error: Can't get remote device information"
							print self.bluemaemo.connect
							print self.bluemaemo.error

						print self.bluemaemo.client_addr
						if self.bluemaemo.client_addr != None:
							print "You are connect to the address: " + self.bluemaemo.client_addr
							print "connected to: " + self.bluemaemo.client_name
						else:

							print "Error: Can't get remote device information"
							print self.bluemaemo.connect
							print self.bluemaemo.error
					except:
			
						self.bluemaemo.error = True
						print 'Error: Bluetooth is off'
		except:
			
			print "Exit"
