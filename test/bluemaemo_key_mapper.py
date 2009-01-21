# -*- coding: utf-8 -*-
#
#      bluemaemo_key_mapper.py
#
#      Copyright 2008 	Valerio Valerio <vdv100@gmail.com>
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

class key_mapper:
	
	def __init__(self):
		
		self.mapper = {}
		
		self.mapper['a'] = 4
		self.mapper['b'] = 5
		self.mapper['c'] = 6
		self.mapper['d'] = 7
		self.mapper['e'] = 8
		self.mapper['f'] = 9
		self.mapper['g'] = 10
		self.mapper['h'] = 11
		self.mapper['i'] = 12
		self.mapper['j'] = 13
		self.mapper['k'] = 14
		self.mapper['l'] = 15
		self.mapper['m'] = 16
		self.mapper['n'] = 17
		self.mapper['o'] = 18
		self.mapper['p'] = 19
		self.mapper['q'] = 20
		self.mapper['r'] = 21
		self.mapper['s'] = 22
		self.mapper['t'] = 23
		self.mapper['u'] = 24
		self.mapper['v'] = 25
		self.mapper['w'] = 26
		self.mapper['x'] = 27
		self.mapper['y'] = 28
		self.mapper['z'] = 29  
		
		self.mapper['1'] = 30
		self.mapper['2'] = 31
		self.mapper['3'] = 32
		self.mapper['4'] = 33
		self.mapper['5'] = 34
		self.mapper['6'] = 35
		self.mapper['7'] = 36
		self.mapper['8'] = 37
		self.mapper['9'] = 38
		self.mapper['0'] = 39
		self.mapper['Return'] = 40
		self.mapper['KP_Enter'] = 40
		self.mapper['Escape'] = 41 
		self.mapper['BackSpace'] = 42
		self.mapper['Tab'] = 43
		self.mapper['space'] = 44
		self.mapper['minus'] = 45
		self.mapper['-'] = 45
		self.mapper['equal'] = 46 
		self.mapper['='] = 46
		self.mapper['bracketleft'] = 47
		self.mapper['['] = 47
		self.mapper['bracketright'] = 48
		self.mapper[']'] = 48
		self.mapper['backslash'] = 49
		self.mapper['\\'] = 49
		
		self.mapper['semicolon'] = 51
		self.mapper[';'] = 51
		self.mapper['apostrophe'] = 52
		self.mapper['\''] = 52
		self.mapper['grave'] = 53
		self.mapper['`'] = 53
		self.mapper['comma'] = 54
		self.mapper[','] = 54
		self.mapper['period'] = 55
		self.mapper['.'] = 55
		self.mapper['slash'] = 56
		self.mapper['/'] = 56
		
		self.mapper['f1'] = 58
		self.mapper['f2'] = 59
		self.mapper['f3'] = 60
		self.mapper['f4'] = 61
		self.mapper['f5'] = 62
		self.mapper['f6'] = 63
		self.mapper['f7'] = 64
		self.mapper['f8'] = 65
		self.mapper['f9'] = 66
		self.mapper['f10'] = 67
		self.mapper['f11'] = 68
		self.mapper['f12'] = 69
		
		self.mapper['F1'] = 58
		self.mapper['F2'] = 59
		self.mapper['F3'] = 60
		self.mapper['F4'] = 61
		self.mapper['F5'] = 62
		self.mapper['F6'] = 63
		self.mapper['F7'] = 64
		self.mapper['F8'] = 65
		self.mapper['F9'] = 66
		self.mapper['F10'] = 67
		self.mapper['F11'] = 68
		self.mapper['F12'] = 69
		
		self.mapper['Insert'] = 73
		self.mapper['Home'] = 74
		self.mapper['Prior'] = 75
		self.mapper['Delete'] = 76
		self.mapper['End'] = 77
		self.mapper['Next'] = 78
		self.mapper['Right'] = 79
		self.mapper['Left'] = 80
		self.mapper['Down'] = 81
		self.mapper['Up'] = 82
		
		self.mapper["v+"] = 128
		self.mapper["v-"] = 129
		
		
		#include tilde ~
		#self.mapper['minus'] = 86
		
		#shift user translation
		self.mapper["space_t"] = "space"
		self.mapper['shift+a'] = "A"
		self.mapper['shift+b'] = "B"
		self.mapper['shift+c'] = "C"
		self.mapper['shift+d'] = "D"
		self.mapper['shift+e'] = "E"
		self.mapper['shift+f'] = "F"
		self.mapper['shift+g'] = "G"
		self.mapper['shift+h'] = "H"
		self.mapper['shift+i'] = "I"
		self.mapper['shift+j'] = "J"
		self.mapper['shift+k'] = "K"
		self.mapper['shift+l'] = "L"
		self.mapper['shift+m'] = "M"
		self.mapper['shift+n'] = "N"
		self.mapper['shift+o'] = "O"
		self.mapper['shift+p'] = "P"
		self.mapper['shift+q'] = "Q"
		self.mapper['shift+r'] = "R"
		self.mapper['shift+s'] = "S"
		self.mapper['shift+t'] = "T"
		self.mapper['shift+u'] = "U"
		self.mapper['shift+v'] = "V"
		self.mapper['shift+w'] = "W"
		self.mapper['shift+x'] = "X"
		self.mapper['shift+y'] = "Y"
		self.mapper['shift+z'] = "Z"
		
		
		self.mapper['shift+1'] = "!"
		self.mapper['shift+2'] = "@"
		self.mapper['shift+3'] = "#"
		self.mapper['shift+4'] = "$"
		self.mapper['shift+5'] = "%"
		self.mapper['shift+6'] = "^"
		self.mapper['shift+7'] = "&"
		self.mapper['shift+8'] = "*"
		self.mapper['shift+9'] = "("
		self.mapper['shift+0'] = ")"
		self.mapper['Shift+grave'] = "~"
		self.mapper['shift+minus'] = "_"
		self.mapper['shift+equal'] = "+"
		self.mapper['shift+bracketleft'] = "{"
		self.mapper['shift+bracketright'] = "}"
		self.mapper['shift+backslash'] = "|"
		self.mapper['shift+semicolon'] = ":"
		self.mapper['shift+apostrophe'] = "?"
		self.mapper['shift+comma'] = "<"
		self.mapper['shift+period'] = ">"
		self.mapper['shift+slash'] = "?"
		self.mapper['shift+plus'] = "="
		
		
		self.mapper["fn_k+q"] = 30
		self.mapper["fn_m+q"] = 0
		self.mapper["fn_k+w"] = 31
		self.mapper["fn_m+w"] = 0
		self.mapper["fn_k+e"] = 32
		self.mapper["fn_m+e"] = 0
		self.mapper["fn_k+r"] = 33
		self.mapper["fn_m+r"] = 0
		self.mapper["fn_k+t"] = 34
		self.mapper["fn_m+t"] = 0
		self.mapper["fn_k+y"] = 35
		self.mapper["fn_m+y"] = 0
		self.mapper["fn_k+u"] = 36
		self.mapper["fn_m+u"] = 0		
		self.mapper["fn_k+i"] = 37
		self.mapper["fn_m+i"] = 0
		self.mapper["fn_k+o"] = 38
		self.mapper["fn_m+o"] = 0
		self.mapper["fn_k+p"] = 39
		self.mapper["fn_m+p"] = 0
		
		self.mapper["fn_k+a"] = 30
		self.mapper["fn_m+a"] = 02
		self.mapper["fn_k+s"] = 52
		self.mapper["fn_m+s"] = 02
		self.mapper["fn_k+d"] = 31
		self.mapper["fn_m+d"] = 02
		self.mapper["fn_k+f"] = 32
		self.mapper["fn_m+f"] = 02
		self.mapper["fn_k+g"] = 49
		self.mapper["fn_m+g"] = 0
		self.mapper["fn_k+h"] = 56
		self.mapper["fn_m+h"] = 0
		self.mapper["fn_k+j"] = 38
		self.mapper["fn_m+j"] = 02
		self.mapper["fn_k+k"] = 39
		self.mapper["fn_m+k"] = 02
		self.mapper["fn_k+l"] = 37
		self.mapper["fn_m+l"] = 02
		self.mapper["fn_k+apostrophe"] = 56
		self.mapper["fn_m+apostrophe"] = 02
		
		#self.mapper["fn+z"] = 37
		#self.mapper["fn+z+mod"] = 02
		self.mapper["fn_k+x"] = 35
		self.mapper["fn_m+x"] = 02
		self.mapper["fn_k+c"] = 53
		self.mapper["fn_m+c"] = 02
		self.mapper["fn_k+v"] = 34
		self.mapper["fn_m+v"] = 02
		self.mapper["fn_k+b"] = 36
		self.mapper["fn_m+b"] = 02
		self.mapper["fn_k+n"] = 33
		self.mapper["fn_m+n"] = 02
		self.mapper["fn_k+m"] = 8
		self.mapper["fn_m+m"] = 64
		self.mapper["fn_k+semicolon"] = 32
		self.mapper["fn_m+semicolon"] = 64
		self.mapper["fn_k+minus"] = 45
		self.mapper["fn_m+minus"] = 02
		self.mapper["plus"] = 46
		self.mapper["fn_k+plus"] = 46
		self.mapper["fn_m+plus"] = 0

		#Fn user translation

		self.mapper["fn_k+q+u"] = "1"
		self.mapper["fn_k+w+u"] = "2"
		self.mapper["fn_k+e+u"] = "3"
		self.mapper["fn_k+r+u"] = "4"
		self.mapper["fn_k+t+u"] = "5"
		self.mapper["fn_k+y+u"] = "6"
		self.mapper["fn_k+u+u"] = "7"		
		self.mapper["fn_k+i+u"] = "8"
		self.mapper["fn_k+o+u"] = "9"
		self.mapper["fn_k+p+u"] = "0"
		
		self.mapper["fn_k+a+u"] = "!"
		self.mapper["fn_k+s+u"] = "\""
		self.mapper["fn_k+d+u"] = "@"
		self.mapper["fn_k+f+u"] = "#"
		self.mapper["fn_k+g+u"] = "\\"
		self.mapper["fn_k+h+u"] = "/"
		self.mapper["fn_k+j+u"] = "("
		self.mapper["fn_k+k+u"] = ")"
		self.mapper["fn_k+l+u"] = "*"
		self.mapper["fn_k+apostrophe+u"] = "?"
		
		#self.mapper["fn+z+u"] = 37
		self.mapper["fn_k+x+u"] = "^"
		self.mapper["fn_k+c+u"] = "~"
		self.mapper["fn_k+v+u"] = "%"
		self.mapper["fn_k+b+u"] = "&"
		self.mapper["fn_k+n+u"] = "$"
		self.mapper["fn_k+m+u"] = "€"
		self.mapper["fn_k+semicolon+u"] = "£"
		self.mapper["fn_k+minus+u"] = "_"
		self.mapper["fn_k+plus+u"] = "="

		#vkb mapping
		self.mapper[":_k"] = 51
		self.mapper[":_m"] = 02
		self.mapper["(_k"] = 38
		self.mapper["(_m"] = 02
		self.mapper[")_k"] = 39
		self.mapper[")_m"] = 02
		self.mapper["$_k"] = 33
		self.mapper["$_m"] = 02
		self.mapper["&_k"] = 36
		self.mapper["&_m"] = 02
		self.mapper["@_k"] = 31
		self.mapper["@_m"] = 02
		self.mapper["?_k"] = 56
		self.mapper["?_m"] = 02
		self.mapper["!_k"] = 30
		self.mapper["!_m"] = 02
		self.mapper["\"_k"] = 52
		self.mapper["\"_m"] = 02
		self.mapper["*_k"] = 37
		self.mapper["*_m"] = 02
		self.mapper["+_k"] = 46
		self.mapper["+_m"] = 02
		self.mapper["__k"] = 45
		self.mapper["__m"] = 02
		self.mapper["#_k"] = 32
		self.mapper["#_m"] = 02
		self.mapper["%_k"] = 34
		self.mapper["%_m"] = 02
		self.mapper["~_k"] = 53
		self.mapper["~_m"] = 02
		self.mapper["|_k"] = 49
		self.mapper["|_m"] = 02
		self.mapper["<_k"] = 54
		self.mapper["<_m"] = 02
		self.mapper[">_k"] = 55
		self.mapper[">_m"] = 02
		self.mapper["{_k"] = 47
		self.mapper["{_m"] = 02
		self.mapper["}_k"] = 48
		self.mapper["}_m"] = 02
		self.mapper["^_k"] = 35
		self.mapper["^_m"] = 02

		#Vkb user translation
		
		self.mapper["sp+:"] = ":"
		self.mapper["sp+("] = "("
		self.mapper["sp+)"] = ")"
		self.mapper["sp+$"] = "$"
		self.mapper["sp+&"] = "&"
		self.mapper["sp+@"] = "@"
		self.mapper["sp+?"] = "?"
		self.mapper["sp+!"] = "!"
		self.mapper["sp+\""] = "\""
		self.mapper["sp+*"] = "*"
		self.mapper["sp++"] = "+"
		self.mapper["sp+_"] = "_"
		self.mapper["sp+#"] = "#"
		self.mapper["sp+%"] = "%"
		self.mapper["sp+~"] = "~"
		self.mapper["sp+|"] = "|"
		self.mapper["sp+<"] = "<"
		self.mapper["sp+>"] = ">"
		self.mapper["sp+{"] = "{"
		self.mapper["sp+}"] = "}"
		self.mapper["sp+^"] = "^"
