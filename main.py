import pygame
import random
import sys
import math

#beautiful, init mate?
pygame.init()
width,height = 1080,720
screen  = pygame.display.set_mode((width,height))
font = pygame.font.SysFont(None,32)

#images
menu_bg = pygame.image.load("menubg.png").convert()
game_backround = pygame.image.load("background.png").convert()
pipeup = pygame.image.load("pipeup.png")
pipedown = pygame.image.load("pipedown.png")
ground = pygame.image.load("ground.png")

#ingame clock
clock = pygame.time.Clock()
fps = 60

#score
global score
score = 0

#the speed the pipes travel to the left
pipespeed = 6


#top and bottom spikes
class Ground:

	def __init__(self):
		self.top = 27
		self.bot = height-27
		self.hitbox = [pygame.Rect(0,0,width,self.top),pygame.Rect(0,self.bot,width,self.top)]
		screen.blit(ground,(0,0))


#pipe
class Pipe:
	
	def __init__(self):
		self.y = random.randint(100,height-100)
		self.x = width+50
		self.passed = False
		self.hitbox = [pygame.Rect(self.x-75, 0,          150, self.y-100),pygame.Rect(self.x-75, self.y+100, 150, height)] 
	
	#moves the pipe to the left when called
	def update(self):
		self.x -= pipespeed*(score/10+1) 
		screen.blit(pipeup,(self.x-75,self.y+100))
		screen.blit(pipedown,(self.x-75,self.y-820))
		self.hitbox = [pygame.Rect(self.x-75, 0,          150, self.y-100),pygame.Rect(self.x-75, self.y+100, 150, height)] 

#fl4ppy b1rd
class Bird:

	def __init__(self,ypos):
		self.ypos = ypos
		self.ascendspeed = 0
		self.yspeed = 30
		self.xpos = width/2.75
		self.timer = 0
		self.scale = 20
		self.corners = [(self.xpos-self.scale,self.ypos-self.scale),(self.xpos-self.scale,self.ypos+self.scale),(self.xpos+self.scale,self.ypos+self.scale),(self.xpos+self.scale,self.ypos-self.scale)]

	#gravity for the bird
	def update(self):
		self.timer += 1/60
		if self.ascendspeed > 0:
			self.ascendspeed -= self.yspeed*self.timer**2.6
			if self.ascendspeed < 0:
				self.ascendspeed = 0
		self.ypos += self.yspeed*self.timer**2 - self.ascendspeed
		self.yvel = self.yspeed*self.timer**2 - self.ascendspeed
		self.corners = [(self.xpos-self.scale,self.ypos-self.scale),(self.xpos-self.scale,self.ypos+self.scale),(self.xpos+self.scale,self.ypos+self.scale),(self.xpos+self.scale,self.ypos-self.scale)]

	#lets the bird flap higher
	def tapped(self):
		self.ascendspeed = 9
		self.yspeed = 30
		self.timer = 0

#checks collision between rectangle and a point
def checkcol(rect,x,y):
	if rect.collidepoint((x,y)):
		return True
	else:
		return False

#draws text onto the screen
def draw_text(text,font,color,surface,x,y):
	textobj = font.render(text,1,color)
	textrect = textobj.get_rect(center=(x,y))
	surface.blit(textobj, textrect)

#the main menu when you start the game
def main_menu():

	#variables
	click = False
	main_menu = True
	
	while main_menu:

		#main menu screen and buttons
		screen.blit(menu_bg,(0,0))
		button_1 = pygame.Rect(0,100,width,50)
		button_2 = pygame.Rect(0,200,width,50)
		pygame.draw.rect(screen,(66,66,66),button_1)
		pygame.draw.rect(screen,(66,66,66),button_2)

		mx,my = pygame.mouse.get_pos()

		#draws text on top of the buttons and checks if you click button1 or button2		
		if button_1.collidepoint((mx,my)):
			pygame.draw.rect(screen,(34,34,34),button_1)
			pygame.draw.rect(screen,(66,66,66),button_2)

			draw_text("Start",font,(60,4,117), screen, width/2, 125)
			draw_text("Exit",font,(255,255,255), screen, width/2, 225)
			if click:
				game()
		elif button_2.collidepoint((mx,my)):
			pygame.draw.rect(screen,(66,66,66),button_1)
			pygame.draw.rect(screen,(34,34,34),button_2)

			draw_text("Start",font,(255,255,255), screen, width/2, 125)
			draw_text("Exit",font,(60,4,117), screen, width/2, 225)
			if click:
				pygame.quit()
				sys.exit()
		else:
			pygame.draw.rect(screen,(66,66,66),button_1)
			pygame.draw.rect(screen,(66,66,66),button_2)

			draw_text("Start",font,(255,255,255), screen, width/2, 125)
			draw_text("Exit",font,(255,255,255), screen, width/2, 225)

		click = False
		
		#checks for click or exit command from the player		
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

		#bakes everything together and updates the screen
		pygame.display.update()
		clock.tick(fps)

#the main game
def game():

	#variables
	global score
	timer1 = 0
	pipes = []
	b1 = Bird(height/2)
	alive = True
	death = False
	score = 0
	kill = False
	
	while alive:

		#projects game background and spikes to screen
		screen.blit(game_backround,(0,0))
		Ground()

		#checks for click or exit command
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				b1.tapped()

		#checks if the player is not dead
		if alive == True:
			#score1 = game difficulty system
			score1 = score
			if score1 > 14:
				score1 = 14

			#creates new Pipe object every x game frames
			if timer1%round((120/score1+1)) == 0:
				pipes.append(Pipe())
			
			#updates the bird and checks if a the bird passed a pipe
			b1.update()
			for pipe in pipes:
				if b1.xpos > pipe.x+75 and pipe.passed == False:
					#adds 1 to the score if the pipe has been passed successfully
					score += 1
					pipe.passed = True
					print(f"score increased :  {score}")
			
				#updates / deletes pipe if necessary
				pipe.update()
				
				if pipe.x < -200:
					pipes = pipes[1:]
			
				if pipe.x+95 > b1.xpos:
					nextpipe = pipe
					break

			#visualized hitbox for the player
 			pygame.draw.polygon(screen,(255,255,25),b1.corners)
			if kill == True:
				main_menu()

			#hit registration
			for point in b1.corners:
				for box in nextpipe.hitbox:
					if checkcol(box,point[0],point[1]):
						kill = True
				for pos in Ground().hitbox:
					if checkcol(pos,point[0],point[1]):
						kill = True

			#checks if the bird is lower or higher than the screen. Replaced by the Ground object but to avoid bugs this will remain 
			if b1.ypos+b1.yspeed*b1.timer**2.5 > height:
				b1.ypos = height-25
				alive = False
				death = True
			
			elif b1.ypos < 0:
				b1.ypos = -5
				alive = False
				death = True

			#visualized hitbox corners for the player
			for point in b1.corners:
				pygame.draw.circle(screen, (0,0,255), (round(point[0]), round(point[1])), 1)

		#updates the game frame
		pygame.display.update()
		clock.tick(fps)
		timer1 += 1
#opens the main menu on start
main_menu()
