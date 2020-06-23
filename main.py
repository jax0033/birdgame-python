import pygame
import random
import sys
import math

#beautiful, init mate?
pygame.init()
width,height = 1080,720
screen  = pygame.display.set_mode((width,height))
font = pygame.font.SysFont(None,32)
menu_bg = pygame.image.load("menubg.png").convert()

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

def draw_text(text,font,color,surface,x,y):
	textobj = font.render(text,1,color)
	textrect = textobj.get_rect(center=(x,y))
	surface.blit(textobj, textrect)

def main_menu():
	click = False
	main_menu = True
	while main_menu:
		screen.blit(menu_bg,(0,0))
		button_1 = pygame.Rect(0,100,width,50)
		button_2 = pygame.Rect(0,200,width,50)
		pygame.draw.rect(screen,(66,66,66),button_1)
		pygame.draw.rect(screen,(66,66,66),button_2)
		
		draw_text("Start",font,(255,255,255), screen, width/2, 125)
		draw_text("Exit",font,(255,255,255), screen, width/2, 225)
		mx,my = pygame.mouse.get_pos()
		
		if button_1.collidepoint((mx,my)):
			if click:
				game()
		if button_2.collidepoint((mx,my)):
			if click:
				pygame.quit()
				sys.exit()
		
		click = False
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		pygame.display.update()
		clock.tick(fps)

def game():
	b1 = Bird(height/2)
	alive = True
	death = False
	while alive:

		screen.fill((240,240,240))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				b1.tapped()

		if alive == True:
			block((b1.xpos,b1.ypos))
			b1.update()

			if b1.ypos+b1.yspeed*b1.timer**2.5 > height:
				b1.ypos = height-25
				alive = False
				death = True
			elif b1.ypos < 0:
				b1.ypos = -5
				alive = False
				death = True

		elif death == True:
			block((b1.xpos,b1.ypos))

		pygame.display.update()
		clock.tick(fps)

main_menu()
print("Game Quit")
pygame.quit()
