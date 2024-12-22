import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.font.init()
MYFONT = pygame.font.SysFont("Arial", 30)

FPS = 60
FramesPerSec = pygame.time.Clock()

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLUE)
pygame.display.set_caption("RichyP")

OUT_OF_BOUNDS_event = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    SPEED_Y = 0
    SCORE = 0
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.SPEED_Y = 0
        self.SCORE = 0
        self.rect.center = (40, SCREEN_HEIGHT / 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):
        self.rect.move_ip(0, self.SPEED_Y)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top + self.rect.height > SCREEN_HEIGHT:
            self.rect.top = SCREEN_HEIGHT - self.rect.height

class Ball(pygame.sprite.Sprite):

    SPEED_X = -5
    SPEED_Y = 2

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.reset()

    def move(self):
        self.rect.move_ip(self.SPEED_X,self.SPEED_Y)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.SPEED_Y = -self.SPEED_Y
        if self.rect.top < 0:
            self.SPEED_Y = -self.SPEED_Y

        if self.rect.left < 0:
            pygame.event.post(pygame.event.Event(OUT_OF_BOUNDS_event))

        if self.rect.left + self.rect.width > SCREEN_WIDTH:
            self.SPEED_X = -self.SPEED_X
            self.SPEED_Y = -(self.SPEED_Y + (random.randrange(8)-4))
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        SPEED_X = -5
        SPEED_Y = 2

P = Player()
B = Ball()

GAME_OVER = False

while True:
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                GAME_OVER = False
                P.reset()
                B.reset()
        if event.type == OUT_OF_BOUNDS_event:
            GAME_OVER = True
    
    keys = pygame.key.get_pressed()

    if GAME_OVER == False:
        s = 0
        if keys[K_UP]:
            s -= 5
        if keys[K_DOWN]:
            s += 5
   
        P.SPEED_Y = s

        if B.rect.colliderect(P.rect):
            P.SCORE += 1
            B.rect.center = (B.rect.centerx + 8, B.rect.centery)
            B.SPEED_X = -B.SPEED_X
            B.SPEED_Y = -B.SPEED_Y + (random.randrange(8)-4)

        P.move()
        B.move()
    else:
        text_surface2 = MYFONT.render("GAME OVER", False, WHITE)
        DISPLAYSURF.blit(text_surface2, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    P.draw(DISPLAYSURF)
    B.draw(DISPLAYSURF)
    text_surface = MYFONT.render("SCORE: " + str(P.SCORE), False, WHITE)
    DISPLAYSURF.blit(text_surface, (0,0))
    pygame.display.update()
    FramesPerSec.tick(FPS)
