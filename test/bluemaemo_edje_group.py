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


#-------------------------------------------------------------------------#
def mouse_position(self,x1,y1):
#-------------------------------------------------------------------------#	
	x = x1 - self.x_init
	y = y1 - self.y_init
	
	self.x_init = x1
	self.y_init = y1
			
	return x,y


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
