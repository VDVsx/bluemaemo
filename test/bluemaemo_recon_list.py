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
from bluemaemo_edje_group import *


(SCROLL_PAGE_FORWARD,
SCROLL_PAGE_BACKWARD,
SCROLL_STEP_FORWARD,
SCROLL_STEP_BACKWARD,
SCROLL_PIXELS_DOWN,
SCROLL_PIXELS_UP) = range(6)

IMAGE_FOLDER = "/usr/share/bluemaemo/images"

#----------------------------------------------------------------------------#
class rec_list(edje_group):
#----------------------------------------------------------------------------#




	def __init__(self,main):

        	edje_group.__init__(self, main, "rec_list")
		items = []
		d = os.path.dirname(sys.argv[0]) #sub pelo image folder
		self.main = main

		for i in xrange(5):
			c = (i % 8) + 1
			items.append(("Item %d" % i,"00:1D:6E:9D:42:9C", os.path.join(d, "connection_icon.png")))
		
		#if
		#items.append(("Known devices list empty","", os.path.join(d, "connection_icon.png")))
		self.list_empty = False
		self.evas_obj = main.canvas
		self.list_obj = KineticList(self.evas_obj,"bluemaemo.edj",self,main,item_height=150)
		self.list_obj.freeze()
		for i in items:
	    		self.list_obj.row_add(i[0], i[1], i[2])
		self.list_obj.thaw()

		self.part_swallow("list", self.list_obj);

	def visible(self):
		
		self.signal_emit("show_list","")

	def invisible(self):

		self.signal_emit("hide_list","")

	def onShow( self ):
		self.focus = True
		if self.list_empty:
			ecore.timer_add(2.0,self.main.transition_to,"menu") #mudar aqui isto	
    

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
	
		elif key == "Escape":
			##alterar para ir para o 1 ecra
			self.main.transition_to("menu")

	#def construct(self,evas):

	


class ResizableImage(evas.SmartObject):
    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas)
        self.image_object = evas.Image(ecanvas)
        self.member_add(self.image_object)

    def file_set(self, filename):
        self.image_object.file_set(filename)
        self.image_object.show()

    def resize(self, w, h):
        self.image_object.size = (w, h)
        self.image_object.fill_set(0, 0, w, h)

    def color_set(self, r, g, b, a):
        self.image_object.color_set(r, g, b, a)

    def show(self):
	pass
	
    def hide(self):
	self.image_object.hide()


