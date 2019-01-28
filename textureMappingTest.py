import pygame
try:
	import numpy
except:
	print("It seems you do not have numpy installed.\nRun pip install numpy")
from pygame import surfarray
from textureMapping import textureMap
import math
from math import sin, cos
import time

pygame.init()

size = w, h = 500, 500
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
texture = pygame.image.load("test.jpg")


print(texture)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    t = sin(time.time()*30)
    timer = time.time()
    screen.fill(black)
    
    
    textureMap(screen,texture,((-30,10),(32,10),(40,150),(35,40)))
    #textureMap(screen,texture,((50,50),(80,40),(50,70),(80,70)))
    #textureMap(screen,texture,((10,10),(30,10),(5,40),(35,40)))
    textureMap(screen,texture,((-5,200),(250,150),(302,231),(-5,250)))

    textureMap(screen,texture,((200,200),(570,150),(302,231),(200,250)))

    pygame.display.flip()

    print(time.time()-timer)