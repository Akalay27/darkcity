'''

Copyright © 2019 Adam Kalayjian

Darkcity

'''
import sys
try:
	import pygame
except:
	print("pygame is not installed. run pip install pygame")
import math
from random import randint, random
from pygame import draw
import time
from pygame import gfxdraw
import drawtile
from drawtile import drawBuilding, drawRoad 
import constants
from constants import *
from car import car, npc
pygame.init()


roadColors = {"side":(30,30,30),"lane":(100,100,100)}


#SHADING OF BUILDINGS - randomly modified later
shading = {"top":(30,30,30),"north":(40,40,40),"east":(35,35,35),"south":(25,25,25),"west":(15,15,15)}

#shading = {"top":(67,67,67),"north":(78,78,78),"east":(90,90,90),"south":(25,25,25),"west":(15,15,15)}
#shading = {"top":(255,255,255),"north":(255,0,0),"east":(0,0,255),"south":(0,255,0),"west":(255,0,255)}


pygame.display.set_caption("DARKCITY DRIFT")
traffic = [[],[]]


screen = pygame.display.set_mode(size)
carLayer = pygame.Surface.copy(screen)

pan = False #controlled camera movement or user input

windowShape = (4,3)
streets = []


def dispText(screen,pos,text):
	font = pygame.font.Font('freesansbold.ttf',10)

	textSurface = font.render(text,True,(255,0,0))
	screen.blit(textSurface,pos)
def mrange(min,max,middle): # goes from sides into center, needed for correct rendering
    direction = -1
    nums = []
    m = max-1
    i = 0

    while m >= middle:        
        nums.append(m)
        m-=1
    i = min
    while i < middle:        
        nums.append(0+i)
        i+=1
    return nums


class building(object):  
	def __init__(self):
		self.length = randint(tileSize/3,tileSize)
		self.width = randint(tileSize/3,tileSize)
		self.height = randint(10,150)
		self.xOffset = random()*(tileSize-self.length)
		self.yOffset = random()*(tileSize-self.width)
		self.decal = random()
		self.textures = {"north":pygame.Surface((int(self.length),int(self.height))),"east":pygame.Surface((int(self.width),int(self.height))),"south":pygame.Surface((int(self.length),int(self.height))),"west":pygame.Surface((int(self.width),int(self.height))),"top":pygame.Surface((int(self.length),int(self.width)))}
		self.shading = {}
		self.brightness = random()+1 # 1 to 1.2
		self.windowSpacing = (randint(windowShape[0]+1,windowShape[0]*2),randint(windowShape[1]+1,windowShape[1]*2))
		for b in self.textures: #each building is given 5 images to use as textures, "base coat" of shading is put on first

			t = self.textures[b]
			baseColor = []
			for c in shading[b]:
				baseColor.append(c*self.brightness)
			self.shading[b] = baseColor
			t.fill(baseColor)
			#t.blit(pygame.transform.smoothscale(supreme,t.get_size()),(0,0))
			width, height = t.get_size()

		self.generateTextures()
	def generateTextures(self): #right now is only windows, eventually logos, storefronts, advertisements, etc.
		sides = ["north","east","south","west"]

		texType = randint(0,100)
		if (texType > 0):
			for b in self.textures:
				t = self.textures[b]
				if (b in sides):
					if (random() < 0.05): continue
					width, height = t.get_size()
					for y in range(self.windowSpacing[1]*2,height-self.windowSpacing[1]*2,self.windowSpacing[1]):
						for x in range(self.windowSpacing[0],width-self.windowSpacing[0],self.windowSpacing[0]):
							
							rand = randint(int(self.shading[b][0]),210)
							draw.rect(t,(rand,rand,rand),(x,y,windowShape[0],windowShape[1]))



class tile(object):
	def __init__(self,pos,t):
		self.pos = pos
		self.t = t

		if (isinstance(self.t,building)):
			self.ty = "building"
		else:
			self.ty = "road"
		#print(self.ty)
		#print(pos)
		

class road(object):		
		def __init__(self, direction):
			self.lanes = 3
			self.direction = direction
			
tileDimX, tileDimY = (int(width/tileSize),int(height/tileSize))
carSize = (2,5)		
lanes = 4
roadMatrix = (5,5)
numCarsPerTile = 3

def genRoads(roads):
	size = 10000
	pos = -size
	skip = 5
	while pos < size:
		roads[0].append(pos)
		pos+=skip
		skip = randint(5,10)
		
	pos = -size
	while pos < size:
		roads[1].append(pos)
		pos+=skip
		skip = randint(5,10)
		#print(pos)
	
		

def newTiles(city,cameraPos,dx, dy):
	for y in range(cameraPos[1]-dy,cameraPos[1]+dy):
		for x in range(cameraPos[0]-dx,cameraPos[0]+dx):
			t = city.get((x,y),None)
			if (t == None):
				if (x in roads[0] and y in roads[1]):
					city[(x,y)] = tile((x,y),road(2))
				elif(x in roads[0]):
					city[(x,y)] = tile((x,y),road(0))
				elif(y in roads[1]):
					city[(x,y)] = tile((x,y),road(1))
				else:
					city[(x,y)] = tile((x,y),building())
				#print("ADDED ", (x,y))

