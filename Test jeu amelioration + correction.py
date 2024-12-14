
import pyxel

WALL = (0, 1)
CORRIDOR = (0, 0)
# Configuration de la fenêtre et de l'environnement du jeu
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
MAP_WIDTH = 320 # Largeur de map(plus grand que l'écran)
MAP_HEIGHT = 120 # Longueur de map(même que l'écran)
GRAVITY = 0.5
JUMP_STRENGTH = -6
MOVE_SPEED = 2
class App:
    def __init__(self):
        # Initialisation de Pyxel
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Toukanet")
        pyxel.load("res.pyxres")
        self.x = 0
        self.x1 = 0
        self.x2 = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.tile = (0, 0)
        # Place de camera
        self.camera_x = 0
        self.camera_y = 0
        # Variables du joueur
        self.player_width = 8
        self.player_height = 8
        self.player_x = 60 # Position initiale du joueur
        self.player_y = SCREEN_HEIGHT - self.player_height - 8 # Position initiale du joueur sur le sol
        self.new_x = 0
        self.new_y = 0
        self.velocity_y = 0 # Vitesse verticale du joueur
        self.is_jumping = False 
        
        pyxel.run(self.update, self.draw)
    # Mise à jour de la logique du jeu : contrôles et physique
    def update(self):
    
        # Déplacement à gauche/droite avec les flèches
        self.new_x = self.player_x
        self.new_y = self.player_y
        
        if pyxel.btn(pyxel.KEY_LEFT):
            self.new_x -= MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.new_x += MOVE_SPEED

        # Saut avec la barre d'espace
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

        # Appliquer la gravité
        self.velocity_y += GRAVITY
        self.new_y += self.velocity_y

        # Collision horizontale

        self.x = self.new_x // 8
        self.y1 = self.player_y // 8
        self.y2 = (self.player_y + self.player_height - 1) // 8

            # Vérifie les tuiles dans la direction horizontale
        if (pyxel.tilemap(0).pget(self.x, self.y1) == WALL or pyxel.tilemap(0).pget(self.x, self.y2) == WALL):
            self.new_x = self.player_x  
    # Bloque le mouvement horizontal

        # Collision verticale
        self.x1 = self.player_x // 8
        self.x2 = (self.player_x + self.player_width - 1) // 8
        self.y = self.new_y // 8

            # Vérifie les tuiles dans la direction verticale
        if (pyxel.tilemap(0).pget(self.x1, self.y) == WALL or
            pyxel.tilemap(0).pget(self.x2, self.y) == WALL):
            if self.velocity_y > 0:  # Collision depuis le haut
                self.new_y = self.y * 8 - self.player_height
                self.velocity_y = 0
                self.is_jumping = False
            elif self.velocity_y < 0:  # Collision depuis le bas
                self.new_y = (self.y + 1) * 8
                self.velocity_y = 0

        # Met à jour les coordonnées du joueur
        self.player_x = self.new_x
        self.player_y = self.new_y

        # Mise à jour de la caméra
        self.camera_x = max(0, min(self.player_x - SCREEN_WIDTH // 2, MAP_WIDTH - SCREEN_WIDTH))
        
    def draw(self):
        pyxel.cls(0) # Efface l'écran avec une couleur de fond noir
        pyxel.bltm(0, 0, 0, self.camera_x, self.camera_y, MAP_WIDTH, MAP_HEIGHT)
        # Dessiner le joueur
        pyxel.blt(
            self.player_x - self.camera_x,
            self.player_y - self.camera_y,
            0,
            8,
            0,
            self.player_width,
            self.player_height,
            0) # Le joueur est un carré blanc 
        
        # Afficher les coordonnées du joueur en haut à gauche pour repère
        pyxel.text(5, 5, f"X: {self.player_x} Y: {self.player_y}", 7)
    

App()
