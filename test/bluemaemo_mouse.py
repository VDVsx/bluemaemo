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

    @evas.decorators.key_up_callback
    def key_up_cb( self, event ):
	self.main.connection.release_keyboard_event()
        key = event.keyname

	if key == "Shift_L":
		self.main.hw_kb.shift = False

	elif key == "ISO_Level3_Shift":
		self.main.hw_kb.fn = False
	
	elif key == "Control_L" or key == "Control_R":
		self.main.hw_kb.ctrl = False
  
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
		
		self.main.hw_kb.send_hw_kb_key(key)



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

		if self.mouse_down:
			
			if self.first_touch:

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

		if self.mouse_down:
			
			if self.first_touch:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
				
				
				if self.button_hold:
					
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
			
			if self.button_hold:
				
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

