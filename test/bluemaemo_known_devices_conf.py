#
#      bluemaemo_known_devices_conf.py
#
#      Copyright 2008-2009 	Valerio Valerio <vdv100@gmail.com>
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



import ConfigParser
import os
import os.path

defaultsfile = "/etc/bluemaemo/known_devices.cfg"

class bluemaemo_known_devices:

	def __init__(self):
		try:
			f = open(defaultsfile)
			self.known_devices_list = {}
			self.empty = True
			for line in f:
				b = line.split('=')
				if b[0] == '\n':
					pass
				else:
					name = b[1].split('\n')
					self.known_devices_list[b[0]] = name[0]
					self.empty = False
			f.close()
		except:
			print "Creating \'" + defaultsfile + "\'..."
			self.empty = True
			f= open("/etc/bluemaemo/known_devices.cfg","w")
			f.close()

	def add_new_dev(self,value):
		
		f = open(defaultsfile,'a')
		f.write(value)
		f.close()
		print "Device added"

		

