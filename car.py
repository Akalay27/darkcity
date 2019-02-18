'''

Copyright © 2019 Adam Kalayjian

Darkcity

'''
import pygame
import math
from pygame import PixelArray, Color
from math import sin, cos,pi
from pygame import draw
from constants import *
from random import randint
import random
import sys
import time


def laneOffset(direction):
	spacing = (tileSize-distanceFromSide*2)//(4)/2
	if (direction == 1):
		return -spacing*(randint(0,1)*2+1)
	if (direction == -1):
		return spacing*(randint(0,1)*2+1)

mainCar = pygame.image.load("carMain.png")

hitBoxes = []


policeOff = pygame.transform.smoothscale(pygame.image.load("policeOff.png"),(60,60))
policeRed =pygame.transform.smoothscale(pygame.image.load("police1.png"),(60,60))
policeBlue = pygame.transform.smoothscale(pygame.image.load("police2.png"),(60,60))


def rotateAtCenter(image,angle):
	loc = image.get_rect().center
	rot_img = pygame.transform.rotate(image,angle)
	rot_img.get_rect().center = loc
	return rot_img,rot_img.get_rect(center=loc)

def drawCar(screen,tex,x,y,angle):
	rotated,rect = rotateAtCenter(tex,angle)
	w, h = tex.get_size()
	screen.blit(rotated,(x+rect.x-w/2,y+rect.y-h/2))
	bounds = hitBoxes[(int(angle)%360)]
	wb,hb = bounds.width,bounds.height
	bounds.x,bounds.y = (x-wb/2,y-hb/2)
	return bounds


def generateCar(color):
	c = mainCar.copy()
	pixels = PixelArray(c)
	pixels.replace(Color(0,255,0, 255), color,0)
	surf = pixels.make_surface()
	del pixels
	surf = pygame.transform.smoothscale(surf,(30,30))
	return surf
mc = pygame.transform.smoothscale(mainCar,(30,30))
for i in range(0,361):

	rotated,rect = rotateAtCenter(mc,i)
	hitBoxes.append(rotated.get_bounding_rect())
def collision(rect1,rect2,screen):
	if (rect1 == rect2):
		return False
	#print(rect1.x,rect1.y,rect1.x+rect1.width,rect1.y+rect1.height)
	#draw.rect(screen,(255,0,0),rect1,1)
	#draw.rect(screen,(255,255,255),rect2,5)
	for y in range(rect2.y,rect2.y+rect2.height,3):
		for x in range(rect2.x,rect2.x+rect2.width,3):
			#draw.circle(screen,(0,255,0),(x,y),2)
			if (rect1.collidepoint((x,y))):
				print((x,y)," collided.")
				print("Player Rect: ",rect1.x,rect1.y,rect1.x+rect1.width,rect1.y+rect1.height)
				print("NPC Rect: ",rect2.x,rect2.y,rect2.x+rect2.width,rect2.y+rect2.height)
				#draw.circle(screen,(255,0,0),(x,y),6)
				return True
	return False

	#print(rect1.center,rect2.center)
	

	
	#to improve, create matrix btwn  points so accurate collisions.

'''
o  o  o
o  o  o
o  o  o          <--
o  o  o 
test each one with collidepoint

'''

