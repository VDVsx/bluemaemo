#
#      bluemaemo_about.py
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
class about(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "about")
	self.part_text_set( "menu_title", "About" )
	self.part_text_set("label_version","BlueMaemo v.0.3.8")
	self.part_text_set("label_version_shadow","BlueMaemo v.0.3.8")
	self.part_text_set("label_programming","Programming:")
	self.part_text_set("label_programming_shadow","Programming:")
	self.part_text_set("label_visual","Visual design:")
	self.part_text_set("label_visual_shadow","Visual design:")
	self.part_text_set("label_programming_name","Valerio Valerio")
	self.part_text_set("label_programming_name_shadow","Valerio Valerio")
	self.part_text_set("label_visual_name","Andrew Zhilin")
	self.part_text_set("label_visual_name_shadow","Andrew Zhilin")
	self.part_text_set("label_programming_email","vdv100@gmail.com")
	self.part_text_set("label_programming_email_shadow","vdv100@gmail.com")
	self.part_text_set("label_visual_email","drew.zhilin@gmail.com")
	self.part_text_set("label_visual_email_shadow","drew.zhilin@gmail.com")
	

    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
     
    @evas.decorators.key_down_callback
    def key_down_cb( self, event ):
        key = event.keyname

	if key == "Escape":

		self.main.transition_to("menu")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source == "task_switcher":

		self.main.task_switcher()

