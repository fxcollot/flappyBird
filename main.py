import pygame
import random
import time
from pygame.locals import *
from neuralNetwork import forward_propagation, last_network

HEIGHT = 336
WIDTH = 496
ACC = 0.5
FRIC = -0.12
FPS = 60

pygame.init()
vec = pygame.math.Vector2
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode( (WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class GenAI():
    def __init__(self, flappy, params):
        self.params = params
        self.surf = flappy
        self.rect = self.surf.get_rect(center = (WIDTH/6, HEIGHT/2))
        self.speed = 0
        self.X = [0, 0, self.speed, 0, 0]

    def flapChoice(self):
        output = forward_propagation(self.X, self.params)
        return output > 0.5

    def update(self,all_pipes):
        if all_pipes != []:
            self.X = [(self.rect.x[0]+self.rect.x[1]) / 2, (self.rect.y[0]+self.rect.y[1])/2, self.speed, (all_pipes[0].x[0]+all_pipes[0].x[1])/2, (all_pipes[0].y[1]+all_pipes[0].y[2])/2]
        if self.flapChoice():
            self.speed -= 4
        self.speed += 0.5
        self.rect.y -= self.speed

    def destroy(self):
        del self

class RandomAI(pygame.sprite.Sprite):
    def __init__(self, flappy):
        super().__init__()
        self.name = "randomAI"
        self.surf = flappy
        self.rect = self.surf.get_rect(center = (WIDTH/6, HEIGHT/2))
        self.speed = 0

    def update(self ,flappyUp, flappyDown):
        if random.randint(1, 20) > 19:
            self.speed -= 2
        if self.speed > 0:
            self.surf = flappyUp
        else:
            self.surf = flappyDown
        self.speed += 0.1
        self.rect.y += self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, flappy):
        super().__init__()
        self.name = "player"
        self.surf = flappy
        self.rect = self.surf.get_rect(center = (WIDTH/6, HEIGHT/2) )
        self.speed = 0

    def update(self, jump, flappyUp, flappyDown):
        if jump:
            self.speed = -2
        if self.speed > 0:
            self.surf = flappyUp
        else:
            self.surf = flappyDown
        self.speed += 0.1
        self.rect.y += self.speed

class Background(pygame.sprite.Sprite):
    def __init__(self, bg):
        super().__init__()
        self.surf = bg
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, pipeUp, pipeDown):
        super().__init__()
        self.speed = 2
        self.surfUp = pipeUp
        self.surfDown = pipeDown
        self.upper = self.surfUp.get_rect()
        self.downner = self.surfDown.get_rect()
        self.upper.x = 450
        self.upper.y = 60-height
        self.downner.x = 450
        self.downner.y = 200-height

    def update(self):
        self.upper.x -= self.speed
        self.downner.x -= self.speed
        if self.upper.x < 0:
            self.destroy()

    def destroy(self):
        self.kill()

def runGraphics(player):
    # Initialisation pygame
    pygame.init()
    vec = pygame.math.Vector2
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode( (WIDTH, HEIGHT))

    # Charger l'image Background
    bg = pygame.image.load("flappybirdBackground.png").convert_alpha()

    new_width = WIDTH
    new_height = HEIGHT
    new_bg = pygame.transform.scale(bg, (new_width, new_height))

    # Charger l'image de la pipe Up & Down
    pipeUp = pygame.image.load("./flappybirdPipe.png").convert_alpha()
    pipeDown = pygame.image.load("./flappybirdPipe.png").convert_alpha()

    pipe_width = 50
    pipe_height = 90
    tmp = pygame.transform.scale(pipeUp, (pipe_width, pipe_height)).convert_alpha()
    new_pipeUp = pygame.transform.rotate(tmp, 180).convert_alpha()
    new_pipeDown = pygame.transform.scale(pipeDown, (pipe_width, pipe_height)).convert_alpha()

    # Charger l'image Game Over
    game_over = pygame.image.load("./flappybirdGameOver.png").convert_alpha()

    # Initialisation du jeu
    
    background = Background(new_bg)
    all_sprites = pygame.sprite.Group()
    all_pipes = pygame.sprite.Group()

    all_sprites.add(background)
    all_sprites.add(player)

    running = True
    frame_counter = 59
    lpipes = []
    lost = False
    while running:
        jump = False
        frame_counter += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif ( event.type == KEYDOWN ) & ( player.name =="player" ):
                if event.key == K_SPACE:
                    jump = True

        if player.name == "randomAI":
            player.update(new_flappyUp, new_flappyDown)
        if player.name == "player":
            player.update(jump, new_flappyUp ,new_flappyDown)      
        all_pipes.update()

        if ( frame_counter == 60):
            lpipes.append(Pipe(random.randint(10, 50),new_pipeUp, new_pipeDown))
            all_pipes.add(lpipes[-1])  
            frame_counter = 0 

        # Mise à jour du jeu
        displaysurface.fill((135, 206, 235))  # Fond bleu ciel (SkyBlue)
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
        for entity in all_pipes:
            displaysurface.blit(entity.surfUp, entity.upper)
            displaysurface.blit(entity.surfDown, entity.downner)

        for pipe in all_pipes:
            if player.rect.colliderect(pipe.upper) or player.rect.colliderect(pipe.downner):
                player.speed = 0
                for entity in all_pipes:
                    entity.speed = 0
                lost = True         

        if player.rect.y > HEIGHT:
            lost = True 
                
        if lost:
            print("Perdu !")
            displaysurface.blit(game_over, (WIDTH/2, HEIGHT/2))
            pygame.display.flip()
            time.sleep(3)  
            pygame.quit()
            running = False
        else:
            pygame.display.flip()
            FramePerSec.tick(FPS)

    pygame.quit()


# Charger l'image du flappy
flappyDown = pygame.image.load("./flappybirdBirdDown.png").convert_alpha()
flappyUp = pygame.image.load("./flappybirdBirdUp.png").convert_alpha()

flappy_width = 30
flappy_height = 30
new_flappyDown = pygame.transform.scale(flappyDown, (flappy_width, flappy_height)).convert_alpha()
new_flappyUp = pygame.transform.scale(flappyUp, (flappy_width, flappy_height)).convert_alpha()

#player = Player(new_flappyDown)
player = RandomAI(new_flappyDown)


runGraphics(player)