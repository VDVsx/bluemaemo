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
class settings(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "settings")
        self.part_text_set("fullscreen_option",str(self.main.bluemaemo_conf.fullscreen))
	self.part_text_set("scroll_option", str(self.main.bluemaemo_conf.scroll))
	self.scroll_value = int(self.main.bluemaemo_conf.scroll)
	self.fscreen_option = str(self.main.bluemaemo_conf.fullscreen)

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

	elif key == "Escape":

		self.main.transition_to("menu")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	 

	if source == "back":
		
		self.main.bluemaemo_conf.set_option("user","fullscreen",self.fscreen_option)
		self.main.bluemaemo_conf.set_option("user","scroll",self.scroll_value)
		self.main.bluemaemo_conf.save_options()
		self.main.scroll = self.scroll_value
		self.main.transition_to("menu")

	elif source == "fullscreen_option":
		
		if self.fscreen_option == "Yes":
			
			self.part_text_set("fullscreen_option","No")
			self.fscreen_option = "No"
			self.main.window.fullscreen = False

		elif self.fscreen_option == "No":
			
			self.part_text_set("fullscreen_option","Yes")
			self.fscreen_option = "Yes"
			self.main.window.fullscreen = True

	elif source == "scroll_right_icon":
		
		if self.scroll_value < 9:
			self.scroll_value += 1
			self.part_text_set("scroll_option", str(self.scroll_value))
	
	elif source == "scroll_left_icon":
		
		if self.scroll_value >= 1:
			self.scroll_value -= 1
			self.part_text_set("scroll_option", str(self.scroll_value))

