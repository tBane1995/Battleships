import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
import time

sdl2.ext.init()

from src import Window
from src import Theme
from src import Game


Window.create()
Theme.load()
game = Game.Game()

while(True):

    # handle events
    events = sdl2.ext.get_events()

    game.cursor_hover()

    for event in events:
        if event.type == sdl2.SDL_QUIT:
            exit()
            
        game.handle_events(event)
        

    # update
    game.update()

    # draw
    Window.renderer.color = Window.color
    Window.renderer.clear()
    game.draw()
    Window.renderer.present()

    time.sleep(1/60)

exit()
    