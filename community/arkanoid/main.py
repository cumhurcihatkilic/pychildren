import pygame,sys
import math
import random
from pygame.locals import *
# import pygame.mixer


try :
    import android
except ImportError :
    android = None
    
pygame.init()

# try:
#     import pygame.mixer as mixer
# except ImportError:
#     import android.mixer as mixer

# mixer.init()

if android :
    android.init()
    android.map_key(android.KEYCODE_BACK,pygame.K_ESCAPE)
clock = pygame.time.Clock()

WIDTH=480
HEIGHT=320
PADDLE_WIDTH = 50
PADDLE_HEIGHT = 20
balle_size = [15,15]
BLUE=(0,0,255)
RED=(255,0,0)
GREEN =(0,255,0)
BLACK=(0,0,0)
speed = 7
direction = "stop"
brique_size = [29,13]



fenetre= pygame.display.set_mode((WIDTH,HEIGHT),RESIZABLE)
pygame.display.set_caption("Arkanoid !!")

bg_img = pygame.image.load("background.jpg").convert()
bg_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

paddle_img = pygame.image.load("pad.png").convert_alpha()
paddle_pos = [WIDTH/2,HEIGHT-PADDLE_HEIGHT]
paddle_rect = pygame.Rect(paddle_pos[0],paddle_pos[1],PADDLE_WIDTH,PADDLE_HEIGHT)

# for a mobile telephone
leftarrow_img = pygame.image.load("leftarrow.png").convert_alpha()
left_rect = pygame.Rect(0,HEIGHT-50,50,50)
rightarrow_img = pygame.image.load("rightarrow.png").convert_alpha()
right_rect = pygame.Rect(WIDTH-50, HEIGHT-50, 50,50)

ball_img = pygame.image.load("ball2.png").convert_alpha()


brique_transparente_img = pygame.image.load("brique_transparente.png").convert_alpha()
brique_bleue_img = pygame.image.load("brique_bleue.png").convert()
brique_jaune_img = pygame.image.load("brique_jaune.png").convert()
brique_noire_img = pygame.image.load("brique_noire.png").convert()
class Brique:
    def __init__(self,image,position,hitable,hit=0,bonusable= False):
        self.image = image
        self.pos = position
        self.hitable = hitable
        self.hit = hit
        self.bonusable = bonusable
    def afficher(self,brique_rect,fenetre):
        global brique_size
        brique_rect = pygame.Rect(self.pos[0],self.pos[1],brique_size[0],brique_size[1])
        self.fenetre.blit(self.image,brique_rect)       

class Ball :
    def __init__(self,image,pos,vel,radius):
        self.image = image
        self.pos = pos
        self.vel = vel
        self.radius = radius
    def get_pos(self):
        return self.position
    def set_pos(self,new_pos):
        self.position = new_pos
    def set_vel(self, new_vel):
        self.vel = new_vel

        
balle_vel = [random.randrange(2,5),random.randrange(1,5)]

balle = Ball(ball_img,[WIDTH/2, HEIGHT/2],balle_vel,balle_size[0])
     
#### level 1
# 0 = transparente
# 1 = bleue
# 2 = jaune
# 3 = noire
level1=[
    [1,1,1,1,0,1,0,1,0,1],
    [1,0,0,1,0,1,0,1,0,1],
    [1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,1,0,1]
    ]
    
li=0
col=0
brique_pos=[]
for ligne in level1 :
    for sprite in ligne :
        x = col * brique_size[0]+2
        y = li * brique_size[1]+2
        
        if sprite == 0 :
            brique_pos.append([brique_transparente_img,[100+x,50+y]])
        elif  sprite == 1 :
            brique_pos.append([brique_bleue_img,[100+x,50+y]])
        elif  sprite == 2 : 
            brique_pos.append([brique_jaune_img,[100+x,50+y]])
        elif  sprite == 3 : 
            brique_pos.append([brique_noire_img,[100+x,50+y]])
        col = (col+1)%len(level1[0])
    li += 1




continuer = True



while True:
    clock.tick(30)
    fenetre.blit(bg_img,bg_rect)
    # if we use keys for moving paddle
    keys=pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                pygame.quit()
                sys.exit()


             
                
