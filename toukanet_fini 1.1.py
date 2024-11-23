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
        pyxel.load("touka.pyxres")

        self.game_start = False
        self.game_over = False
        self.victory = False
        self.tilemap = 1
        self.bgc = 0
        self.world = 0
        
        self.player = Player()
        self.life = 3
        self.score = 0
        self.level = 0
        self.score_list = [4, 6, 8, 10]
        self.win_score = 2
        self.fruit = 0
        self.frame_enemy = [15, 12, 9, 4.5, 3]
        self.level_up = False
         
        self.enemy_speed = 3
        
        self.enemies_list = []
        self.fruits_list = []
        
        self.d = 0
        self.u = 0
        self.color = 2
        
        pyxel.run(self.update, self.draw)
        

        
    def restart(self):
        self.life = 3
        self.score = 0
        self.level = 0
        self.win_score = 2
        self.fruit = 0
        self.game_over == False
        
#enemy create 0.5s per 1 (frame_count % 30 == 0 >>> 1s per 1)         
    def enemy_create(self):
        if pyxel.frame_count % self.frame_enemy[self.level] == 0:
            self.enemies_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
#fruit create 2s per 1 (frame_count % 30 == 0 >>> 1s per 1)            
    def fruit_create(self):

        if pyxel.frame_count % 60 == 0 and self.fruit < 3:
            if self.tilemap == 0:
                self.x = [random.randint(0, 16), random.randint(23, 40), random.randint(47, 64)]
                self.y = [104, 232]
                self.fruits_list.append([random.choice(self.x) * TILE, random.choice(self.y)])
                
            if self.tilemap == 2:
                self.x_border = [random.randint(0, 16), random.randint(47, 64)]
                self.x_middle = random.randint(23, 39)
                self.y_border = (104, 232)
                self.y_middle = (168, 296)
                if random.randint(0, 1) == 0:
                    self.fruits_list.append([random.choice(self.x_border) * TILE, random.choice(self.y_border)])
                else:
                    self.fruits_list.append([self.x_middle * TILE, random.choice(self.y_middle)])
                    
            if self.tilemap == 3:
                self.x_border = [random.randint(0, 16), random.randint(47, 64)]
                self.x_middle = random.randint(24, 39)
                self.y_border = (40, 232)
                self.y_middle = 168
                if random.randint(0, 1) == 0:
                    self.fruits_list.append([random.choice(self.x_border) * TILE, random.choice(self.y_border)])
                else:
                    self.fruits_list.append([self.x_middle * TILE, self.y_middle])
                
            self.fruit += 1
                
