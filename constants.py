'''

Copyright © 2019 Adam Kalayjian

Darkcity

'''
size = width, height = 500, 500
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

#WORLDGEN OPTIONS
city = {}
cityWidth = 10
cityLength = 10
tileSize = 75
#CAMERA OPTIONS
floatingPos = [0,0]
cameraPos = [0,0]
perspectiveAmount = 550

#ROAD OPTIONS
distanceFromSide = 5
laneSize = 10
maxLanes = (tileSize-(distanceFromSide*2))//laneSize

roadColors = {"side":(100,100,100),"lane":(30,30,30)}

physicsSpeed = 1

#have to do this because cross refrencing city and drawtile is really bad and doesn't work.
#so variables that are referenced and changed in both are stored in this file

roads = [[],[]]	








def tileAt(p):
	x, y = p
	pos = [int(x/tileSize),int(y/tileSize)]
	if x < 0:
		pos[0]-=1
	if y < 0:
		pos[1]-=1
	a = (pos[0],pos[1])
	return a

def posAt(t,cameraPos):
	tx,ty = t

	return [int((tx*tileSize)-cameraPos[0]+width/2), int((ty*tileSize)-cameraPos[1]+height/2)]
