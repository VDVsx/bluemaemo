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
class presentation(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation")

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
		
		self.main.transition_to("menu")

	elif source ==	"conf_keys":
		
		self.main.transition_to("presentation_conf")

	elif source == "previous":


		key = self.main.previous_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "next":

		key = self.main.next_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "fullscreen":

		key = self.main.fullscreen_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key
		modif, val = key_dec(self,key)
		self.main.connection.send_keyboard_event(modif,val)

#----------------------------------------------------------------------------#
class presentation_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation_conf")
	count = 0
	self.prev_key = ""
	self.next_key = ""
	self.full_key = ""
	self.no_full_key = ""
	for i in (self.main.previous_key,self.main.next_key,self.main.fullscreen_key, self.main.no_fullscreen_key):
		if len(i) > 6:
			#shift translation
			if i[0] == "s":
				text_value = self.main.key_mapper.mapper[i]
				count +=1
		elif len(i) > 5 and i[0] == "f" and i[1] == "n":
			
			val = str(i) + "+u"
			text_value = self.main.key_mapper.mapper[val]
			count +=1

		elif len(i) == 4 and i[0] == "s" and i[1] == "p":
			text_value = self.main.key_mapper.mapper[i]
			count +=1
			
		else:
			text_value = i
			count +=1
		if count == 1:
			self.prev_key = text_value
		elif count == 2:
			self.next_key = text_value
		elif count == 3:
			self.full_key = text_value
		elif count == 4:
			self.no_full_key = text_value
				
		 
	self.part_text_set("previous_key_icon", self.prev_key)
	self.part_text_set("next_key_icon", self.next_key)
	self.part_text_set("fullscreen_key_icon", self.full_key)
	self.part_text_set("no_fullscreen_key_icon", self.no_full_key)
	self.key_value = ""

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

		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("presentation")	

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		self.main.bluemaemo_conf.save_options()
		self.main.transition_to("presentation")	
	else:
		if source == "previous_key":

			self.key_value = self.part_text_get("previous_key_icon")
			self.main.key_text = self.key_value

		elif source == "next_key":

			self.key_value = self.part_text_get("next_key_icon")
			self.main.key_text = self.key_value

		elif source == "fullscreen_key":

			self.key_value = self.part_text_get("fullscreen_key_icon")
			self.main.key_text = self.key_value

		elif source == "no_fullscreen_key":

			self.key_value = self.part_text_get("no_fullscreen_key_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "presentation"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value+ "  ")
		self.main.transition_to("conf_keys")	
	

