import pygame
import numpy
from pygame import surfarray
# texture = pygame.image.load("test.jpg")
# pygame.init()

# size = w, h = 320, 240
# speed = [2, 2]
# black = 0, 0, 0

# screen = pygame.display.set_mode(size)
# teximg = pygame.image.load("test.jpg")
# texture = surfarray.array3d(teximg)

# print(texture)
resolution = (1,1)


def bounds(value,mi,ma): #crashes when indexing array val outside screen, so I need this
	if (value >= ma):
		return ma-1
	if (value < mi):
		return mi
	return value
def textureMap(screen,image,pts): #able to draw parallelograms, which is all I need!
	points = []       #                            - very quickly
	for c in pts:
		points.append((round(c[0]),round(c[1])))
	start = points[0]
	sideX = points[1]
	sideY = points[3]
	width, height = (sideX[0]-start[0],sideY[1]-start[1])
	scr = surfarray.pixels3d(screen)
	im = surfarray.pixels3d(pygame.transform.smoothscale(image,(width,height)))
	w, h = scr.shape[:2]
	direction = -1
	imageW, imageH = im.shape[:2]
	

	if width == 0 or height == 0: return
	if (start[0]-sideY[0] == 0):
		direction = 1
	if (start[1]-sideX[1] == 0):
		direction = 0
	#print(width,height,imageW,imageH)
	if (direction == 0):
		dY = ((sideY[0]-start[0])/height) #shift in ENTIRE X ROW for every y value, gives it the slant.
		mX = int(imageW/width) #ratio btwn width of original picture and new width
		mY = int(imageH/height)
		#print(width)
		for y in range(height):
			
			boundL = int(abs(start[0]+dY*y-bounds(start[0]+dY*y,0,w)))
			boundR = int(abs(start[0]+dY*y+width-bounds(start[0]+dY*y+width,0,w)))
			#print("Bounds:",boundL,boundR)
			if (boundL > 0):
				boundL+=1
			#print(bounds(int(start[0]+dY*y),0,w),int(start[0]+dY*y))
			try:
				scr[bounds(int(start[0]+dY*y),0,w):bounds(int(start[0]+dY*y+width),0,w),bounds(start[1]+y,0,h)] = im[boundL:width-boundR,y] #im[0:int(width*mX):mX,y*mY]
			except:
				continue

	elif (direction == 1):
		dX = (sideX[1]-start[1])/width #shift in ENTIRE Y ROW for every x value, gives it the slant.
		mX = int(imageW/width) #ratio btwn width of original picture and new width
		mY = int(imageH/height) 

		

		for x in range(width):
			boundT = int(abs(start[1]+dX*x-bounds(start[1]+dX*x,0,h)))
			boundB = int(abs(start[1]+dX*x+height-bounds(start[1]+dX*x+height,0,h)))
			#print(boundT,boundB)
			if (boundT > 0):
				boundT+=1
			try: #numpy array slicing is so much faster 
				scr[bounds(int(start[0]+x),0,w),bounds(int(start[1]+dX*x),0,h):bounds(int(start[1]+dX*x+height),0,h)] = im[x,boundT:height-boundB]
			except:
				continue 


