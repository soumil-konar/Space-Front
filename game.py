import pygame
import random
import math
from pygame import mixer


pygame.init()

screen=pygame.display.set_mode((800,600))

#GameOver

over_font=pygame.font.Font('game_over.ttf', 70)

#background

background=pygame.image.load("index.jpeg").convert_alpha()
background = pygame.transform.scale(background, (800,600))	

#Title and Logo

pygame.display.set_caption("Space Front")
icon = pygame.image.load("battleship.png")
pygame.display.set_icon(icon)

#Music
mixer.music.load('background.wav')
mixer.music.play(-1)


#player


playerimage = pygame.image.load("space-invaders.png")
# for scaling photos
#.convert_alpha()
# playerimage = pygame.transform.scale(playerimage, (50,30))
playerX = 365
playerY = 480
playerX_change=0


#enemy


#using list for multiple enemies
enemyimage =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range (num_of_enemies):

	enemyimage.append(pygame.image.load("ship.png"))

	# for scaling photos
	#.convert_alpha()
	# playerimage = pygame.transform.scale(playerimage, (50,30))

	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,200))
	enemyX_change.append(0.3)
	enemyY_change.append(40)

#bullet

#ready - bullet not seen
#fire - bullet can be seen

bulletimage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.1
bullet_state = "ready"

#Score

score_value=0
font = pygame.font.Font('game_over.ttf',60)
scoreX = 10
scoreY = 10

#Functions

def game_over_text():
	over_font=font.render("GAME OVER",True, (0,0,0))
	screen.blit(over_font, (325,250))

def show_score(x,y):
	score = font.render("Score : " + str(score_value), True, (0,0,0))
	screen.blit(score,(x,y))
	
	
def player(x,y):
	screen.blit(playerimage,(x,y))
	
	
def enemy(x,y,i):
	screen.blit(enemyimage[i] ,(x,y))
	

def fire_bullet(x,y):
	global bullet_state	
	bullet_state = "fire"
	screen.blit(bulletimage,(x+16,y+10))
	
	
def if_collided(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
	if distance < 27:
		return True
	else:
		return False
		



#Game Loop


running = True
while running:
	
	#RGB		
	screen.fill((251, 250, 245))
	#screen.fill((0,0,0))
	
	#background image
	screen.blit(background,(0,0))
	
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
			
	# if keystroke is pressd check whether it is right or left
		
		
		if event.type == pygame.KEYDOWN:
			print("A keystroke is pressed")
			if event.key == pygame.K_LEFT:
				playerX_change = -0.35
				print("Left arrow is pressed")
			if event.key == pygame.K_RIGHT:
				playerX_change = 0.35
				print("Right arrow is pressed")
			if event.key == pygame.K_SPACE:
				bullet_sound = mixer.Sound('bullet.wav')
				bullet_sound.play()
				bulletX=playerX
				fire_bullet(bulletX,bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
				print("Keystroke has been released")
	
	
#player movement
	
	playerX += playerX_change 	#playercall
	
	if playerX <= 0:		#making boundary to stop player from exiting screen
		playerX = 0
	elif playerX >=736:
		playerX = 736
		
		

#enemy movement

	for i in range (num_of_enemies):
		
		#Gameover
		if enemyY[i] > 435:
			for j in range (num_of_enemies):
				enemyY[j] = 2000
			game_over_text()	 	
			break
		
			
		enemyX[i] += enemyX_change[i]	
		if enemyX[i] <= 0:		#making boundary to stop enemy from exiting screen
			enemyX_change[i] = 0.4
			enemyY[i]+=enemyY_change[i]
		elif enemyX[i] >=736:
			enemyX_change[i] = -0.4
			enemyY[i]+=enemyY_change[i]
		
		#collision check
		collision = if_collided(enemyX[i],enemyY[i],bulletX, bulletY)
		if collision:
			explosion_sound=mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY=480
			bullet_state="ready"
			score_value+=1
			enemyX[i]=random.randint(0,735)
			enemyY[i]=random.randint(50,150)
		
		enemy(enemyX[i], enemyY[i], i)
		
		
#bullet movement

	if bulletY<=0:
		bulletY=480
		bullet_state="ready"

	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change
		
#Final Display
		
	player(playerX,playerY)	#player movement
	show_score(scoreX,scoreY)	#score display
	
	pygame.display.update()
	
	
	
	
	
