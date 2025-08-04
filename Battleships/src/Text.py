# Text.py
import sys
import os
import sdl2
import sdl2.ext
import sdl2.ext.ttf

from src import Window
_text_cache = {}

def draw_text_centered(x: int, y: int, text: str, font: sdl2.ext.FontManager, font_size: int, text_color: sdl2.ext.Color):
    if text == "" or text == "\n":
        return

    key = (text, font_size, text_color.r, text_color.g, text_color.b)
    
    if key not in _text_cache:
        surface = font.render(text, size=font_size, color=text_color)
        texture = sdl2.SDL_CreateTextureFromSurface(Window.renderer.sdlrenderer, surface)
        w = sdl2.c_int()
        h = sdl2.c_int()
        sdl2.SDL_QueryTexture(texture, None, None, w, h)
        _text_cache[key] = (texture, w.value, h.value)
        sdl2.SDL_FreeSurface(surface)

    texture, width, height = _text_cache[key]
    dstrect = sdl2.SDL_Rect(x - width // 2, y - height // 2, width, height)
    sdl2.SDL_RenderCopy(Window.renderer.sdlrenderer, texture, None, dstrect)