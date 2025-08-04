import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlttf
import sdl2.sdlimage

from src import Window

font_size: int
mid_font_size: int
big_font_size: int
font: sdl2.ext.FontManager

player_empty : sdl2.ext.Texture
player_ship : sdl2.ext.Texture
player_hit : sdl2.ext.Texture
player_miss : sdl2.ext.Texture

enemy_empty : sdl2.ext.Texture
enemy_ship : sdl2.ext.Texture
enemy_hit : sdl2.ext.Texture
enemy_miss : sdl2.ext.Texture

player_color: sdl2.ext.Color
enemy_color: sdl2.ext.Color

tile_size: int
tile_border: int
map_border: int
map_margin_top: int
map_margin: int

def load_texture(path: str) -> sdl2.ext.Texture:
    surface = sdl2.sdlimage.IMG_Load(path.encode('utf-8'))
    texture = sdl2.SDL_CreateTextureFromSurface(Window.renderer.sdlrenderer, surface)
    sdl2.SDL_FreeSurface(surface)
    return texture

def load():

    global font
    global font_size
    global mid_font_size
    global big_font_size
    
    font_size = 20
    big_font_size = 64
    mid_font_size = 40
    font = sdl2.ext.FontManager(b"FiraCode-Medium.ttf")

    global player_color
    global enemy_color
    player_color = sdl2.ext.Color(32, 32, 128)
    enemy_color = sdl2.ext.Color(128, 32, 32)

    global player_empty
    global player_ship
    global player_hit
    global player_miss

    player_empty = load_texture("tex/player_empty.png")
    player_ship = load_texture("tex/player_ship.png")
    player_hit = load_texture("tex/player_hit.png")
    player_miss = load_texture("tex/player_miss.png")

    global enemy_empty
    global enemy_ship
    global enemy_hit
    global enemy_miss

    enemy_empty = load_texture("tex/enemy_empty.png")
    enemy_ship = load_texture("tex/enemy_ship.png")
    enemy_hit = load_texture("tex/enemy_hit.png")
    enemy_miss = load_texture("tex/enemy_miss.png")

    global tile_size
    global tile_border
    global map_border
    global map_margin_top
    global map_margin

    tile_size = 32
    tile_border = 1
    map_border = 6
    map_margin_top = 128
    map_margin = 16

