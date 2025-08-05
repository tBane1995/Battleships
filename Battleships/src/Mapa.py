import os
import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
import numpy as np
from src import Window
from src import Theme
from src import Text

empty ='.'
ship = '#'
hit = 'X'
miss = '*'

class Mapa:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.tiles = np.full((self.width, self.height), empty, dtype=str)

        self.w = Theme.tile_size * 10 + 2 * Theme.map_border
        self.h = Theme.tile_size * 10 + 2 * Theme.map_border
        self.x = Window.size[0]//2 - self.w//2
        self.y = Theme.map_margin_top
        
    def get_random_empty_or_ship_tile(self) -> tuple[int, int]:
            
            empty_tiles = []
            for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[y][x] == empty or self.tiles[y][x] == ship:
                        empty_tiles.append((x,y))
            
            i = np.random.randint(len(empty_tiles))
            return empty_tiles[i]
        
    def get_random_empty_tile(self) -> tuple[int, int]:
            
            empty_tiles = []
            for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[y][x] == empty:
                        empty_tiles.append((x,y))
                        
            if len(empty_tiles) ==0:
                return (-1,-1)
                
            i = np.random.randint(len(empty_tiles))
            return empty_tiles[i]
  
    def generate_ship(self, len: int):
        
        generated = False
        
        while not generated:
            if np.random.randint(2) == 0:
                # vertical
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height-len)
                is_place = True
                
                for yy in range(-1, len+1):
                    for xx in range(-1, 2):
                        if x+xx>= 0 and x+xx< self.width and y+yy>=0 and y+yy<self.height and self.tiles[y+yy][x+xx] == ship:
                                is_place = False
                                break
                        
                if is_place == False:
                    continue
                
                for i in range(len):
                    self.tiles[y+i][x] = ship
                        
                generated = True
            else:
            # horizontal
           
                x = np.random.randint(0, self.width- len)
                y = np.random.randint(0, self.height)
                is_place = True
                
                for yy in range(-1, 2):
                    for xx in range(-1, len+1):
                        if x+xx>=0 and x+xx< self.width and y+yy>=0 and y+yy<self.height and self.tiles[y+yy][x+xx] == ship:
                                is_place = False
                                break
                        
                if is_place == False:
                    continue
                
                for i in range(len):
                    self.tiles[y][x+i] = ship
                        
                generated = True
    
    def generate_ships(self):
        
        ship_4_count = 1
        ship_3_count = 2
        ship_2_count = 3
        ship_1_count = 4
        
        for i in range(ship_4_count):
            self.generate_ship(4)
        
        for i in range(ship_3_count):
            self.generate_ship(3)
            
        for i in range(ship_2_count):
            self.generate_ship(2)
            
        for i in range(ship_1_count):
            self.generate_ship(1)
    
    def attack_tile(self, point: tuple[int, int]) -> bool:
        x, y = point
        if self.tiles[y][x] == empty:
            self.tiles[y][x] = miss
            return False

        if self.tiles[y][x] == ship:
            self.tiles[y][x] = hit
            return True
            
    def hit_sunk(self, point: tuple[int, int], check_list: set) -> bool:
        
        if point in check_list:
            return True
        
        x, y = point
        
        if x<0 or x>=self.width or y<0 or y>=self.height:
            return True
            
        check_list.add((x,y))
        
        if self.tiles[y][x] == ship:
            return False
        
        if self.tiles[y][x] == empty or self.tiles[y][x] == miss:
            return True
        
        if self.tiles[y][x] == hit:
            if not self.hit_sunk((x-1, y), check_list):
                return False
            if not self.hit_sunk((x+1, y), check_list):
                return False
            if not self.hit_sunk((x, y-1), check_list):
                return False
            if not self.hit_sunk((x, y+1), check_list):
                return False
        
        return True
        
    def set_miss_around_ship(self, point: tuple[int, int], check_list: set):
        
        if point in check_list:
            return
            
        x, y = point
        
        if x<0 or x>=self.width or y<0 or y>=self.height:
            return
            
        check_list.add((x,y))
        
        if self.tiles[y][x] == empty:
            self.tiles[y][x] = miss
        
        elif self.tiles[y][x] == hit:
            self.set_miss_around_ship((x-1,y-1), check_list)
            self.set_miss_around_ship((x,y-1), check_list)
            self.set_miss_around_ship((x+1,y-1), check_list)
            
            self.set_miss_around_ship((x-1,y), check_list)
            self.set_miss_around_ship((x+1,y), check_list)
            
            self.set_miss_around_ship((x-1,y+1), check_list)
            self.set_miss_around_ship((x,y+1), check_list)
            self.set_miss_around_ship((x+1,y+1), check_list)
        
    
    def ships_sunks(self):
        sunks = True
        for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[y][x] == ship:
                        sunks = False
                        
        return sunks
    
    def draw_border(self, border_color: sdl2.ext.Color):
        Window.renderer.color = border_color
        rect = sdl2.SDL_Rect(self.x, self.y, self.w, self.h)
        Window.renderer.fill(rect)
    
    def draw_tile(self, point: tuple[int, int], player_map: bool, show_ship: bool):
        
        x, y = point
        
        xx = self.x + Theme.tile_size*x + Theme.map_border
        yy = self.y + Theme.tile_size*y + Theme.map_border
                
        # border
        Window.renderer.color = sdl2.ext.Color(32, 32, 32)
        rect = sdl2.SDL_Rect(xx, yy, Theme.tile_size, Theme.tile_size)
        Window.renderer.fill(rect)
        
        # coords
        for i in range(10):
            xxx = self.x - Theme.tile_size//2 - Theme.map_border
            yyy = self.y + i*Theme.tile_size + Theme.tile_size//2 + Theme.map_border
            Text.draw_text_centered(xxx, yyy, str(i+1), Theme.font, Theme.font_size, sdl2.ext.Color(255, 255, 255))
            
        for i in range(10):
            xxx = self.x + i * Theme.tile_size + Theme.tile_size // 2 + Theme.map_border
            yyy = self.y - Theme.tile_size // 2 - Theme.map_border
            Text.draw_text_centered(xxx, yyy, chr(ord('a') + i), Theme.font, Theme.font_size, sdl2.ext.Color(255, 255, 255))
          
        # center
        Window.renderer.color = sdl2.ext.Color(64, 64, 64)
        rect = sdl2.SDL_Rect(xx + Theme.tile_border, yy + Theme.tile_border, Theme.tile_size-2*Theme.tile_border, Theme.tile_size-2*Theme.tile_border)
        Window.renderer.fill(rect)
        
        # object
        dstrect = sdl2.SDL_Rect(xx, yy, Theme.tile_size, Theme.tile_size)
        tex: sdl2.ext.Texture
        
        if player_map:
            if self.tiles[y][x] == empty:
                tex = Theme.player_empty
            elif self.tiles[y][x] == ship:
                    if show_ship:
                        tex = Theme.player_ship
                    else:
                        tex = Theme.player_empty
            elif self.tiles[y][x] == miss:
                tex = Theme.player_miss
            elif self.tiles[y][x] == hit:
                tex = Theme.player_hit
        else:
            if self.tiles[y][x] == empty:
                tex = Theme.enemy_empty
            elif self.tiles[y][x] == ship:
                    if show_ship:
                        tex = Theme.enemy_ship
                    else:
                        tex = Theme.enemy_empty
            elif self.tiles[y][x] == miss:
                tex = Theme.enemy_miss
            elif self.tiles[y][x] == hit:
                tex = Theme.enemy_hit
        
        sdl2.SDL_RenderCopy(Window.renderer.sdlrenderer, tex, None, dstrect)
    
    def draw(self, player_map: bool):
       
        if player_map:
           self.draw_border(Theme.player_color)
        else:
            self.draw_border(Theme.enemy_color)
        
        show_ships = player_map
        
        # draw tiles
        for y in range(self.height):
            for x in range(self.width):
                self.draw_tile((x, y), player_map, show_ships)