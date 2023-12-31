from pygame.locals import *
import pygame
import pymunk
import time
import random

pygame.init()

WIDTH = 640
HEIGHT = 320
width_flow = 640
obs_position = 650


window = pygame.display.set_mode(size=(WIDTH, HEIGHT))

move_x = 320
move_y = 220

clock = pygame.time.Clock()

collision_tollerance_top = 10
collision_tollerance_side = 80

# Definição do objeto afetado pela gravidade
class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 0
        self.gravity = 0.5
        
        

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Impede que o objeto saia da parte inferior da janela
        if self.rect.bottom > 250:
            self.rect.bottom = 250
            self.velocity = 0

        if self.rect.x <= 0:
            self.rect.x *= -1
            

    def walk_right(self):
        self.rect.x += 0.1
    
    def walk_left(self):
        self.rect.x -= 0.1
    
    def jump(self):
        self.velocity = -10


class RigidBodyObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

def collider_func(player, obj):
    if player.rect.colliderect(obj.rect):
        if player.rect.bottom > obj.rect.top and abs(obj.rect.top - player.rect.bottom) < collision_tollerance_top:
            player.rect.bottom = obj.rect.top
            player.velocity = 0
        elif player.rect.right > obj.rect.left and abs(obj.rect.left - player.rect.right) < collision_tollerance_side and player.rect.x < obj.rect.x:
            player.rect.right = obj.rect.left

        elif player.rect.left < obj.rect.right and abs(obj.rect.right - player.rect.left) < collision_tollerance_side and player.rect.x > obj.rect.x:
            player.rect.left = obj.rect.right


def obs_generate(obsList):
    obs_heigh = random.randint(58, 78)
    obs_y = 250 - obs_heigh
    new_obstaculo = RigidBodyObject(obs_position, obs_y, 30, obs_heigh)
    obsList.append(new_obstaculo)


    return obsList


player = GameObject(320, 250, 50, 50)
obstaculoList = []
obs_generate(obstaculoList)


while(True):
    #ceu
    window.fill((0,204,204))
    #chao
    chao = pygame.draw.rect(window, (135,62,35), (0,250,width_flow,70))

    #obstaculo
    i = len(obstaculoList) - 1
    obstaculoobj = pygame.draw.rect(window, (204,0,0), obstaculoList[i])


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.jump()

            
    
    if pygame.key.get_pressed()[K_RIGHT]:
        obstaculoList[i].rect.x -= 5
        player.walk_right()

    if pygame.key.get_pressed()[K_LEFT]:
        print(i)
        obstaculoList[i].rect.x += 5
        player.walk_left()

    if obstaculoList[i].rect.x < 5:
        obstaculoList = obs_generate(obstaculoList)
        
    

    playerobj = pygame.draw.rect(window, (76,153,0), player.rect)
    collider_func(player, obstaculoList[i])


    #if playerobj.colliderect(obstaculoobj):

    player.update()
    
    pygame.display.flip()
    

    clock.tick(60)