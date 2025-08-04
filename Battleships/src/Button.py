import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlttf
import sdl2.sdlimage
import time
import ctypes

from src import Window
from src import Theme
from src import Text

ButtonStates = ["idle", "hover", "press"]

class Button_With_Text:
    
    def __init__(self, text: str, x: int, y: int , w: int, h: int):
        
        self.text = text
        self.font = Theme.font
        self.font_size = Theme.font_size
        self.color = sdl2.ext.Color(64, 64, 64)
        self.color_hover = sdl2.ext.Color(80, 80, 80)
        self.color_press = sdl2.ext.Color(96, 96, 96)
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.state = 0 # 0-idle, 1-hover, 2-press
        
        self.text_color = sdl2.ext.Color(255, 255, 255)

        self.onclick_func = None
        
        self.click_time = time.time()
    
    def set_text(self, text:str):
        self.text = text
    
    def set_text_color(self, color: list[int]):
        self.text_color = color
    def set_font_size(self, size: int):
        self.font_size = size

    def click(self):
        if(self.onclick_func):
                self.onclick_func()
                        
    def cursor_hover(self):
        if self.state != 2:

            mx = ctypes.c_int(0)
            my = ctypes.c_int(0)
            sdl2.SDL_GetMouseState(ctypes.byref(mx), ctypes.byref(my))
            mouse_x, mouse_y = mx.value, my.value

            if mouse_x >= self.x-self.w//2 and mouse_x <= self.x+self.w//2 and mouse_y >= self.y-self.h//2 and mouse_y <= self.y+self.h//2:
                self.state = 1
            else:
                self.state = 0
            
    def handle_events(self, event: sdl2.ext.events):
        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            mx = ctypes.c_int(0)
            my = ctypes.c_int(0)
            sdl2.SDL_GetMouseState(ctypes.byref(mx), ctypes.byref(my))
            mouse_x, mouse_y = mx.value, my.value
            if mouse_x >= self.x-self.w//2 and mouse_x <= self.x+self.w//2 and mouse_y >= self.y-self.h//2 and mouse_y <= self.y+self.h//2:
                self.state = 2
                self.click_time = time.time()
            
    def update(self):
        if self.state == 2:
            if time.time() - self.click_time > 0.25:
                self.state = 0
                self.click()
        
    def draw(self):
       

        if self.state == 0:
            Window.renderer.color = self.color
        elif self.state == 1: 
            Window.renderer.color = self.color_hover
        else:
            Window.renderer.color = self.color_press
        
        rect = sdl2.SDL_Rect(self.x - self.w // 2, self.y - self.h// 2, self.w, self.h)
        Window.renderer.fill(rect)
        
        Text.draw_text_centered(self.x, self.y, self.text, self.font, self.font_size, self.text_color)
