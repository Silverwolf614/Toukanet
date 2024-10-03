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
        
        if self.x >= 0 and self.x <= 16 * TILE and self.y <= 15 * TILE and self.y >= 102:
            self.y = 102
        if self.x <= 512 and self.x >= 384 and self.y <= 15 * TILE and self.y >= 102:
            self.y = 102
        if self.x >= 0 and self.x <= 16 * TILE and self.y <= 31 * TILE and self.y >= 230:
            self.y = 230
        if self.x <= 512 and self.x >= 384 and self.y <= 31 * TILE and self.y >= 230:
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
                pyxel.blt(self.x, self.y, 0, 0, 0, self.direction * 16, 16, 7)
            else:
                pyxel.blt(self.x, self.y, 0, 16, 0, self.direction * 16, 16, 7)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, self.direction * 16, 16, 7)



class App:
    
    def __init__(self):
        #init(width, height, [title], [fps], [quit_key], [display_scale], [capture_scale], [capture_sec])
        pyxel.init(MAP_WIDTH * TILE, MAP_HEIGHT * TILE, fps=30)
        pyxel.load("res.pyxres")
        self.player = Player()
        self.life = 3
        
        self.enemies_list = []
        
        pyxel.run(self.update, self.draw)
        
    def enemy_create(self):
        
        if (pyxel.frame_count % 15 == 0):
            self.enemies_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
    
    def enemy_move(self):
        for enemy in self.enemies_list:
            enemy[1] += 3
            if enemy[1] > TILE * MAP_HEIGHT:
                self.enemies_list.remove(enemy)
    
    def enemy_collision(self):
        
        for enemy in self.enemies_list:
            if enemy[0] <= self.player.x + 16 and enemy[1] <= self.player.y + 16 and enemy[0] + 8 >= self.player.x and enemy[1] + 16 >= self.player.y :
                self.enemies_list.remove(enemy)
                self.life -= 1
    
    def update(self):
        self.player.update()
        self.enemy_create()
        self.enemy_move()
        self.enemy_collision()
        
    def draw(self):
        pyxel.cls(11)
        if self.life > 0 :
            pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.player.draw()
            if self.life >= 1 :
                pyxel.blt(0, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(0, 0, 0, 16, 16, 16, 16, 0)
            if self.life >= 2 :
                pyxel.blt(16, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(16, 0, 0, 16, 16, 16, 16, 0)
            if self.life == 3:
                pyxel.blt(32, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(32, 0, 0, 16, 16, 16, 16, 0)
            
            
            for enemy in self.enemies_list:
                pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 0)
            
        else:
            pyxel.bltm(0, 0, 7, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            pyxel.quit
        
        
App()


        



        
    