#gravity of bottle y + 3 per second, remove out the screen
#enemy[0] = x, enemy[1] = y
    def enemy_move(self):
        for enemy in self.enemies_list:
            enemy[1] += self.enemy_speed
            if enemy[1] > TILE * MAP_HEIGHT:
                self.enemies_list.remove(enemy)
    
    def collision(self):
        if self.tilemap == 0:
            if 102 <= self.player.y <= 15 * TILE and ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE) or (self.player.x >= 23 * TILE and self.player.x <= 40 * TILE)):
                self.player.y = 102
            #platform y = 230
            elif 230 <= self.player.y <= 31 * TILE and ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE) or (self.player.x >= 23 * TILE and self.player.x <= 40 * TILE)):
                self.player.y = 230
                
        if self.tilemap == 2:
            if 102 <= self.player.y <= 15 * TILE and ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE)):
                self.player.y = 102
            elif 230 <= self.player.y <= 31 * TILE and ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE)):
                self.player.y = 230
            elif 166 <= self.player.y <= 23 * TILE and 40 * TILE >= self.player.x >= 23 * TILE:
                self.player.y = 166
            elif 294 <= self.player.y <= 39 * TILE and 40 * TILE >= self.player.x >= 23 * TILE:
                self.player.y = 294
                
        if self.tilemap == 3:
            if 166 <= self.player.y <= 24 * TILE and 40 * TILE >= self.player.x >= 23 * TILE:
                self.player.y = 166
            elif 38 <= self.player.y <= 7 * TILE and  ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE)):
                self.player.y = 38
            elif 230 <= self.player.y <= 31 * TILE and  ((self.player.x >= 0 and self.player.x <= 16 * TILE) or (self.player.x <= 64 * TILE and self.player.x >= 47 * TILE)):
                self.player.y = 230
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
        if pyxel.btnp(pyxel.KEY_1) and self.game_start != True:
            self.game_start = True
            self.tilemap = 0
            self.bgc = 11
            self.color = 13
            
        elif pyxel.btnp(pyxel.KEY_2) and self.game_start != True:
            self.game_start = True
            self.tilemap = 2
            self.bgc = 12
            self.color = 13
        
        elif pyxel.btnp(pyxel.KEY_3) and self.game_start != True:
            self.game_start = True
            self.tilemap = 3
            self.bgc = 9
            self.color = 13
            
        if self.level_up:
            self.color = 2
        else:
            self.color = 13
            
        
            
        if self.game_start:
            self.player.update()
            self.collision()
            
            if self.life <= 0:
                self.game_over = True
                self.tilemap = 7
    #victory detection
            if self.score >= self.win_score:
                self.level_up = True
                self.enemies_list = []
    
    #work when level up by C pressed
            if self.level_up and pyxel.btnp(pyxel.KEY_C) and self.level != 4:
                self.win_score = self.score_list[self.level]
                self.enemy_speed += 1.5
                self.level += 1
                self.level_up = False
                self.life = 3
                
            if self.level == 1:
                self.player.DY = 8
                
            if self.level == 2:
                self.player.DX = 6
                
            if self.level == 3:
                self.player.DY = 9
            
            if self.level == 4:
                self.player.DX = 8
                
            if self.level_up == False:   
                self.enemy_create()
                self.enemy_move()
                self.enemy_collision()
                self.fruit_create()
                self.fruit_collision()

            self.d = self.score // 10
            self.u = self.score % 10
        
        
    
        
    def draw(self):
        pyxel.cls(self.bgc)
        pyxel.bltm(0, 0, self.tilemap, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE, self.color)
        
        if self.game_start and self.game_over == False :
         
            self.player.draw()
    #affichage "LEVEL"        
            pyxel.blt(24 * TILE, 0, 0, 80, 112, 16, 16 ,0)
            pyxel.blt(26 * TILE, 0, 0, 64, 112, 16, 16 ,0)
            pyxel.blt(28 * TILE, 0, 0, 96, 112, 16, 16 ,0)
            pyxel.blt(30 * TILE, 0, 0, 64, 112, 16, 16 ,0)
            pyxel.blt(32 * TILE, 0, 0, 80, 112, 16, 16 ,0)
            
            pyxel.blt(34 * TILE, 0, 0, self.level * 16, 128, 16, 16, 0)
    
   
    #animation pour afficher les coeurs
            if self.life >= 1 :
                pyxel.blt(0, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(0, 0, 0, 16, 16, 16, 16, 0)
            if self.life >= 2 :
                pyxel.blt(16, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(16, 0, 0, 16, 16, 16, 16, 0)
            if self.life >= 3:
                pyxel.blt(32, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(32, 0, 0, 16, 16, 16, 16, 0)
                
    #affichage "SCORE"
            pyxel.blt(50 * TILE, 0, 0, 0, 112, 16, 16, 0)
            pyxel.blt(52 * TILE, 0, 0, 16, 112, 16, 16, 0)
            pyxel.blt(54 * TILE, 0, 0, 32, 112, 16, 16, 0)
            pyxel.blt(56 * TILE, 0, 0, 48, 112, 16, 16, 0)
            pyxel.blt(58 * TILE, 0, 0, 64, 112, 16, 16, 0) 
            
    #affichage score
            if self.d <= 4:
                pyxel.blt(60 * TILE, 0, 0, self.d * 16, 128, 16, 16, 0)
            else:
                pyxel.blt(60 * TILE, 0, 0, (self.d - 5) * 16, 144, 16, 16, 0)
            if self.u <= 4:
                pyxel.blt(62 * TILE, 0, 0, self.u * 16, 128, 16, 16, 0)
            else:
                pyxel.blt(62 * TILE, 0, 0, (self.u - 5) * 16, 144, 16, 16, 0)    
                
    #affichage des enemies et des fruits seulement que le jeu est lancé
    # x, y, img, u, v, width, height, transparent color
            if self.game_over == False and self.level_up == False:
                for enemy in self.enemies_list:
                    pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 11)
                    
                for fruit in self.fruits_list:
                    pyxel.blt(fruit[0], fruit[1], 0, 32, 16, 16, 16, 0)
      
        
                
                    
        
        
App()