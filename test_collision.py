import pyxel

SCROLL = 40
TILE_FLOOR = (1, 0)
WALL = (0, 1)

scroll_x = 0
player = None

def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
    
# Selon les coordonnées de joueur, indentifié ses tuiles voisins, et renvoyer Vrai ou Faux pour la collision
#WALL = On ne peut pas traverser de n'importe quel sens, FLOOR = On peut traverser sauf de haut vers le bas
def is_colliding(x, y, is_falling):
    x1 = x // 8
    x2 = (x + 7)// 8
    y1 = y // 8
    y2 = (y + 7)// 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi) == WALL:
                return True
        if is_falling and y % 8 == 1:
            for xi in range(x1, x2 + 1):
                if get_tile(xi, y1 + 1) == TILE_FLOOR:
                    return True
    return False
    
def push_back(x, y, dx, dy):
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_colliding(x, y + step, dy > 0):
            break
        y += step
        dy -= step
    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_colliding(x + step, y, dy > 0):
            break
        x += step
        dx -= step
    return x, y



class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = False
        
    def update(self):
        global scroll_x
        last_y = self.y
        
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2
            self.direction = 1
            
        self.dy = min(self.dy + 1, 3)
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.dy = -6
            
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy)
            
        if self.y < 0:
            self.y = 0
        if self.x < 0:
            self.x = 0
        
        self.dx = int(self.dx * 0.8)  
        self.is_falling = self.y > last_y
        
        if self.y >= pyxel.height:
            game_over()
            
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, 8 * self.direction, 8, 0)
        
class App:
    def __init__(self):
        pyxel.init(128, 128, title="Test")
        pyxel.load("res.pyxres")
        
        global player
        player = Player(0, 0)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        
        player.update()
        global scroll_x
        if player.x < scroll_x + SCROLL:
            scroll_x = max(0, player.x - SCROLL)
        if player.x > scroll_x + pyxel.width - SCROLL:
            scroll_x = min(player.x - pyxel.width + SCROLL, pyxel.tilemap(0).width * 8 - pyxel.width)
        
    def draw(self):
        
        pyxel.cls(0)
        
        pyxel.camera()
        pyxel.bltm(0, 0, 0, scroll_x, 0, 128, 128, 0)
        
        pyxel.camera(scroll_x, 0)
        player.draw()
        
        pyxel.text(5 + scroll_x, 5, f"X: {player.x} Y: {player.y}", 7)
        pyxel.text(5 + scroll_x, 15, f"DX: {player.dx} DY: {player.dy}", 7)
        pyxel.text(5 + scroll_x, 25, f"Scroll: {scroll_x}", 7)

        
            
def game_over():
    global scroll_x, enemies
    scroll_x = 0
    player.x = 0
    player.y = 0
    player.dx = 0
    player.dy = 0
    
App()