class KineticList(evas.SmartObject):
    (
        SCROLL_PAGE_FORWARD,
        SCROLL_PAGE_BACKWARD,
        SCROLL_STEP_FORWARD,
        SCROLL_STEP_BACKWARD,
        SCROLL_PIXELS_DOWN,
        SCROLL_PIXELS_UP
    ) = range(6)


    def __init__(self, ecanvas, file, edje_class, main, item_width=-1, item_height=-1):
        
        evas.SmartObject.__init__(self, ecanvas)
	self.edje_class = edje_class
	self.main = main
        self.elements = []
        self.objects = []
        self.image_objects = []
        self.w = 12
        self.h = 12

        self.realized = False

        self.top_pos = 0
        self.last_top_pos = 0
        self.last_start_row = -1

        self.canvas = ecanvas
        self.edje_file = file

        self.row_width = item_width
        self.row_height = item_height

        self.__manage_objects()

        self.mouse_down = False
        self.last_y_pos = 0
        self.start_pos = 0
        self.mouse_moved = False
        self.continue_scrolling = False
        self.is_scrolling = False
        self.do_freeze = False

    def onShow(self):
	self.focus = True
    

    def onHide(self):
	self.focus = False

    def hide(self):
	self.edje_class.hide()
	for i in self.image_objects:
		i.hide()


    def freeze(self):
        self.do_freeze = True

    def thaw(self):
        self.do_freeze = False
        if self.realized:
            self.__update_variables_after_new_elements()
            self.__update_screen()

    def scroll(self, scroll_type, amount=1):
        self.continue_scrolling = False

        if scroll_type == self.SCROLL_PAGE_FORWARD:
            self.top_pos += amount * self.row_height * self.max_visible_rows
        elif scroll_type == self.SCROLL_PAGE_BACKWARD:
            self.top_pos -= amount * self.row_height * self.max_visible_rows
        elif scroll_type == self.SCROLL_STEP_FORWARD:
            self.top_pos += amount * self.row_height
        elif scroll_type == self.SCROLL_STEP_BACKWARD:
            self.top_pos -= amount * self.row_height
        elif scroll_type == self.SCROLL_PIXELS_DOWN:
            self.top_pos += amount
        elif scroll_type == self.SCROLL_PIXELS_UP:
            self.top_pos -= amount
        else:
            return

        self.__update_screen()

    def __on_mouse_clicked(self, edje_obj, emission, source, data=None):
        
        edje_obj.signal_emit("select_adap", "")
	if edje_obj.part_text_get("adap_addr") == "":
		ecore.timer_add(1.0,self.main.transition_to,"menu") #mudar aqui isto
	else:
		self.main.current_adapter_name = edje_obj.part_text_get("adap_name")
		self.main.current_adapter_addr =  edje_obj.part_text_get("adap_addr")
		ecore.timer_add(1.0,self.main.transition_to,"confirm_conn")

    def __on_mouse_move(self, edje_obj, emission, source, data=None):
        if self.mouse_down:
            x_pos, y_pos = self.canvas.pointer_canvas_xy
            diff = int(self.last_y_pos - y_pos)

            if diff == 0:
                return

            self.mouse_moved = True

            # Reset the data if the direction of the mouse move is changed
            if self.last_diff != -1 and (diff < 0) != (self.last_diff < 0):
                self.last_y_pos = y_pos
                self.start_pos = y_pos
                self.start_time = time.time()

            self.last_diff = diff
            self.top_pos += diff

            self.last_y_pos = y_pos
            self.__update_screen()
            self.last_update_time = time.time()

    def __on_mouse_down(self, edje_obj, emission, source, data=None):
        if not self.is_scrolling:
            self.mouse_moved = False

        self.continue_scrolling = False
        self.mouse_down = True

        x_pos, y_pos = self.canvas.pointer_canvas_xy

        self.last_diff = -1
        self.last_y_pos = y_pos
        self.start_pos = y_pos
        self.start_time = time.time()
        self.last_update_time = time.time()

    def __on_mouse_up(self, edje_obj, emission, source, data=None):
        if self.mouse_down:
            self.mouse_down = False

            x_pos, end_pos = self.canvas.pointer_canvas_xy

            if not self.mouse_moved and not self.is_scrolling:
                self.__on_mouse_clicked(edje_obj, emission, source)
                return

            self.mouse_moved = False
            self.is_scrolling = False

            # do not scroll automatically if the finger was paused
            if time.time() - self.last_update_time > 0.1:
                return

            end_time = time.time()

            pos_diff =  end_pos - self.start_pos
            time_diff = end_time - self.start_time

            self.pixel_per_sec = pos_diff / time_diff
            self.continue_scrolling = True
            self.__do_scroll()

    def __do_scroll(self):
        self.is_scrolling = True

        if self.continue_scrolling == False:
            return

        diff = int(self.pixel_per_sec / 10)

        if abs(self.pixel_per_sec) - diff <= self.row_height:
            offset = self.top_pos % self.row_height

            if offset >= self.row_height / 2:
                self.sign = 1
                offset = self.row_height - offset
            else:
                self.sign = -1

            self.pixels_left = offset
            self.__do_magnetic_scroll()

            return

        if diff != 0:
            self.top_pos -= diff
            self.pixel_per_sec -= self.pixel_per_sec / 10
            self.__update_screen()

        ecore.timer_add(0.02, self.__do_scroll)

    def __do_magnetic_scroll(self):
        if self.pixels_left <= 0 or abs(self.pixel_per_sec) < 1:
            self.mouse_moved = False
            self.is_scrolling = False
            return

        self.pixel_per_sec -= (self.pixel_per_sec / 10)

        pixels_to_substract = int(abs(self.pixel_per_sec / 10))
        if abs(pixels_to_substract) < 1:
            pixels_to_substract = 1

        if self.pixels_left - pixels_to_substract > 0:
            self.pixels_left -= pixels_to_substract
            self.top_pos += self.sign * pixels_to_substract
        else:
            self.top_pos += self.sign * self.pixels_left
            self.pixels_left = 0

        self.__update_screen()
        ecore.timer_add(0.1, self.__do_magnetic_scroll)

    def row_add(self, label,addr, image):
        self.elements.append((label, addr, image))

        if not self.do_freeze:
            self.__update_variables_after_new_elements()
            self.__update_screen()

    def __manage_objects(self):
        remain = (self.h % self.row_height) > 1
        needed_objects = ((self.h / self.row_height) + 1 + remain) * (self.w / self.row_width)
        current_objects = len(self.objects)

        if current_objects < needed_objects:
            for i in range(current_objects, needed_objects):
                obj = edje.Edje(self.canvas);
                obj.file_set(self.edje_file, "list_item");

                obj.signal_callback_add("mouse,move", "*",
                                        self.__on_mouse_move)
                obj.signal_callback_add("mouse,down,1", "*",
                                        self.__on_mouse_down)
                obj.signal_callback_add("mouse,up,1", "*",
                                        self.__on_mouse_up)

                obj.size = (self.row_width, self.row_height)
                obj.clip = self
                self.objects.append(obj)

                image_obj = ResizableImage(self.canvas)
                image_obj.size = (100, 75)
                obj.part_swallow("thumbnail", image_obj);
                self.image_objects.append(image_obj)

        elif needed_objects < current_objects:
            for i in range(needed_objects, current_objects):
                pass # Make this work, it throws exception that makes
                     # things stop working properly
                #del self.objects[i]

    def __update_variables_after_resize(self):
        self.max_visible_rows = (self.h / self.row_height) + 1
        self.max_horiz_elements = (self.w / self.row_width)
        self.max_visible_elements = self.max_visible_rows * \
                                    self.max_horiz_elements

        # Invalidate variable in order to repaint all rows
        # Some might not have been painted before (Didn't
        # fit on the screen
        self.last_start_row = -1

        self.__update_variables_after_new_elements()

    def __update_variables_after_new_elements(self):
        if not self.realized:
            return

        self.min_pos = 0
        remainer1 = (len(self.elements) % self.max_horiz_elements) > 0
        remainer2 = (self.h % self.row_height) > 0
        self.row_amount = (len(self.elements) / self.max_horiz_elements) + \
                          remainer1 + remainer2
        self.max_pos = self.row_height * \
                       (self.row_amount - self.max_visible_rows + 1)

    def __update_screen(self):
        remainer = (self.h % self.row_height) > 0
        row_offset = (self.top_pos / self.row_height)
        pixel_offset = - (self.top_pos % self.row_height)
        start_row = row_offset
        end_row = self.max_visible_rows + row_offset + remainer

        SCROLL_DOWN = self.top_pos > self.last_top_pos
        SCROLL_UP = self.top_pos < self.last_top_pos

        # Let's not move over the last element
        if SCROLL_DOWN and self.last_top_pos >= self.max_pos:
            self.top_pos = self.max_pos
            self.last_top_pos = self.top_pos
            self.continue_scrolling = False
            return

        # Let's not move over the first element
        if SCROLL_UP and self.last_top_pos <= self.min_pos:
            self.top_pos = self.min_pos
            self.last_top_pos = self.top_pos
            self.continue_scrolling = False
            return

        # Overflow scrolling down
        if SCROLL_DOWN and end_row > self.row_amount:
            offset = end_row - self.row_amount
            end_row -= offset
            start_row -= offset
            row_offset -= offset - 1
            self.top_pos = self.max_pos
            pixel_offset = 0

        # Overflow scrolling up
        if SCROLL_UP and start_row < 0:
            self.top_pos = self.min_pos
            end_row -= start_row
            start_row = 0
            row_offset = 0
            pixel_offset = 0

        self.last_top_pos = self.top_pos

        if start_row != self.last_start_row:
            for i in range(0, len(self.objects)):
                self.objects[i].hide()

        for i in range(start_row, end_row):
            row_iter = i - start_row

            for k in range(self.max_horiz_elements):
                obj_iter = row_iter * self.max_horiz_elements + k
                data_iter = i * self.max_horiz_elements + k

                try:
                    label, addr, image = self.elements[data_iter]
                except Exception, e:
                    break;

                offset = (self.w %
                          (self.row_width * self.max_horiz_elements)) / 2
                x = self.row_width * k + self.top_left[0] + offset
                y = self.top_left[1] + self.row_height * (i - row_offset) - \
                    5 + pixel_offset

                self.objects[obj_iter].move(x, y)

                if start_row != self.last_start_row:
                    self.image_objects[obj_iter].file_set(image)
                    self.objects[obj_iter].part_text_set("adap_name", label)
		    self.objects[obj_iter].part_text_set("adap_addr", addr)
                    self.objects[obj_iter].show()

        self.last_start_row = start_row

    def resize(self, w, h):
        if self.row_width == -1 or self.row_width == self.w:
            self.row_width = w

        if self.row_height == -1 or self.row_height == self.h:
            self.row_height = h

        self.w = w
        self.h = h

        self.__manage_objects()

        for obj in self.objects:
            obj.size = (self.row_width, self.row_height)

        self.realized = True
        self.__update_variables_after_resize()
        self.__update_screen()

    def show(self):
	pass



        





