#
#      bluemaemo_edje_group.py
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
import os


edjepaths = "bluemaemo.edj themes/bluemaemo.edj /usr/share/bluemaemo/themes/bluemaemo.edj".split()

for i in edjepaths:
    if os.path.exists( i ):
       global edjepath
       edjepath = i
       break
else:
    raise Exception( "bluemaemo.edj not found. looked in %s" % edjepaths )

#aux functions

#-------------------------------------------------------------------------#
def mouse_position(self,x1,y1):
#-------------------------------------------------------------------------#	
	x = x1 - self.x_init
	y = y1 - self.y_init
	
	self.x_init = x1
	self.y_init = y1
			
	return x,y


#-------------------------------------------------------------------------#
def key_dec(self,key):
#-------------------------------------------------------------------------#
	self.shift = False
	self.ctrl = False
	self.alt = False
	self.win = False
	self.fn = False
	self.sp = False
	self.modif = ""
	self.val = ""
	if len(key) < 4:
		value = self.main.key_mapper.mapper[str(key)]
		return "00", value

	else:

		key_split = key.split("+")
		
		for i in key_split:
			
			if i == "shift":
				self.shift = True
			
			elif i == "ctrl":
				self.ctrl = True
			
			elif i == "alt":
				self.alt = True
			elif i == "win":
				self.win = True

			elif i == "fn_k":
				self.fn = True

			elif i == "sp":
				self.sp = True
			
			else:
			
				if self.shift == True:

					self.modif = "02"
					self.shift = False
					self.val = self.main.key_mapper.mapper[str(i)]

				if self.win == True:

					self.modif = "08"
					self.win = False
					self.val = self.main.key_mapper.mapper[str(i)]

				elif self.ctrl == True and self.alt == True:

					self.ctrl = False
					self.alt = False
					self.modif = "05"
					self.val = self.main.key_mapper.mapper[str(i)]
				
				elif self.ctrl == True:

					
					self.ctrl = False
					self.modif = "01"
					self.val = self.main.key_mapper.mapper[str(i)]
				
				elif self.alt == True:
					
					self.alt = False
					self.modif = "04"
					self.val = self.main.key_mapper.mapper[str(i)]

				elif self.fn == True:

					self.fn = False
					self.modif = self.main.key_mapper.mapper["fn_m+"+str(i)]
					self.val = self.main.key_mapper.mapper["fn_k+"+str(i)]

				elif self.sp == True:

					self.sp = False
					self.val = self.main.key_mapper.mapper[str(i)+ "_k"]
					self.modif = self.main.key_mapper.mapper[str(i)+ "_m"]

				else:	
					self.modif = "00"
					self.val = self.main.key_mapper.mapper[str(i)]
	
	return self.modif,self.val


#----------------------------------------------------------------------------#
class edje_group(edje.Edje):
#----------------------------------------------------------------------------#
    def __init__(self, main, group, parent_name="main"):
        self.main = main
        self.parent_name = parent_name
        global edjepath
        f = edjepath
        try:
            edje.Edje.__init__(self, self.main.evas_canvas.evas_obj.evas, file=f, group=group)
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (f, e))
        self.size = self.main.evas_canvas.evas_obj.evas.size

    def onShow( self ):
        pass

    def onHide( self ):
        pass

    @edje.decorators.signal_callback("mouse,clicked,1", "button_bottom_right")
    def on_edje_signal_button_bottom_right_pressed(self, emission, source):
        self.main.transition_to(self.parent_name)

    @edje.decorators.signal_callback("finished_transition", "*")
    def on_edje_signal_finished_transition(self, emission, source):
        self.main.transition_finished()
