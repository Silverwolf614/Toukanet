import pyxel
import random

TILE = 8
MAP_WIDTH = 64
MAP_HEIGHT = 48

class Player:
    
    width = 8
    heigth = 8
    
    def __init__(self):
        
        self.x = MAP_WIDTH * TILE / 2
        self.y = MAP_HEIGHT * TILE - 16
        self.DX = 5
        self.DY = 7
        self.flying = False
        self.direction = 1
        
    def update(self):
#collision platform and sprite
        #platform y = 102
        if self.y <= 15 * TILE and self.y >= 102 and ((self.x >= 0 and self.x <= 16 * TILE) or (self.x <= 64 * TILE and self.x >= 47 * TILE) or (self.x >= 23 * TILE and self.x <= 40 * TILE)):
            self.y = 102
        #platform y = 230
        if self.y <= 31 * TILE and self.y >= 230 and ((self.x >= 0 and self.x <= 16 * TILE) or (self.x <= 64 * TILE and self.x >= 47 * TILE) or (self.x >= 23 * TILE and self.x <= 40 * TILE)):
            self.y = 230

#platform y = -136        
        self.flying = False
        if self.y < 367 :
            self.y = (self.y + 2) % pyxel.height

#player moving, detect key pressed            
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            if self.y > 8:
                self.y = self.y - self.DY
                self.flying = True
              
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if self.y < 340:
                if self.y != 232 and self.y != 104:
                    self.y = self.y + self.DY
            
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.x = min(TILE * MAP_WIDTH - 16, self.x + self.DX)
            self.direction = 1
                
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            self.x = max(0, self.x - self.DX)
            self.direction = -1

    def draw(self):
        if self.flying:
#animation flying
            if pyxel.frame_count % 6 < 3:
                pyxel.blt(self.x, self.y, 0, 16, 0, self.direction * 16, 16, 7)
            else:
                pyxel.blt(self.x, self.y, 0, 16, 32, self.direction * 16, 16, 7)
        else:
            if pyxel.frame_count % 12 < 3:
                pyxel.blt(self.x, self.y, 0, 0, 0, self.direction * 16, 16, 7)
            else:
                pyxel.blt(self.x, self.y, 0, 0, 32, self.direction * 16, 16, 7) 

class App:
    
    def __init__(self):
        #init(width, height, [title], [fps], [quit_key], [display_scale], [capture_scale], [capture_sec])
        pyxel.init(MAP_WIDTH * TILE, MAP_HEIGHT * TILE, fps=30)
        pyxel.load("res.pyxres")
        self.player = Player()
        self.life = 3
        self.score = 0
        self.win_score = 5
        self.fruit = 0
        self.level = 15
        self.game_over = False
        self.level_up = False
        
        self.enemy_speed = 3
        
        self.enemies_list = []
        self.fruits_list = []
        
        pyxel.run(self.update, self.draw)
        
            
#enemy create 0.5s per 1 (frame_count % 30 == 0 >>> 1s per 1)         
    def enemy_create(self):
        if pyxel.frame_count % self.level == 0:
            self.enemies_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
#fruit create 2s per 1 (frame_count % 30 == 0 >>> 1s per 1)            
    def fruit_create(self):
        if pyxel.frame_count % 60 == 0 and self.fruit < 3:
            self.x = [random.randint(0, 16), random.randint(23, 40), random.randint(47, 64)]
            self.y = [104, 232]
            self.fruits_list.append([random.choice(self.x) * TILE, random.choice(self.y)])
            self.fruit += 1
            
#gravity of bottle y + 3 per second, remove out the screen
    def enemy_move(self):
        for enemy in self.enemies_list:
            enemy[1] += self.enemy_speed
            if enemy[1] > TILE * MAP_HEIGHT:
                self.enemies_list.remove(enemy)
                
#detecte collision with coordination of two sprites
    def enemy_collision(self):
        for enemy in self.enemies_list:
            if enemy[0] <= self.player.x + 16 and enemy[1] <= self.player.y + 16 and enemy[0] + 8 >= self.player.x and enemy[1] + 16 >= self.player.y :
                self.enemies_list.remove(enemy)
                self.life -= 1
    def fruit_collision(self):
        for fruit in self.fruits_list:
            if fruit[0] <= self.player.x + 16 and fruit[1] <= self.player.y + 16 and fruit[0] + 8 >= self.player.x and fruit[1] + 16 >= self.player.y :
                self.fruits_list.remove(fruit)
                self.fruit -= 1
                self.score += 1
                
                
    def update(self):
#call function
        self.player.update()
#work when level up by C pressed
        if self.level_up == True and pyxel.btnp(pyxel.KEY_C):
            self.win_score += 5
            self.level -= 2
            self.enemy_speed += 1.5
            self.level_up = False
            self.life = 3
            self.player.x = MAP_WIDTH * TILE / 2
            self.player.y = MAP_HEIGHT * TILE - 16
        self.enemy_create()
        self.enemy_move()
        self.enemy_collision()
        self.fruit_create()
        self.fruit_collision()

        
    def draw(self):
        pyxel.cls(11)
        if self.game_over == False:
            if self.life <= 0:
                self.game_over = True
            pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.player.draw()
#animation of heart with life leftover
            if self.life >= 1 :
                pyxel.blt(0, 0, 0, 0, 16, 16, 16, 0)
            if self.life >= 2 :
                pyxel.blt(16, 0, 0, 0, 16, 16, 16, 0)
            if self.life == 3:
                pyxel.blt(32, 0, 0, 0, 16, 16, 16, 0)
            
            
#for enemy and fruit created(in the list) draw the sprite only when game is working 
# x, y, img, u, v, width, height, transparent color
            if self.game_over == False and self.level_up == False:
                for enemy in self.enemies_list:
                    pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 0)
                    
                for fruit in self.fruits_list:
                    pyxel.blt(fruit[0], fruit[1], 0, 32, 16, 16, 16, 0)
#victory menu 
        if self.score >= self.win_score:
            pyxel.bltm(0, 0, 6, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.level_up = True
#Gameover bloc                
        if self.game_over == True:
            pyxel.bltm(0, 0, 7, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
        
        
App()


        



        
    