class car(object):
	def __init__(self, pos):
		
		self.pos = pos
		self.dir = 0
		self.speed = 0
		self.lastTilePos = (0,0)
		self.turnSpeed = 0
		self.turning = False
		self.texture = generateCar(Color(150,0,0))
	def playerControl(self,roads):
		
		keys = pygame.key.get_pressed()  #checking pressed keys for user-input camera movement
		if keys[pygame.K_UP]:
			self.speed+=0.03
		if keys[pygame.K_DOWN]:
			self.speed-=0.03
		
		self.turning = False
		if keys[pygame.K_LEFT]:
			self.dir+=self.turnSpeed*abs(self.speed)/3
			if (self.turnSpeed > -0.05):
				self.turnSpeed-=0.003
			self.turning = True
		if keys[pygame.K_RIGHT]:
			self.dir+=self.turnSpeed*abs(self.speed)/3
			if (self.turnSpeed < 0.05):
				self.turnSpeed+=0.003
			self.turning = True

		if (not self.turning):
			self.turnSpeed = 0
		self.speed*=0.98
		self.pos[0]+=(math.cos(self.dir)*self.speed)
		self.pos[1]+=(math.sin(self.dir)*self.speed)
		# if (self.vy > 0 and self.vx > 0):
		# 	movingDir = math.asin(self.vy/self.vx)
		# else:
		# 	movingDir = self.dir
		# # friction = math.fabs(movingDir-self.dir)
		# self.vx*=friction
		# self.vy*=friction

		




		tilePos = tileAt(self.pos)

		currentTile = city[tilePos]

		lastTile = city[self.lastTilePos]
		if (currentTile.ty == "building"):
			#print("HIT BUILDING")
			if (tilePos[0]-self.lastTilePos[0] == 1 or tilePos[0]-self.lastTilePos[0] == -1):
				self.speed*=-1
				self.pos[0]+=(math.cos(self.dir)*self.speed)*1.5
				self.pos[1]+=(math.sin(self.dir)*self.speed)*1.5
			if (tilePos[1]-self.lastTilePos[1] == 1 or tilePos[1]-self.lastTilePos[1] == -1):
				self.speed*=-1
				self.pos[0]+=(math.cos(self.dir)*self.speed)*1.5
				self.pos[1]+=(math.sin(self.dir)*self.speed)*1.5

		#print(tilePos,self.pos[1]/tileSize,currentTile.ty,currentTile.t)

		# if currentTile.ty == "building":
		# 	self.vx = 0
		# 	self.vy = 0

		self.lastTilePos = tilePos



		return self.pos
	def draw(self,screen,color,x,y,npcs):
		self.bounds = drawCar(screen,self.texture,x,y,-math.degrees(self.dir))
		#npcBounds = [x.bounds for x in npcs]
		#index = collision(self.bounds,npcBounds)
		

		for n in npcs:
			if (abs(n.pos[0]-self.pos[0]) < tileSize*2 and abs(n.pos[1]-self.pos[1]) < tileSize*2):
				
				col = collision(self.bounds,n.bounds,screen)
				
				if (col == True):

					#print("PLAYER POS: ",self.bounds.x,self.bounds.y)
					#print("NPC POS:    ",n.bounds.x,n.bounds.y)
					self.speed*=-1
					if (not n.done):
						
						
						if (n.police):
							print("hit a police!")
							n.sirens = False
						else:
							print("hit a npc!")
						n.done = True
						break
				
							
		#draw.circle(screen,(0,255,0),(self.bounds.x,self.bounds.y),3)
		#draw.circle(screen,(255,0,0),(self.bounds.x+self.bounds.width,self.bounds.y+self.bounds.height),3)
		#draw.rect(screen,(255,0,0),self.bounds,1)

	
		#draw.rect(screen,color,(int(self.pos[0]/tileSize-cameraPos[0])*tileSize,int(self.pos[1]/tileSize),tileSize,tileSize),3)
class segment(object):
	def __init__(self,pos1,pos2,numFrames):
		self.pos1 = pos1
		self.pos2 = pos2
		self.numFrames = numFrames

