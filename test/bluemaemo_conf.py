#
#      bluemaemo_conf.py
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



import ConfigParser
import ecore
import os
import os.path

defaultsfile = "/etc/bluemaemo/bluemaemo.cfg"

class bluemaemo_conf:

	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		try:
			self.config.readfp(open(defaultsfile))
			version = self.config.get("version", "version")

		except:
			os.system("mkdir /etc/bluemaemo/")
			os.system("cp /usr/share/bluemaemo/data/bluemaemo.cfg /etc/bluemaemo/")
			self.config.readfp(open(defaultsfile))
		try:
			#settings
			self.scroll = self.config.get("user","scroll")
			self.firsttime = self.config.get("user","firsttime")
			self.autoconnect = self.config.get("user","autoconnect")
			#presentation profile
			self.previous_key = self.config.get("presentation","previous_key")
			self.next_key = self.config.get("presentation","next_key")
			self.fullscreen_key = self.config.get("presentation","fullscreen_key")
			self.no_fullscreen_key = self.config.get("presentation","no_fullscreen_key")
			#multimedia profile
			self.play_key = self.config.get("multimedia","play_key")
			self.pause_key = self.config.get("multimedia","pause_key")
			self.stop_key = self.config.get("multimedia","stop_key")
			self.forward_key = self.config.get("multimedia","forward_key")
			self.rewind_key = self.config.get("multimedia","rewind_key")
			self.fullscreen_key_m = self.config.get("multimedia","fullscreen_key_m")
			self.volume_m_key = self.config.get("multimedia","volume_m_key")
			self.volume_p_key = self.config.get("multimedia","volume_p_key")
			self.no_fullscreen_key_m = self.config.get("multimedia", "no_fullscreen_key_m")
			self.mute_key = self.config.get("multimedia","mute_key")
			self.previous_key_m = self.config.get("multimedia","previous_key_m")
			self.next_key_m = self.config.get("multimedia","next_key_m")
			#games profile
			self.up_key = self.config.get("games","up_key")
			self.down_key = self.config.get("games","down_key")
			self.right_key = self.config.get("games","right_key")
			self.left_key = self.config.get("games","left_key")
			self.a_key = self.config.get("games", "a_key")
			self.b_key = self.config.get("games","b_key")
			self.c_key = self.config.get("games","c_key")
			self.x_key = self.config.get("games", "x_key")
			self.y_key = self.config.get("games", "y_key")
			self.z_key = self.config.get("games", "z_key")
			self.one_key = self.config.get("games", "one_key")
			self.two_key = self.config.get("games", "two_key")
			#autoconnect options
			self.name = self.config.get("autoconnect","name")
			self.addr = self.config.get("autoconnect", "addr")

		except:
			
			print "Error: Failed to read the config file"
			try:
				#try to restore the conf files
				os.system("mkdir /etc/bluemaemo/")
				os.system("cp /usr/share/bluemaemo/data/bluemaemo.cfg /etc/bluemaemo/")
			except:
				print "Error: Failed to restore the config file"
				
			ecore.main_loop_quit()

	def set_option(self,seccion,opt,value):
		
		self.config.set(seccion,opt, value)
		print "conf set"
		
	def save_options(self):	
	
		try:
			
			file = open(defaultsfile, 'w')
			self.config.write(file)
			file.close()
			print "Options saved"
			
		except:
			
			print "Error: Non such file or directory \'" + defaultsfile + "\'"

		
		

