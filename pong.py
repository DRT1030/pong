import pygame
import random

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parry")

clock = pygame.time.Clock() 
FPS = random.randint(30,120)

# Striker class


class Striker:
		# Take the initial position, dimensions, speed and color of the object
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		# Rect that is used to control the position and collision of the object
		self.doeRect = pygame.Rect(posx, posy, width, height)
		# Object that is blit on the screen
		self.doe = pygame.draw.rect(screen, self.color, self.doeRect)

	# Used to display the object on the screen
	def display(self):
		self.doe = pygame.draw.rect(screen, self.color, self.doeRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Restricting the striker to be below the top surface of the screen
		if self.posy <= 0:
			self.posy = 0
		# Restricting the striker to be above the bottom surface of the screen
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# Updating the rect with the new values
		self.doeRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.doeRect

# Ball class


class Ball:
	global FPS
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		# If the ball hits the top or bottom surfaces, 
		# then the sign of yFac is changed and 
		# it results in a reflection
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		global FPS
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1
		temp = random.randint(1,4)
		FPS = 120 / temp

	# Used to reflect the ball along the X-axis
	def hit(self):
		global FPS
		self.xFac *= -1
		FPS += 5

	def getRect(self):
		return self.ball

# Game Manager


def main():
	running = True

	# Defining the objects
	doe1 = Striker(0, 0, 10, 100, 10, GREEN)
	doe2 = Striker(WIDTH-10, 0, 10, 100, 10, GREEN)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

	listOfdoes = [doe1, doe2]

	# Initial parameters of the players
	doe1Score, doe2Score = 0, 0
	doe1YFac, doe2YFac = 0, 0

	while running:
		screen.fill(BLACK)

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					doe2YFac = -1
				if event.key == pygame.K_DOWN:
					doe2YFac = 1
				if event.key == pygame.K_w:
					doe1YFac = -1
				if event.key == pygame.K_s:
					doe1YFac = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					doe2YFac = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					doe1YFac = 0

		# Collision detection
		for doe in listOfdoes:
			if pygame.Rect.colliderect(ball.getRect(), doe.getRect()):
				ball.hit()

		# Updating the objects
		doe1.update(doe1YFac)
		doe2.update(doe2YFac)
		point = ball.update()

		# -1 -> doe_1 has scored
		# +1 -> doe_2 has scored
		# 0 -> None of them scored
		if point == -1:
			doe1Score += 1
		elif point == 1:
			doe2Score += 1
		if doe1Score == 10 or doe2Score == 10:
			pygame.quit()

		# Someone has scored
		# a point and the ball is out of bounds.
		# So, we reset it's position
		if point: 
			ball.reset()

		# Displaying the objects on the screen
		doe1.display()
		doe2.display()
		ball.display()
      
		# Displaying the scores of the players
		doe1.displayScore("doe_1 : ",  doe1Score, 100, 20, WHITE)
		doe1.displayScore("Pong", 0 ,WIDTH//2, 20, WHITE)
		doe2.displayScore("doe_2 : ", doe2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)
		print(str(FPS))


if __name__ == "__main__":
	main()
	pygame.quit()