class npc(object):
	def __init__(self, startTile, endTile,roads,police):
		self.startTile = startTile
		self.endTile = endTile


		self.police = police
		self.sirens = False
		self.sirenTimer = 0
		self.pos = ((self.startTile[0]*tileSize)+tileSize/2,(self.startTile[1]*tileSize)+tileSize/2)
		self.vx, self.vy = 0,0
		self.path = [startTile]
		t = [startTile[0],startTile[1]]
		nextDirection = int(startTile[0] < endTile[0]),int(startTile[1] < endTile[1])  
		#print(startTile,endTile)
		#print(nextDirection)
		a = startTile
		self.posOnPath =0 
		self.movementDirection = nextDirection[0]*2-1,nextDirection[1]*2-1
		
		self.done = False
		self.color = randint(0,255),randint(0,255),randint(0,255)
		if (not self.police):
			self.texture = generateCar(Color(self.color[0],self.color[1],self.color[2]))
		else:
			self.texture = policeOff
		nextD = nextDirection[0]*2-1,nextDirection[1]*2-1
		while a != self.endTile:   #    Creates the path in terms of tiles for the npc
			direction = randint(0,1) #  createPath function uses actual positions of each point and generates segments and speeds of movement
			if (direction == 0):
				if (t[0] != self.endTile[0]):
					i = roads[0].index(t[0])
					i+=nextD[0]
					t[0] = roads[0][i]
			elif (direction == 1):
				if (t[1] != self.endTile[1]):
					i = roads[1].index(t[1])
					i+=nextD[1]
					t[1] = roads[1][i]
			
			a = (t[0],t[1])

			self.path.append(a)
		print("DONE GEN")






			#print(t,startTile,endTile)
			#print(startTile,endTile)
			#print(a)
			#time.sleep(0.3)

		#convert to positions path from tile path

		self.createPath()
		self.currentSegment = 0
		self.prevSegmentsTotal = 0


		self.quickChase = False
		self.turnSpeed = 0
		self.turning = False
		self.speed = 0
		self.dynpos = [0,0]
		self.dir = 0

		#print(self.path)
	def createPath(self):
		points = []
		for p in range(len(self.path)):
			b = self.path[p]
			a = b[0]*tileSize+tileSize/2, b[1]*tileSize+tileSize/2
			if (p > 0):
				last = self.path[p-1]#             1
				lastDir = int(last[0] == b[0])#  0 

				if (lastDir == 0):
					points.append(((a[0]-self.movementDirection[0]*tileSize/2,a[1]-laneOffset(self.movementDirection[0])),randint(30,50)))
				elif(lastDir == 1):
					points.append(((a[0]+laneOffset(self.movementDirection[1]),a[1]-self.movementDirection[1]*tileSize/2),randint(30,50)))
			if (p < len(self.path)-1):
				nxt = self.path[p+1]#             1
				nextDir = int(nxt[0] == b[0])#  0 

				if (nextDir == 0):
					points.append(((a[0]+self.movementDirection[0]*tileSize/2,a[1]-laneOffset(self.movementDirection[0])),randint(100,200)))
				elif(nextDir == 1):
					points.append(((a[0]+laneOffset(self.movementDirection[1]),a[1]+self.movementDirection[1]*tileSize/2),randint(100,200)))


			#points.append(a)


		segments = []
		for p in range(len(points)-1):
			segments.append(segment(points[p][0],points[p+1][0],points[p][1]))
		self.segments = segments
	def move(self):

		if (self.quickChase == False):
			if (not self.done):
				self.pos = self.posAt(self.posOnPath)
			#print(self.pos)

			self.posOnPath+=0.1

		



	def chase(self,target):
		if (not self.done):
			if (self.quickChase == False):
				self.dynpos = [self.pos[0],self.pos[1]]
			self.quickChase = True
			targetDelta = target[0]-self.dynpos[0],target[1]-self.dynpos[1]
			targetDirection = math.atan2(targetDelta[1],targetDelta[0])
			deltaDirection = targetDirection-self.dir
			print(targetDirection)
			self.turning = False
			if (deltaDirection < -0.1):
				self.dir+=self.turnSpeed*abs(self.speed)/3
				if (self.turnSpeed > -0.05):
					self.turnSpeed-=0.003
				self.turning = True
			elif(deltaDirection > 0.1):
				self.dir+=self.turnSpeed*abs(self.speed)/3
				if (self.turnSpeed < 0.05):
					self.turnSpeed+=0.003
				self.turning = True
			if (not self.turning):
				self.turnSpeed = 0

			self.speed+=0.02
			self.speed*=0.98

			self.dynpos[0]+=(math.cos(self.dir)*self.speed)
			self.dynpos[1]+=(math.sin(self.dir)*self.speed)
			self.pos = self.dynpos

			self.currentTile = tileAt(self.pos)

		


	def draw(self,screen,cameraPos):
		#draw.rect(screen,(255,0,255),(self.pos[0]-cameraPos[0]+width/2,self.pos[1]-cameraPos[1]+height/2,30,30))
		if (not self.quickChase):

			self.bounds = drawCar(screen,self.texture,self.pos[0]-cameraPos[0]+width/2,self.pos[1]-cameraPos[1]+height/2,-math.degrees(self.dir))
		else:
			self.bounds = drawCar(screen,self.texture,self.dynpos[0]-cameraPos[0]+width/2,self.dynpos[1]-cameraPos[1]+height/2,-math.degrees(self.dir))
		#draw.rect(screen,(255,0,0),self.bounds,1)
		if (self.quickChase):
			self.sirens = True

			self.sirenTimer+=1


		if (self.sirenTimer > 30):
			self.sirenTimer = 0
		if (self.police):
			if (self.sirens):
				if (self.sirenTimer < 15):
					self.texture = policeRed
				else:
					self.texture = policeBlue
			else:
				self.texture = policeOff
	def posAt(self,t):
		#print(self.startTile,self.endTile)
		f = t
		i = 0
		if (self.currentSegment == len(self.segments)-1):
			self.done = True
		if (self.posOnPath-self.prevSegmentsTotal > self.segments[self.currentSegment].numFrames):
			self.prevSegmentsTotal+=self.segments[self.currentSegment].numFrames
			self.currentSegment+=1
		
		sel = self.segments[self.currentSegment]
		f = self.posOnPath-self.prevSegmentsTotal
		percentFinished = f/sel.numFrames
		#print(sel.pos1,sel.pos2)
		pos = sel.pos1[0]+(sel.pos2[0]-sel.pos1[0])*percentFinished,sel.pos1[1]+(sel.pos2[1]-sel.pos1[1])*percentFinished
		self.dir = math.atan2(sel.pos2[1]-self.pos[1],sel.pos2[0]-self.pos[0])
		return pos

	def drawPath(self,screen,cameraPos):
		for s in self.segments:
			a = s.pos1[0]-cameraPos[0]+width/2,s.pos1[1]-cameraPos[1]+height/2
			b = s.pos2[0]-cameraPos[0]+width/2,s.pos2[1]-cameraPos[1]+height/2
			draw.line(screen,self.color,a,b,3)

	
