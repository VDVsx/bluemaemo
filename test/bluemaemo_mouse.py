#
#      bluemaemo_mouse.py
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


import time
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
class mouse_ui(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "mouse_ui")
        self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True
        self.button_hold = False
	self.scroll_pos = 0
	self.tape_mouse_area = 0
	self.main.bluemaemo_conf.fullscreen
	self.alt = False
        self.ctrl = False
	self.fn = False
	self.shift = False

    
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
  
    #mouse
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

	if key == "F7" or key == "F8":

		self.button_hold = True
		self.signal_emit("hold_pressed", "")

	elif key == "F6":

		if self.main.bluemaemo_conf.fullscreen == "Yes":
			
			self.main.bluemaemo_conf.fullscreen = "No"
			self.main.window.fullscreen = False

		elif self.main.bluemaemo_conf.fullscreen == "No":
			
			self.main.bluemaemo_conf.fullscreen = "Yes"
			self.main.window.fullscreen = True

	elif key == "Escape":

		self.main.transition_to("menu")

	else:
		
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
			
				if self.shift == True:
					self.main.connection.send_keyboard_event("02",value)
			
				elif self.alt == True and self.ctrl == True:
					self.main.connection.send_keyboard_event("05",value)
					self.ctrl = False
					self.alt = False
				
				elif self.ctrl == True:
					self.main.connection.send_keyboard_event("01",value)
					self.ctrl = False
				
				elif self.alt == True:
					self.main.connection.send_keyboard_event("04",value) 	
					self.alt = False
			
				elif str(key) == "plus" and self.fn == False:

					self.main.connection.send_keyboard_event("02",value) 
			
				elif self.fn == True:
					modi = self.main.key_mapper.mapper["fn_m+"+str(key)]
					value2 = self.main.key_mapper.mapper["fn_k+"+str(key)]
					self.main.connection.send_keyboard_event(modi,value2) 	
			
				else:
					self.main.connection.send_keyboard_event("00",value)
		except:
			print "Key error --->>>"
				


    @evas.decorators.key_up_callback
    def key_up_cb( self, event ):
        key = event.keyname
	
	if key == "F7" or key == "F8":
		self.button_hold = False
		self.signal_emit("hold_released", "")

	elif key == "Shift_L":
		self.shift = False

	elif key == "ISO_Level3_Shift":
		self.fn = False

	elif key == "Escape" or key == "F6":
		pass

	else:
		self.main.connection.release_keyboard_event()


    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True
		self.tape_mouse_area = time.time()

    		

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_mouse_up(self, emission, source):

		if source == "mouse_area":
			tape_time = time.time() - self.tape_mouse_area
			
			if tape_time < 0.2:

				self.main.connection.send_mouse_event(1,0,0,0)
				self.main.connection.send_mouse_event(0,0,0,0)
				

		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0
		

    @edje.decorators.signal_callback("mouse_over_scroll", "*") 
    def on_mouse_over_scroll(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:

				tmp,self.scroll_pos = self.main.canvas.pointer_canvas_xy			
				self.first_touch = False
			else:

				tmp,y_scroll = self.main.canvas.pointer_canvas_xy	

				if y_scroll > self.scroll_pos + self.main.scroll:

					self.scroll_pos = y_scroll
					self.main.connection.send_mouse_event(0,0,0,255)
					
					

				elif y_scroll < self.scroll_pos - self.main.scroll:

					self.scroll_pos = y_scroll
					self.main.connection.send_mouse_event(0,0,0,1)
					
					
				else:

					pass

		else:

			pass

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
				
				
				if self.button_hold == True:
					
					mov = "02:01:" + str(x1) + ":" + str(y1) + ":000"
					
					self.main.connection.send_mouse_event(01,x1,y1,00)
					
				else:	
					
					mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
					self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	
			
   
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_mouse_click(self, emission, source):
    	
		
		if source == "bt_right":
			
			self.main.connection.send_mouse_event(2,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)			
			
		elif source == "bt_left":
			
			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)	
			
		elif source == "bt_hold":
			
			if self.button_hold == True:
				
				self.button_hold = False
				
				self.signal_emit("hold_released", "")
				self.main.connection.send_mouse_event(0,0,0,0)	

				
			else:
				
				self.button_hold = True
				self.signal_emit("hold_pressed", "")
				
		elif source == "bt_middle":
			
			self.main.connection.send_mouse_event(4,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)				
			
		elif source == "back":
	
			print self.main.previous_group
			self.main.transition_to("menu")
				
		else:
				
			pass

