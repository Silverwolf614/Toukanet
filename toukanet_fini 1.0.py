import pyxel
import random

TILE = 8
#64 * 8 = 512
MAP_WIDTH = 64
#48 * 8 = 384
MAP_HEIGHT = 48

class Player:
    
    def __init__(self):
        #coordonée, vitesse, direction, état
        self.x = MAP_WIDTH * TILE / 2
        self.y = MAP_HEIGHT * TILE - 16
        self.DX = 5
        self.DY = 7
        self.flying = False
        #droite = 1, gauche = -1
        self.direction = 1
        
    def update(self):
#collision platform and sprite
        #platform y = 102
        if 102 <= self.y <= 15 * TILE and ((self.x >= 0 and self.x <= 16 * TILE) or (self.x <= 64 * TILE and self.x >= 47 * TILE) or (self.x >= 23 * TILE and self.x <= 40 * TILE)):
            self.y = 102
        #platform y = 230
        elif 230 <= self.y <= 31 * TILE and ((self.x >= 0 and self.x <= 16 * TILE) or (self.x <= 64 * TILE and self.x >= 47 * TILE) or (self.x >= 23 * TILE and self.x <= 40 * TILE)):
            self.y = 230


        

#platform y = -136        
        self.flying = False
        #gravity
        if self.y < 367 :
            self.y = (self.y + 2) % pyxel.height

#player moving, detect key pressed          
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            if self.y > 8:
                self.y -= self.DY
                self.flying = True
              
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if self.y < 340:
                if self.y != 232 and self.y != 104:
                    self.y += self.DY
            
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            if self.x < TILE * MAP_WIDTH - 16 :
                self.x += self.DX
                self.direction = 1
                
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            if self.x > 0 :
                self.x -= self.DX
                self.direction = -1

    def draw(self):
        #if self.flying == True:
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
        #les variables changeable dans le code suivant
        pyxel.init(MAP_WIDTH * TILE, MAP_HEIGHT * TILE, fps=30)
        pyxel.load("res.pyxres")
        self.player = Player()
        self.life = 3
        self.score = 0
        self.level = 0
        self.score_list = [5, 10, 15, 20, 25]
        self.win_score = 5
        self.fruit = 0
        self.frame_enemy = [15, 12, 9, 4.5, 3]
        self.game_over = False
        self.level_up = False
         
        self.enemy_speed = 3
        
        self.enemies_list = []
        self.fruits_list = []
        self.heals_list = []
        
        self.d = 0
        self.u = 0
        pyxel.run(self.update, self.draw)
        
            
#enemy create 0.5s per 1 (frame_count % 30 == 0 >>> 1s per 1)         
    def enemy_create(self):
        if pyxel.frame_count % self.frame_enemy[self.level] == 0:
            self.enemies_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
#fruit create 2s per 1 (frame_count % 30 == 0 >>> 1s per 1)            
    def fruit_create(self):
        if pyxel.frame_count % 60 == 0 and self.fruit < 3:
            self.x = [random.randint(0, 16), random.randint(23, 40), random.randint(47, 64)]
            self.y = [104, 232]
            self.fruits_list.append([random.choice(self.x) * TILE, random.choice(self.y)])
            self.fruit += 1
            
#gravity of bottle y + 3 per second, remove out the screen
#enemy[0] = x, enemy[1] = y
    def enemy_move(self):
        for enemy in self.enemies_list:
            enemy[1] += self.enemy_speed
            if enemy[1] > TILE * MAP_HEIGHT:
                self.enemies_list.remove(enemy)
                
#detecte collision with coordination of two sprites
    def enemy_collision(self):
        for enemy in self.enemies_list:
            if self.player.x - 8 <= enemy[0] <= self.player.x + 16 and self.player.y - 8 <= enemy[1] <= self.player.y + 16:
                self.enemies_list.remove(enemy)
                self.life -= 1
                
    def fruit_collision(self):
        for fruit in self.fruits_list:
            if self.player.x - 8 <= fruit[0] <= self.player.x + 16 and self.player.y - 8 <= fruit[1] <= self.player.y + 16:
                self.fruits_list.remove(fruit)
                self.fruit -= 1
                self.score += 1

                           
                
    def update(self):
#call function
        self.player.update()
#work when level up by C pressed
        if self.level_up == True and pyxel.btnp(pyxel.KEY_C):
            self.win_score = self.score_list[self.level]
            self.enemy_speed += 1.5
            self.level += 1
            self.level_up = False
            self.life = 3
#coordonnée initiale
            self.player.x = MAP_WIDTH * TILE / 2
            self.player.y = MAP_HEIGHT * TILE - 16
        if self.level == 1:
            self.player.DY = 8
            
        if self.level == 2:
            self.player.DX = 6
            
        if self.level == 3:
            self.player.DY = 9
        
        if self.level == 4:
            self.player.DX = 8
            self.life = 5
        self.enemy_create()
        self.enemy_move()
        self.enemy_collision()
        self.fruit_create()
        self.fruit_collision()
        self.d = self.score // 10
        self.u = self.score % 10

    
        
    def draw(self):
        pyxel.cls(11)
        if self.game_over == False :
            if self.life <= 0:
                self.game_over = True
            pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.player.draw()
#animation of heart with life leftover
            if self.life >= 1 :
                pyxel.blt(0, 0, 0, 0, 16, 16, 16, 0)
            if self.life >= 2 :
                pyxel.blt(16, 0, 0, 0, 16, 16, 16, 0)
            if self.life >= 3:
                pyxel.blt(32, 0, 0, 0, 16, 16, 16, 0)
            

#score printing
            if self.d <= 4:
                pyxel.blt(60 * TILE, 0, 0, self.d * 16, 128, 16, 16, 0)
            else:
                pyxel.blt(60 * TILE, 0, 0, (self.d - 5) * 16, 144, 16, 16, 0)
            if self.u <= 4:
                pyxel.blt(62 * TILE, 0, 0, self.u * 16, 128, 16, 16, 0)
            else:
                pyxel.blt(62 * TILE, 0, 0, (self.u - 5) * 16, 144, 16, 16, 0)    
            
#for enemy and fruit created(in the list) draw the sprite only when game is working 
# x, y, img, u, v, width, height, transparent color
            if self.game_over == False and self.level_up == False:
                for enemy in self.enemies_list:
                    pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 0)
                    
                for fruit in self.fruits_list:
                    pyxel.blt(fruit[0], fruit[1], 0, 32, 16, 16, 16, 0)
                    

#victory menu 
        if self.score >= self.win_score:
            self.life = 100
            pyxel.bltm(0, 0, 6, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.level_up = True
            if self.level > 4 :
                self.life = 1000
                pyxel.bltm(0, 0, 5, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            
#Gameover bloc                
        if self.game_over == True:
            pyxel.bltm(0, 0, 7, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            
        
        
App()


        



        
    