def getIntersectionNear(roads,pos,r=10):
	dist = 10000000000000
	ix = None
	for x in range(pos[0]-r,pos[0]+r):
		if (x in roads[0]):
			ix = x
	for y in range(pos[1]-r,pos[1]+r):
		if (y in roads[1]):
			iy = y
	return ix, iy
		
def getRoadNear(roads,pos,direction):
	if direction == 0:
		for y in range(pos[1],pos[1]+100):
			if y in roads[1]:
				return pos[0],y


genRoads(roads)



# while player.pos[0] not in roads[1]:
# 	player.pos[0]+=tileSize


startPos = getIntersectionNear(roads,(0,0),7)

endPos = getIntersectionNear(roads,(100,100))



playerStart = getRoadNear(roads,(0,0),0)
print(playerStart,endPos)
player = car([playerStart[0]*tileSize,playerStart[1]*tileSize])

player.pos[0]+=tileSize/2
player.pos[1]+=tileSize/2
print(player.pos)



newTiles(city,startPos,tileDimX,tileDimY)
print(playerStart,endPos)
npcs = []

total = 1500
for n in range(total):

	start, end = None,None
	while start == end:
		start = getIntersectionNear(roads,(randint(-100,100),randint(-100,100)))
		end = getIntersectionNear(roads,(randint(-100,100),randint(-100,100)))

	npcs.append(npc(start,end,roads,random() < -1))

	draw.arc(screen,(255,255,255),((width/2-50,height/2-50),(100,100)),0,((n/total)*math.pi*2),4)
	pygame.display.flip()


frames = 0
while 1:
	floatingPos[0] = player.pos[0]
	floatingPos[1] = player.pos[1]
	cameraPos = (round(floatingPos[0]),round(floatingPos[1])) #floatingPos is required since cameraPos must be int but I need slower movement.
	screen.fill(black)
	#print("PLAYER AT ",tileAt(cameraPos), "NPC AT ", tileAt(test.pos))
	frames+=1

	newTiles(city,(int(cameraPos[0]/tileSize),int(cameraPos[1]/tileSize)),tileDimX*2,tileDimY*2)
	
	#addRoads(city)
	#drawTraffic(city,screen)
	# if (pan == False): 
	# 	floatingPos[0]-=0.3
	# 	floatingPos[1]-=0.6 
	
	
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: sys.exit()
		# if event.type == pygame.KEYDOWN:
		# 	if event.key == pygame.K_LEFT:
		# 		perspectiveAmount -= 20
		# 	if event.key == pygame.K_RIGHT:
		# 		perspectiveAmount += 20
			
	keys = pygame.key.get_pressed()  #checking pressed keys for user-input camera movement
	# if keys[pygame.K_UP]:
	# 	floatingPos[1]-=20
	# if keys[pygame.K_DOWN]:
	# 	floatingPos[1]+=20
	# if keys[pygame.K_LEFT]:
	# 	floatingPos[0]-=20
	# if keys[pygame.K_RIGHT]:
	# 	floatingPos[0]+=20

	cmPosTile = (int(cameraPos[0]/tileSize),int(cameraPos[1]/tileSize))
	for y in mrange(cmPosTile[1]-tileDimY,cmPosTile[1]+tileDimY,cmPosTile[1]):
		for x in mrange(cmPosTile[0]-tileDimX,cmPosTile[0]+tileDimX,cmPosTile[0]):
			t = city.get((x,y),None)
			if t != None:
				xp,yp = int(x*tileSize-cameraPos[0]+width/2),int(y*tileSize-cameraPos[1]+height/2)
				if (isinstance(t.t,building)):
					drawBuilding(screen,t.t,xp,yp,perspectiveAmount,shading)
				if (isinstance(t.t,road)):
					drawRoad(screen,t.t,xp,yp)
				#if (frames % 4 == 0): dispText(screen,(xp,yp),str(t.pos) + "," + str(t.pos))
	
	#draw.circle(screen,(255,0,0),posAt((0,0),cameraPos),30)
	
	#test.drawPath(screen,cameraPos)
	for n in npcs:
		if (abs(n.pos[0]-player.pos[0]) < tileSize*tileDimX*2 and abs(n.pos[1]-player.pos[1]) < tileSize*tileDimY*2):
			n.draw(screen,cameraPos)
			n.move()
		if (abs(n.pos[0]-player.pos[0]) < tileSize*3 and abs(n.pos[1]-player.pos[1]) < tileSize*3 and n.police == True):
			n.chase(player.pos)
		elif (n.quickChase):
			n.chase(player.pos)
	player.playerControl(roads)
	player.draw(screen,(255,0,0),width/2,height/2,npcs)
		#if n.done:
		#	n = npc(getIntersectionNear(roads,(randint(-100,100),randint(-100,100))),getIntersectionNear(roads,(randint(-100,100),randint(-100,100))),roads)
		#n.drawPath(screen,cameraPos)
	#mi = test.startTile
	#ma = max(test.path)
	# for p in test.path:

	# 	draw.circle(screen,(255,0,0),(p[0]-test.startTile[0]+300,p[1]-test.startTile[1]+300),1)
	pygame.display.flip()

#ROAD DIRECTIONS: 0
#                 X 1
#                 



