import neat
import pygame
import random
import sys
import math
import os

#beautiful, init mate?
pygame.init()
width,height = 1080,720
screen  = pygame.display.set_mode((width,height))
font = pygame.font.SysFont(None,32)

#images
menu_bg = pygame.image.load("./assets/pictures/menubg.png").convert()
game_backround = pygame.image.load("./assets/pictures/background.png").convert()
pipeup = pygame.image.load("./assets/pictures/pipeup.png")
pipedown = pygame.image.load("./assets/pictures/pipedown.png")
ground = pygame.image.load("./assets/pictures/ground.png")
bird = pygame.image.load("./assets/pictures/bird.png")


#ingame clock
clock = pygame.time.Clock()
fps = 80

#scores; score1 caps at 14
global score
global score1
score = 0
score1 = 0

#the speed the pipes travel to the left
pipespeed = 6
def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(game,50)

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
		self.y = random.randint(150,height-150)
		self.x = width+50
		self.passed = False
		self.hitbox = [pygame.Rect(self.x-75, 0,          150, self.y-100),pygame.Rect(self.x-75, self.y+100, 150, height)] 
		self.top = self.y - 100
		self.bot = self.y + 100 
	#moves the pipe to the left when called
	def update(self):
		self.x -= pipespeed
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
		self.corners = [(self.xpos-self.scale,self.ypos-self.scale+5),(self.xpos-self.scale,self.ypos+self.scale-5),(self.xpos+self.scale,self.ypos+self.scale-5),(self.xpos+self.scale,self.ypos-self.scale+5)]

	#gravity for the bird
	def update(self):
		self.timer += 1/fps
		if self.ascendspeed > 0:
			self.ascendspeed -= self.yspeed*self.timer**2.6
			if self.ascendspeed < 0:
				self.ascendspeed = 0
		self.ypos += self.yspeed*self.timer**2 - self.ascendspeed
		self.yvel = self.yspeed*self.timer**2 - self.ascendspeed
		self.corners = [(self.xpos-self.scale,self.ypos-self.scale+5),(self.xpos-self.scale,self.ypos+self.scale-5),(self.xpos+self.scale,self.ypos+self.scale-5),(self.xpos+self.scale,self.ypos-self.scale+5)]
		screen.blit(bird,(self.corners[0][0]-2,self.corners[0][1]-2))
	#lets the bird flap higher
	def tapped(self):
		self.ascendspeed = 7
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

#the main game
def game(genomes, config):

	#variables
	nets = []
	ge = []
	birds = []

	for _,g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g,config)
		nets.append(net)
		birds.append(Bird(height/2))
		g.fitness = 0
		ge.append(g)

	pipes = []
	alive = True
	death = False
	kill = False
	global score1
	global score
	score1 = 0
	score = 0
	timer1 = 0

	while alive:
		clock.tick(fps)
		#projects game background and spikes to screen
		screen.blit(game_backround,(0,0))
		Ground()

		#checks for click or exit command
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


		#this is now useless
		if True:			
			
			#score1 = game difficulty system
			score1 = score
			if score1 > 14:
				score1 = 14

			
			#creates new Pipe object every x game frames
			if timer1%120 == 0:
				pipes.append(Pipe())
			
			
			#updates the bird and checks if a the bird passed a pipe
			for bird in birds:
				bird.update()

			for pipe in pipes:
				for bird in birds:
					add_score = False
					if bird.xpos > pipe.x+75 and pipe.passed == False:
			

						#adds 1 to the score if the pipe has been passed successfully
						pipe.passed = True
						add_score = True
						
						for g in ge:
							g.fitness += 5

						print(f"score increased :  {score}")
					if add_score:
						score += 1
			
			
				#updates / deletes pipe if necessary
				pipe.update()
				
			
				if pipe.x < -200:
					pipes = pipes[1:]
				for bird in birds:
					if pipe.x+95 > bird.xpos:
						nextpipe = pipe
						break
			if len(birds) < 1:
				alive = False
				break

			for n,bird in enumerate(birds):
				bird.update()
				ge[n].fitness += 0.04

				output = nets[n].activate((bird.ypos, abs(bird.ypos-nextpipe.top), abs(bird.ypos - nextpipe.bot)))

				if output[0] > 0.5:
					bird.tapped()




			#hit registration for ground and pipes
			for n,bird in enumerate(birds):
				for point in bird.corners:
					for box in nextpipe.hitbox:
						try:
							if checkcol(box,point[0],point[1]):
								ge[n].fitness -= 1
								birds.pop(n)
								nets.pop(n)
								ge.pop(n)							
						except:
							pass
					for pos in Ground().hitbox:
						try:
							if checkcol(pos,point[0],point[1]):
								ge[n].fitness -= 1
								birds.pop(n)
								nets.pop(n)
								ge.pop(n)
						except:
							pass

			#checks if the bird is lower or higher than the screen. Replaced by the Ground object but to avoid bugs this will remain 
			for n,bird in enumerate(birds):
				if bird.ypos+bird.yspeed*bird.timer**2.5 > height:
					bird.ypos = height-25
					birds.pop(n)
					nets.pop(n)
					ge.pop(n)
				
			
				elif bird.ypos < 0:
					bird.ypos = -5
					birds.pop(n)
					nets.pop(n)
					ge.pop(n)
			
		#updates the game frame
		pygame.display.update()
		timer1 += 1

#opens the main menu on start
if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)
