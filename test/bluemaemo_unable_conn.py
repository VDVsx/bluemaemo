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
class unable_conn(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "unable_conn")
        
	self.part_text_set("label_connect","Unable to Connect to")
	self.part_text_set("label_name", "1234 ")

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

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):

	if source == "quit" or source == "no_option" :

		ecore.main_loop_quit()

	if source == "yes_option":

		self.main.power_on_bt()
		self.main.bluetooth_obj = True
		self.main.transition_to("main")


