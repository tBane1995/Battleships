import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
import time

from src import Theme
from src import Window
from src import Text
from src import Button
from src import Game

class Start_Screen:
    
    def __init__(self):
        dist = 96
        
        self.easy_btn = Button.Button_With_Text("easy", Window.size[0]//2-dist, Window.size[1]//2 + 64, 128, 64)
        self.easy_btn.onclick_func = lambda: Window.pages.append(Game.Game(0))
        
        self.hard_btn = Button.Button_With_Text("hard", Window.size[0]//2+dist, Window.size[1]//2 + 64, 128, 64)
        self.hard_btn.onclick_func = lambda: Window.pages.append(Game.Game(1))
        
    def cursor_hover(self):
        self.easy_btn.cursor_hover()
        self.hard_btn.cursor_hover()
        
    def handle_events(self, event: sdl2.ext.events):
        self.easy_btn.handle_events(event)
        self.hard_btn.handle_events(event)
        
    def update(self):
        self.easy_btn.update()
        self.hard_btn.update()
        
    def draw(self):
        
        Text.draw_text_centered(Window.size[0]//2,Window.size[1]//2-64,"select difficulty", Theme.font, Theme.mid_font_size, sdl2.ext.Color(255,255,255))
        
        self.easy_btn.draw()
        self.hard_btn.draw()