#test si souris hors de l ecran 
    if mouse_pos[0]<0 or mouse_pos[0]> WIDTH:
        mouse_pos[0] = WIDTH /2
        
    if mouse_pos[1]<0 or mouse_pos[1]> HEIGHT:
        mouse_pos[1] = HEIGHT /2

#test si souris sur carre gauche ou droite ou hors carre et affectation direction   
    if left_rect.collidepoint(mouse_pos) or keys[K_LEFT] :
        direction = "left"   
    elif right_rect.collidepoint(mouse_pos) or keys[K_RIGHT] :
        direction = "right"
    else :
        direction = "stop"
        
#limitation du paddle a droite et gauche
    if direction == "left" and paddle_rect.left-speed >=0:
        paddle_pos[0] -= speed
    elif direction == "left" and paddle_rect.left-speed <0 :
        paddle_pos[0] = 0
        direction = "stop"
    elif direction == "right" and paddle_rect.right+speed <=WIDTH:
        paddle_pos[0] += speed
        direction = "stop"
    elif direction == "right" and paddle_rect.right+speed >WIDTH:
        paddle_pos[0] = WIDTH - PADDLE_WIDTH
        direction = "stop" 
#affichage

    balle_rect = pygame.Rect(balle.pos[0],balle.pos[1],balle_size[0],balle_size[1])   
    #fenetre.fill(BLACK)
    balle.pos[0] = balle.pos[0] + balle.vel[0]
        
#bricks draw, and collision test    
    for brique in brique_pos :
        
        fenetre.blit(brique[0],(brique[1][0],brique[1][1]))
        brique_rect = brique[0].get_rect()
        brique_rect.topleft=(brique[1][0],brique[1][1])
        if brique_rect.colliderect(balle_rect) and brique[0]!= brique_transparente_img :
            brique_pos.remove(brique)
            balle.vel[0]= - balle.vel[0]
            balle.vel[1]= - balle.vel[1]
            
    
    paddle_rect = pygame.Rect(paddle_pos[0],paddle_pos[1],PADDLE_WIDTH,PADDLE_HEIGHT)
    

#balle
    
    balle.pos[0] = balle.pos[0] + balle.vel[0]
    balle.pos[1] = balle.pos[1] + balle.vel[1]
#bounce if reach top of window
    if  balle.pos[1] < 0 :
        balle.vel[1] = - balle.vel[1]
#bounce if reach left or right side of window
    if balle.pos[0]< 0 or balle.pos[0]+balle_size[0] > WIDTH:
        balle.vel[0] = - balle.vel[0]
#bounce if on the paddle   
    if balle_rect.bottom < HEIGHT - PADDLE_HEIGHT and balle_rect.bottom + balle.vel[1]>=HEIGHT-PADDLE_HEIGHT :
        
        if balle.pos[0]+balle_size[0]>=paddle_pos[0] and balle.pos[0]<=paddle_pos[0] + PADDLE_WIDTH:
            
            balle.pos[1] = HEIGHT - PADDLE_HEIGHT - balle_size[1]
            if direction == "right" and balle.vel[0]>=0:
                balle.vel[0] = balle.vel[0] + 0.4*speed
            elif direction == "right" and balle.vel[0]<0:
                balle.vel[0] = balle.vel[0] - 0.4*speed
            elif direction == "left" and balle.vel[0]<0:
                balle.vel[0] = balle.vel[0] - 0.4*speed
            elif direction == "left" and balle.vel[0]>=0:
                balle.vel[0] = balle.vel[0] + 0.4*speed
            else :
                balle.vel[0] = balle.vel[0] - 0.1*speed

            balle.vel[1] = - balle.vel[1]
    if balle_rect.bottom > HEIGHT:
        balle_vel = [random.randrange(2,5),random.randrange(2,5)]
        balle = Ball(ball_img,[WIDTH/2, HEIGHT/2],balle_vel,balle_size[0])

            
    
    pygame.draw.rect(fenetre,BLUE,left_rect)
    pygame.draw.rect(fenetre,GREEN,right_rect)
    fenetre.blit(leftarrow_img,left_rect)
    fenetre.blit(rightarrow_img,right_rect)
    fenetre.blit(paddle_img,paddle_rect)
    fenetre.blit(balle.image,balle_rect)
    pygame.display.flip()
