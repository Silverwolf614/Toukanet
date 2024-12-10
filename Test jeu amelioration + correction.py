import pyxel
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Ce que tu as fait c'est pas mal
#mais l'inconvénient de ne pas dessiner le tilemap 
#c'est qu'on ne peut pas faire des slide screen pour vrai
#là ce que j'ai fait c'est comme une démonstration ou quoi

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

        # Place de camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Variables du joueur
        self.player_width = 8
        self.player_height = 8
        self.player_x = 60 # Position initiale du joueur
        self.player_y = SCREEN_HEIGHT - self.player_height - 8 # Position initiale du joueur sur le sol
        self.velocity_y = 0 # Vitesse verticale du joueur
        self.is_jumping = False 
        # Définition de la scène : ici on ajoute une plateforme et un décor
        pyxel.run(self.update, self.draw)
    # Mise à jour de la logique du jeu : contrôles et physique
    def update(self):
    
        # Déplacement à gauche/droite avec les flèches
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += MOVE_SPEED
    
        # Saut avec la barre d'espace
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
    
        # Appliquer la gravité
        self.velocity_y += GRAVITY
        self.player_y += self.velocity_y
    
        # Empêcher le joueur de sortir de l'écran horizontalement
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > SCREEN_WIDTH - self.player_width:
            self.player_x = SCREEN_WIDTH - self.player_width
    
        # Collision avec le sol ou les plateformes
        if self.player_y >= SCREEN_HEIGHT - self.player_height - 8: # Si le joueur touche le sol
            self.player_y = SCREEN_HEIGHT- self.player_height - 8
            self.is_jumping = False
            self.velocity_y = 0
        # Mise à jour de la place de camera
        self.camera_x = self.player_x - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(self.camera_x, MAP_WIDTH - SCREEN_WIDTH))
        
    def draw(self):
        pyxel.cls(0) # Efface l'écran avec une couleur de fond noire
        # Répétition d'un décor simple
        for i in range(0, MAP_WIDTH, 16):
            pyxel.rect(i - self.camera_x, SCREEN_HEIGHT - 16, 16, 16, 7)  # sol
            if i % 32 == 0:  # les petits arbres
                pyxel.rect(i - self.camera_x, SCREEN_HEIGHT - 32, 8, 16, 3)
    
        # Dessiner le joueur
        pyxel.rect(
            self.player_x - self.camera_x,
            self.player_y - self.camera_y,
            self.player_width,
            self.player_height,
            11) # Le joueur est un carré blanc 
        
        # Afficher les coordonnées du joueur en haut à gauche pour repère
        pyxel.text(5, 5, f"X: {self.player_x} Y: {self.player_y}", 7)
    

App()
