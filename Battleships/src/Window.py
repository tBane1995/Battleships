import os
import sys
import sdl2
import sdl2.ext

window = sdl2.ext.Window
renderer = sdl2.ext.Renderer

color = sdl2.ext.Color(48, 48, 48)
size = (600, 600)


def create():
    global window
    global renderer
    global color
    global size

    window = sdl2.ext.Window("Battleships", size)
    window.show()
  
    renderer = sdl2.ext.Renderer(window)

