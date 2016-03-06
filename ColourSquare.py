"""
Copyright (C) 2014 Andrew Skinner <obs@theandyroid.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""


import obspython as libobs
import os,traceback,sys
from random import randint


class ColourSquare():
    def __init__(self,settings,source):
        self.source = source
        self.width = 1
        self.height = 1
        self.bpp = 4

        self.multi = 1
        self.rand = 0
        LEVELS =1  
        
        self.pixelbuffer = bytearray(self.width*self.height*self.bpp)


        self.SetColour(0,0,0,255)
        
        libobs.obs_enter_graphics()
        self.tex = libobs.gs_texture_create(self.width,
                                            self.height,
                                            libobs.GS_BGRA,
                                            1,
                                            self.pixelbuffer,libobs.GS_DYNAMIC)
        libobs.obs_leave_graphics()         
        libobs.blog("oestuhoensthu")
    @staticmethod
    def create(settings,source):
        return ColourSquare(settings,source)
    def render(self,effect):

        
        self.rand += 1*self.multi
        if(self.rand >= 255):
            self.multi = -1
        if(self.rand <= 0):
            self.multi = 1
            
        self.SetColour(0,self.rand,0,255)



        # no go zone if you error in the graphics mutex you will freeze obs
        libobs.obs_enter_graphics()        
        libobs.gs_reset_blend_state()
        libobs.gs_effect_set_texture(
            libobs.gs_effect_get_param_by_name(effect, "image"),
            self.tex)    
        libobs.gs_texture_set_image(self.tex,self.pixelbuffer,self.width*self.bpp,False)
        libobs.gs_draw_sprite(self.tex, 0, 
                              self.width, 
                              self.height)


        libobs.obs_leave_graphics()         

    def tick(self,seconds):
        pass

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height

    def destroy(self):
        libobs.obs_enter_graphics()        
        libobs.gs_texture_destroy(self.tex)
        libobs.obs_leave_graphics()         
        print("Destroy")

        pass
    def get_properties(self):
        self.props = libobs.obs_properties_create()
        return self.props

    def update(self,data):
        return

    def save(self,data):
        return

    @staticmethod
    def get_name():
        return "COLOURSQUARE"

    def SetColour(self,r,g,b,a):
        for i in range(0,self.width*self.height*self.bpp,self.bpp):
            self.pixelbuffer[i] = b  #blue
            self.pixelbuffer[i+1] = g #green
            self.pixelbuffer[i+2] = r #red
            self.pixelbuffer[i+3] = a #alpha


def register():

    src = libobs.obs_source_info()
    src.id = "ColourSquare"
    src.get_name = ColourSquare.get_name
    src.create = ColourSquare.create
    src.video_render = ColourSquare.render
    src.video_tick = ColourSquare.tick
    src.get_height = ColourSquare.get_height
    src.get_width = ColourSquare.get_width
    src.destroy = ColourSquare.destroy
    src.get_properties = ColourSquare.get_properties
    src.update = ColourSquare.update
    src.save = ColourSquare.save
    libobs.obs_register_source(src)

    print ("Registered ColourSquare")

