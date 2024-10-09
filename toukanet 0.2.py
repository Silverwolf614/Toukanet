import pyxel
import random
#first project version 0.2

TILE = 8
MAP_WIDTH = 64
MAP_HEIGHT = 48

class Player:
    
    width = 8
    heigth = 8
    
    def __init__(self):
        
        self.x = 0
        self.y = 0
        self.DX = 5
        self.DY = 7
        self.flying = False
        self.direction = 1

    def update(self):
        
        self.flying = False
        if self.y < 367:
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
        self.alive = True
        
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
        
    def player_collision(self):
        
        for enemy in self.enemies_list:
            if enemy[0] <= self.player.x + 16 and enemy[1] <= self.player.y + 16 and enemy[0] + 8 >= self.player.x and enemy[1] + 16 >= self.player.y :
                self.enemies_list.remove(enemy)
                self.alive = False
    def update(self):
        self.player.update()
        self.enemy_create()
        self.enemy_move()
        self.player_collision()
        
    def draw(self):
        pyxel.cls(11)
        if self.alive == True :
            pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH * TILE, MAP_HEIGHT * TILE)
            self.player.draw()
            
            for enemy in self.enemies_list:
                pyxel.blt(enemy[0], enemy[1], 0, 32, 0, 8, 16, 0)
                
        else:
            
            pyxel.text(178, 192, 'GAME OVER', 7)

        
        
App()


        



        
    




