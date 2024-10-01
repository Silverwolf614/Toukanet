import pyxel
import random

TILE = 8
MAP_WIDTH = 64
MAP_HEIGHT = 48

class Player1:
    
    width = 8
    heigth = 8
    
    def __init__(self):
        
        self.x = MAP_WIDTH * TILE / 2
        self.y = MAP_HEIGHT * TILE - 16
        self.DX = 5
        self.DY = 7
        self.flying = False
        self.direction = 1
        self.life = 3

    def update(self):
#platform y = -136        
        self.flying = False
        if self.y < 367 :
            self.y = (self.y + 2) % pyxel.height
            
        if pyxel.btn(pyxel.KEY_Z):
            if self.y > 8:
                self.y = self.y - self.DY
                self.flying = True
#valeur = width - 16               
        if pyxel.btn(pyxel.KEY_S):
            if self.y < 340:
                self.y = self.y + self.DY
#valeur = width - 16             
        if pyxel.btn(pyxel.KEY_D):
            self.x = min(TILE * MAP_WIDTH - 16, self.x + self.DX)
            self.direction = 1
                
        if pyxel.btn(pyxel.KEY_Q):
            self.x = max(0, self.x - self.DX)
            self.direction = -1

    def draw(self):
        if self.flying:
            if pyxel.frame_count % 6 < 3:
                pyxel.blt(self.x, self.y, 0, 0, 0, self.direction * 16, 16, 7)
            else:
                pyxel.blt(self.x, self.y, 0, 16, 0, self.direction * 16, 16, 7)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, self.direction * 16, 16, 7)

class Player2:
    
    width = 8
    heigth = 8
    
    def __init__(self):
        
        self.x = MAP_WIDTH * TILE / 2
        self.y = MAP_HEIGHT * TILE - 16
        self.DX = 5
        self.DY = 7
        self.flying = False
        self.direction = 1
        self.life = 3

    def update(self):
#platform y = -136        
        self.flying = False
        if self.y < 367 :
            self.y = (self.y + 2) % pyxel.height
            
        if pyxel.btn(pyxel.KEY_UP):
            if self.y > 8:
                self.y = self.y - self.DY
                self.flying = True
#valeur = width - 16               
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.y < 340:
                self.y = self.y + self.DY
#valeur = width - 16             
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(TILE * MAP_WIDTH - 16, self.x + self.DX)
            self.direction = 1
                
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - self.DX)
            self.direction = -1

    def draw(self):
        if self.flying:
            if pyxel.frame_count % 6 < 3:
                pyxel.blt(self.x, self.y, 0, 0, 32, self.direction * 16, 16, 7)
            else:
                pyxel.blt(self.x, self.y, 0, 16, 32, self.direction * 16, 16, 7)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 32, self.direction * 16, 16, 7)


class App:
    
    def __init__(self):
        #init(width, height, [title], [fps], [quit_key], [display_scale], [capture_scale], [capture_sec])
        pyxel.init(MAP_WIDTH * TILE, MAP_HEIGHT * TILE, fps=30)
        pyxel.load("toukanet.pyxres")
        self.player1 = Player1()
        self.player2 = Player2()
        
        
        self.enemies_list = []
        self.apples_list = []
        self.collisions_list = []
        
        pyxel.run(self.update, self.draw)
        
    def enemy_create(self):
        
        if (pyxel.frame_count % 15 == 0):
            self.enemies_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
    
    def apple_create(self):
        if (pyxel.frame_count % 60 == 0):
            self.apples_list.append([random.randint (0, TILE * MAP_WIDTH - 16), 0])
            
    def enemy_move(self):
        for enemy in self.enemies_list:
            enemy[1] += 3
            if enemy[1] > TILE * MAP_HEIGHT:
                self.enemies_list.remove(enemy)
    
    def apple_move(self):
        for apple in self.apples_list:
            apple[1] += 3
            if apple[1] > TILE * MAP_HEIGHT:
                self.apples_list.remove(apple)
                
    def enemy_collision(self):
        
        for enemy in self.enemies_list:
            if enemy[0] <= self.player1.x + 16 and enemy[1] <= self.player1.y + 16 and enemy[0] + 8 >= self.player1.x and enemy[1] + 16 >= self.player1.y :
                self.enemies_list.remove(enemy)
                self.player1.life -= 1
        
        for enemy in self.enemies_list:
            if enemy[0] <= self.player2.x + 16 and enemy[1] <= self.player2.y + 16 and enemy[0] + 8 >= self.player2.x and enemy[1] + 16 >= self.player2.y :
                self.enemies_list.remove(enemy)
                self.player2.life -= 1
    
    def apple_collision(self):
        
        for apple in self.apples_list:
            if apple[0] <= self.player1.x + 16 and apple[1] <= self.player1.y + 16 and apple[0] + 8 >= self.player1.x and apple[1] + 8 >= self.player1.y :
                self.apples_list.remove(apple)
                if self.player1.life != 3 :
                    self.player1.life += 1

        for apple in self.apples_list:
            if apple[0] <= self.player2.x + 16 and apple[1] <= self.player2.y + 16 and apple[0] + 8 >= self.player2.x and apple[1] + 8 >= self.player2.y :
                self.apples_list.remove(apple)
                if self.player2.life != 3 :
                    self.player2.life += 1
                
    def update(self):
        self.player1.update()
        self.player2.update()
        self.enemy_create()
        self.enemy_move()
        self.enemy_collision()
        self.apple_create()
        self.apple_move()
        self.apple_collision()
        
    def draw(self):
        pyxel.cls(11)
        pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
        for enemy in self.enemies_list:
                pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 0)
            
        for apple in self.apples_list:
            pyxel.blt(apple[0], apple[1], 0, 40, 0, 8, 8, 0)
        
        if self.player1.life > 0 :
            
            self.player1.draw()
            if self.player1.life >= 1 :
                pyxel.blt(0, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(0, 0, 0, 16, 16, 16, 16, 0)
            if self.player1.life >= 2 :
                pyxel.blt(16, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(16, 0, 0, 16, 16, 16, 16, 0)
            if self.player1.life == 3:
                pyxel.blt(32, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(32, 0, 0, 16, 16, 16, 16, 0)

            
            
        else:
            pyxel.bltm(0, 0, 7, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
        
        if self.player2.life > 0 :
            self.player2.draw()
            if self.player2.life >= 1 :
                pyxel.blt(496, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(496, 0, 0, 16, 16, 16, 16, 0)
            if self.player2.life >= 2 :
                pyxel.blt(480, 0, 0, 0, 16, 16, 16, 0)
            else:
                pyxel.blt(480, 0, 0, 16, 16, 16, 16, 0)
            if self.player2.life == 3:
                pyxel.blt(464, 0, 0, 0, 16, 16, 16, 0)
                
            else:
                pyxel.blt(464, 0, 0, 16, 16, 16, 16, 0)
App()


        



        
    




