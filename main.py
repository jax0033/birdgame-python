import pygame
import random
import math

#beautiful, init mate?
pygame.init()
screen  = pygame.display.set_mode((802,802))
width,height = 802,802
font = pygame.font.Font("freesansbold.ttf",32)
clock = pygame.time.Clock()
fps = 60


class Pipe:
	def __init__(self):
		self.ypos = random.randint(40,height-40)


class Bird:
	def __init__(self,ypos):
		self.ypos = ypos
		self.ascendspeed = 0
		self.yspeed = 30
		self.xpos = width/2.75
		self.timer = 0	
	def update(self):
		
		self.timer += 1/60

		if self.ascendspeed > 0:
			self.ascendspeed -= self.yspeed*self.timer**2.5
			if self.ascendspeed < 0:
				self.ascendspeed = 0
		
		self.ypos += self.yspeed*self.timer**2 - self.ascendspeed

	def tapped(self):
		self.ascendspeed = 9
		self.yspeed = 30
		self.timer = 0

def block(coords, color=(255,0,0)):
	x,y = coords[0],coords[1]
	x2,y2 = x+30,y+30
	pygame.draw.polygon(screen,color, ((x,y),(x2,y),(x2,y2),(x,y2)),0)


b1 = Bird(height/2)
start = True
run = True

while run:
	clock.tick(fps)
	screen.fill((240,240,240))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			b1.tapped()


	if start == True:
		if b1.ypos > height:
			run = False
		block((b1.xpos,b1.ypos))
		b1.update()


	pygame.display.update()
print("Game Quit")
pygame.quit()
