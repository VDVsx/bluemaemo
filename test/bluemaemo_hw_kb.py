#
#      bluemaemo_hw_kb.py
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

#----------------------------------------------------------------------------#
class bluemaemo_hw_kb:
#----------------------------------------------------------------------------#
	def __init__(self, main):

		self.alt = False
		self.ctrl = False
		self.fn = False
		self.shift = False
		self.main = main

	def send_hw_kb_key(self,key):
		
		try:
			if key == "Shift_L":
				self.shift = True
			
			elif key == "Control_L" or key == "Control_R":
				self.ctrl = True
			
			elif key == "Alt_L":
				self.alt = True

			elif key == "ISO_Level3_Shift":
				self.fn = True
			
			else:
			
				value = self.main.key_mapper.mapper[str(key)]
					
				if self.shift:
					self.main.connection.send_keyboard_event("02",value)
			
				elif self.alt and self.ctrl:
					self.main.connection.send_keyboard_event("05",value)
					self.ctrl = False
					self.alt = False
				
				elif self.ctrl:
					self.main.connection.send_keyboard_event("01",value)
					self.ctrl = False
				
				elif self.alt:
					self.main.connection.send_keyboard_event("04",value) 	
					self.alt = False
			
				elif str(key) == "plus" and not self.fn:

					self.main.connection.send_keyboard_event("02",value) 
			
				elif self.fn:
					modi = self.main.key_mapper.mapper["fn_m+"+str(key)]
					value2 = self.main.key_mapper.mapper["fn_k+"+str(key)]
					self.main.connection.send_keyboard_event(modi,value2) 	
			
				else:
					self.main.connection.send_keyboard_event("00",value)
		except:
			print "Key error --->>>"
