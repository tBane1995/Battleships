import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
import time

sdl2.ext.init()

from src import Theme
from src import Window
from src import Start_Screen
from src import Game

Window.create()
Theme.load()
Window.pages.append(Start_Screen.Start_Screen())

while(True):

    Window.pages[-1].cursor_hover()

    # handle events
    events = sdl2.ext.get_events()

    for event in events:
        if event.type == sdl2.SDL_QUIT:
            exit()
            
        Window.pages[-1].handle_events(event)
        

    # update
    Window.pages[-1].update()

    # draw
    Window.renderer.color = Window.color
    Window.renderer.clear()
    Window.pages[-1].draw()
    Window.renderer.present()

    time.sleep(1/60)

exit()
    