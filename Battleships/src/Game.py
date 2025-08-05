# Text.py
import sys
import os
import sdl2
import sdl2.ext
import sdl2.ext.ttf
import numpy as np
import time
from enum import Enum
import ctypes

from src import Window
from src import Theme
from src import Text
from src import Button
from src import Mapa

class Turn(Enum):
    Player = 1
    Player_To_Enemy = 2
    Enemy = 3
    Enemy_To_Player = 4

class Game:
    def __init__(self, difficulty: int):
        self.start_game(difficulty)
        
    def start_game(self, difficulty: int):
        
        self.difficulty = difficulty
        
        self.player = Mapa.Mapa()
        self.player.generate_ships()
        
        self.enemy = Mapa.Mapa()
        self.enemy.generate_ships()
        
        self.enemy_hits = []
        self.enemy_tiles_to_hits = []
        
        if np.random.randint(2) == 0:
            self.current_turn = Turn.Enemy
        else:
            self.current_turn = Turn.Player
        
        self.end_game = False
        self.player_win = False
        self.restart_btn = None
        
        self.action_time = 1
        self.last_action_time = time.time()

        
        
    def create_restart_btn(self):
        self.restart_btn = Button.Button_With_Text("restart", Window.size[0]//2, Window.size[1]//2 + 64, 128, 64)
        self.restart_btn.onclick_func = lambda: Window.pages.pop()
        
    def get_min_x(self) -> int:
        min_x = self.enemy_hits[0][0]
        for i in self.enemy_hits:
            if i[0] < min_x:
                min_x = i[0]
        return min_x
    
    def get_max_x(self) -> int:
        max_x = self.enemy_hits[0][0]
        for i in self.enemy_hits:
            if i[0] > max_x:
                max_x = i[0]
        return max_x

    def get_min_y(self) -> int:
        min_y = self.enemy_hits[0][1]
        for i in self.enemy_hits:
            if i[1] < min_y:
                min_y = i[1]
        return min_y
    
    def get_max_y(self) -> int:
        max_y = self.enemy_hits[0][1]
        for i in self.enemy_hits:
            if i[1] > max_y:
                max_y = i[1]
        return max_y

    
            
            
    def enemy_turn(self):
       
        if time.time() - self.last_action_time < self.action_time:
            return
        
        if self.difficulty == 0 and np.random.randint(2)%2==0:
            x, y = self.player.get_random_empty_tile()
            
            if x==-1 and y ==-1:
                return
            
            self.player.attack_tile((x,y))
            self.current_turn = Turn.Enemy_To_Player
            self.last_action_time = time.time()
            return
                
        
        # ai
        if len(self.enemy_hits) == 0:
            
            x, y = self.player.get_random_empty_or_ship_tile()


            if self.player.tiles[y][x] == Mapa.empty or self.player.tiles[y][x] == Mapa.ship:
                    

                if self.player.attack_tile((x,y)) == True:

                    self.enemy_hits.append((x,y))
                        
                    if self.player.hit_sunk((self.enemy_hits[0][0], self.enemy_hits[0][1]), set()):
                        self.player.set_miss_around_ship((self.enemy_hits[0][0], self.enemy_hits[0][1]), set())
                        self.enemy_hits = []
                        self.enemy_tiles_to_hits = []
                    else:
                        if y>0 and (self.player.tiles[y-1][x] == Mapa.empty or self.player.tiles[y-1][x] == Mapa.ship):
                            self.enemy_tiles_to_hits.append((x,y-1))

                        if y<self.player.height - 1 and (self.player.tiles[y+1][x] == Mapa.empty or self.player.tiles[y+1][x] == Mapa.ship):
                            self.enemy_tiles_to_hits.append((x,y+1))

                        if x>0 and (self.player.tiles[y][x-1] == Mapa.empty or self.player.tiles[y][x-1] == Mapa.ship):
                            self.enemy_tiles_to_hits.append((x-1,y))

                        if x<self.player.width - 1 and (self.player.tiles[y][x+1] == Mapa.empty or self.player.tiles[y][x+1] == Mapa.ship):
                            self.enemy_tiles_to_hits.append((x+1,y))
                        

                else:
                    self.current_turn = Turn.Enemy_To_Player
                    self.last_action_time = time.time()

        elif len(self.enemy_hits) == 1:
            index = np.random.randint(len(self.enemy_tiles_to_hits))
            
            p = self.enemy_tiles_to_hits[index]

            if self.player.attack_tile(p) == True:
                self.enemy_hits.append(p)
                self.enemy_tiles_to_hits = []
            else:
                self.enemy_tiles_to_hits.remove(p)
                self.current_turn = Turn.Enemy_To_Player

            if self.player.hit_sunk((self.enemy_hits[0][0], self.enemy_hits[0][1]), set()):
                self.player.set_miss_around_ship((self.enemy_hits[0][0], self.enemy_hits[0][1]), set())
                self.enemy_hits = []
                self.enemy_tiles_to_hits = []

        else:
            # len(self.enemy_hits) > 1

            # ship horizontal or vertical
            if self.enemy_hits[0][1]- self.enemy_hits[1][1] != 0:
                # vertical
                x = self.enemy_hits[0][0]

                min_y = self.get_min_y()
                if min_y>0 and (self.player.tiles[min_y-1][x] == Mapa.ship or self.player.tiles[min_y-1][x] == Mapa.empty):
                   self.enemy_tiles_to_hits.append((x,min_y-1))
               
                max_y = self.get_max_y()
                if max_y<self.player.height-1 and (self.player.tiles[max_y+1][x] == Mapa.ship or self.player.tiles[max_y+1][x] == Mapa.empty):
                   self.enemy_tiles_to_hits.append((x,max_y+1))
             
            else:
                # horizontal ship
                y = self.enemy_hits[0][1]

                min_x = self.get_min_x()
                if min_x>0 and (self.player.tiles[y][min_x-1] == Mapa.ship or self.player.tiles[y][min_x-1] == Mapa.empty):
                   self.enemy_tiles_to_hits.append((min_x-1,y))
               
                max_x = self.get_max_x()
                if max_x<self.player.width-1 and (self.player.tiles[y][max_x+1] == Mapa.ship or self.player.tiles[y][max_x+1] == Mapa.empty):
                   self.enemy_tiles_to_hits.append((max_x+1,y))
             
            # attack 
            if len(self.enemy_tiles_to_hits)>0:
                
                index = np.random.randint(len(self.enemy_tiles_to_hits))
      
                p = self.enemy_tiles_to_hits[index]
                    
                if self.player.attack_tile(p) == True:
                    self.enemy_hits.append(p)
                    self.enemy_tiles_to_hits = []
                else:
                    self.enemy_tiles_to_hits.remove(p)
                    self.current_turn = Turn.Enemy_To_Player          

                if self.player.hit_sunk((self.enemy_hits[0][0], self.enemy_hits[0][1]), set()):
                    self.player.set_miss_around_ship((self.enemy_hits[0][0], self.enemy_hits[0][1]), set())
                    self.enemy_hits = []
                    self.enemy_tiles_to_hits = []   
         
        if self.player.ships_sunks():
            self.end_game = True
            self.player_win = False
            self.create_restart_btn()
            
        self.last_action_time = time.time()
                    
    def player_attack(self, event: sdl2.ext.events):

        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            
            mx = ctypes.c_int(0)
            my = ctypes.c_int(0)
            sdl2.SDL_GetMouseState(ctypes.byref(mx), ctypes.byref(my))
            mouse_x, mouse_y = mx.value, my.value

            x = (mouse_x-self.enemy.x-Theme.map_border)//Theme.tile_size
            y = (mouse_y-self.enemy.y-Theme.map_border)//Theme.tile_size
            
            if x<0 or x>=self.enemy.width or y<0 or y>=self.enemy.height:
                return

            if self.enemy.tiles[y][x] == Mapa.empty:
                self.enemy.tiles[y][x] = Mapa.miss
                self.current_turn = Turn.Player_To_Enemy
                self.last_action_time = time.time()
        
            if self.enemy.tiles[y][x] == Mapa.ship:
                self.enemy.tiles[y][x] = Mapa.hit
            
            if self.enemy.hit_sunk((x,y), set()):
                self.enemy.set_miss_around_ship((x,y), set())
            
            if self.enemy.ships_sunks():
                self.end_game = True
                self.player_win = True
                self.create_restart_btn()
        
    def player_turn(self):
        return
    
    def draw_end_screen(self):
        if self.player_win:
               Text.draw_text_centered(Window.size[0]//2,Window.size[1]//2-64,"You win", Theme.font, Theme.big_font_size, sdl2.ext.Color(255,255,255))
        else:
           Text.draw_text_centered(Window.size[0]//2,Window.size[1]//2-64,"You lost", Theme.font, Theme.big_font_size, sdl2.ext.Color(255,255,255))
        
        if self.restart_btn is not None:
            self.restart_btn.draw()
    
    def cursor_hover(self):
        if self.restart_btn is not None:
            self.restart_btn.cursor_hover()

    def handle_events(self, event: sdl2.ext.events):
        if self.restart_btn is not None:
            self.restart_btn.handle_events(event)
            
        elif self.current_turn == Turn.Player:
            self.player_attack(event)
            
    def update(self):
        if self.restart_btn is not None:
            self.restart_btn.update()
        elif self.current_turn == Turn.Enemy:
            self.enemy_turn()
            Text.draw_text_centered
        elif self.current_turn == Turn.Player:
            self.player_turn()
        elif self.current_turn == Turn.Enemy_To_Player:
            if time.time()-self.last_action_time>self.action_time:
                self.current_turn = Turn.Player
                self.last_action_time = time.time()
        elif self.current_turn == Turn.Player_To_Enemy:
            if time.time()-self.last_action_time>self.action_time:
                self.current_turn = Turn.Enemy
                self.last_action_time = time.time()
                
        
    
    def draw(self):

        if self.end_game == True:
           self.draw_end_screen()
                   
        elif self.current_turn == Turn.Player or self.current_turn == Turn.Player_To_Enemy:
           self.enemy.draw(False)
           Text.draw_text_centered(Window.size[0]//2,32,"Your turn", Theme.font, Theme.mid_font_size, sdl2.ext.Color(255,255,255))
          
        else:
            self.player.draw(True)
            Text.draw_text_centered(Window.size[0]//2,32,"Enemy turn", Theme.font, Theme.mid_font_size, sdl2.ext.Color(255,255,255))
        