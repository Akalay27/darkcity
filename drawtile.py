'''

Copyright © 2019 Adam Kalayjian

Darkcity

'''
import sys, pygame
import math
from random import randint, random
from pygame import draw
import time
from pygame import gfxdraw,surfarray
import constants
from constants import *
from textureMapping import textureMap
black = (0,0,0)



def aaPoly(screen,color,points,linewidth=0):
	draw.polygon(screen,color,points,linewidth)
	gfxdraw.aapolygon(screen,points,color)

def drawBuilding(screen,b,x,y,perspectiveAmount,shading):
	x+=b.xOffset
	y+=b.yOffset
	#draw.rect(screen,red,(x,y,b.length,b.width),3)

	corners = ((x,y+b.width),(x,y),(x+b.length,y),(x+b.length,y+b.width))
	topCorners = []
	perspective = (width/2,height/2)
	deltaView = x+b.width/2-perspective[0],y+b.length/2-perspective[1] #CENTER OF BUILDING CALC
	#deltaView = c[0]-perspective[0],c[1]-perspective[1] #EACH CORNER CALC
	distance = math.sqrt((x+b.width/2-perspective[0])**2 + (y+b.length/2-perspective[1])**2)/perspectiveAmount
	angle = math.atan2(deltaView[1],deltaView[0]) #FOR EACH CORNER
	for c in corners:
		#print(c)
		#draw.circle(screen,blue,c,1)
		#deltaView = (c[0]-mouseX,c[1]-mouseY)
		
		
		
		topCorner = (c[0]+math.cos(angle)*b.height*distance,c[1]+math.sin(angle)*b.height*distance)
		#draw.line(screen,white,c,topCorner,2)
		topCorners.append((round(topCorner[0]),round(topCorner[1])))
	# [1]     [2]
	#
	#
	# [0]     [3]
	#

	sidesVisible = [0,0,0,0]
	if (angle >= 0 and angle <= math.pi/2):
		sidesVisible = [1,0,0,1]
	elif (angle >= math.pi/2 and angle <= math.pi):
		sidesVisible = [1,1,0,0]
	elif (angle <= 0 and angle >= -math.pi/2):
		sidesVisible = [0,0,1,1]
		
	else:
		sidesVisible = [0,1,1,0]
	if (sidesVisible[0]): 
		aaPoly(screen,b.shading["north"],(corners[1],corners[2],topCorners[2],topCorners[1]))
		textureMap(screen,b.textures["north"],(corners[1],corners[2],topCorners[2],topCorners[1]))
	if (sidesVisible[1]): 
		aaPoly(screen,b.shading["east"], (corners[2],corners[3],topCorners[3],topCorners[2]))
		textureMap(screen,pygame.transform.rotate(b.textures["east"],90),(topCorners[2],corners[2],corners[3],topCorners[3]))
	if (sidesVisible[2]): 
		aaPoly(screen,b.shading["south"],(corners[3],corners[0],topCorners[0],topCorners[3]))
		textureMap(screen,b.textures["south"],(topCorners[0],topCorners[3],corners[3],corners[0]))
	if (sidesVisible[3]): 
		aaPoly(screen,b.shading["west"],(corners[1],corners[0],topCorners[0],topCorners[1]))
		textureMap(screen,pygame.transform.rotate(b.textures["west"],-90),(corners[1],topCorners[1],topCorners[0],corners[0]))
	aaPoly(screen,b.shading["top"],topCorners)
	screen.blit(b.textures["top"],topCorners[1])
def aaEllipse(screen,color,rect): # unused
	draw.ellipse(screen,color,rect)
	gfxdraw.aaellipse(screen,int(rect[0]+rect[2]/2),int(rect[1]+rect[3]/2),int(rect[2]/2),int(rect[3]/2),color)
def drawRoad(screen,r,x,y): #should probably be storing this function inside of the road class, but no
	#borders/lanes first
	colors = roadColors
	#BORDERS:
	spacing = (tileSize-distanceFromSide*2)//(r.lanes+1)
	if (r.direction == 0):
		draw.line(screen,colors["side"],(x+distanceFromSide,y),(x+distanceFromSide,y+tileSize),2)
		draw.line(screen,colors["side"],(x+tileSize-distanceFromSide,y),(x+tileSize-distanceFromSide,y+tileSize),2)

		for l in range(0,r.lanes):
			draw.line(screen,colors["lane"],(x+distanceFromSide+((l+1)*spacing),y),(x+distanceFromSide+((l+1)*spacing),y+tileSize),2)
	if (r.direction == 1):
		#print("SIDEWAYS")
		draw.line(screen,colors["side"],(x,y+distanceFromSide),(x+tileSize,y+distanceFromSide),2)
		draw.line(screen,colors["side"],(x,y+tileSize-distanceFromSide),(x+tileSize,y+tileSize-distanceFromSide),2)
		for l in range(0,r.lanes):
			draw.line(screen,colors["lane"],(x,y+distanceFromSide+((l+1)*spacing)),(x+tileSize,y+distanceFromSide+((l+1)*spacing)),2)
	if (r.direction == 2):
		corners = [(x+distanceFromSide,y+distanceFromSide),(x+tileSize-distanceFromSide,y+distanceFromSide),(x+tileSize-distanceFromSide,y+tileSize-distanceFromSide),(x+distanceFromSide,y+tileSize-distanceFromSide)]
		for c in corners:
			draw.circle(screen,colors["side"],c,3) 
			gfxdraw.aacircle(screen,c[0],c[1],3,colors["side"])
	#see, I did use 5+ circles!
