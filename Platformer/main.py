# importing libraries/modules
import pygame
from level1 import world_data1
from level2 import world_data2
from level3 import world_data3
from pygame.locals import *


# Initializing pygame
pygame.init()

# Setting the frame rate of screen 
clock = pygame.time.Clock()
fps = 60

# Initializing screen size
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Setting display name (top left)
pygame.display.set_caption('Intro to Python')

# Setting tile size. tile size * num tiles should be screen width. 
tile_size = 30

# Setting the game over condition. eg touching enemies
game_over = 0

# Setting the start menu condition 
start_menu = True

# Level variables (change when the player advances)
level = 1
max_levels = 3

# Loading background image
bg_img = pygame.image.load(r'C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Mushroom expansion\Backgrounds\bg_castle_square.png')

# Resize the background to screen size
resized_background = pygame.transform.scale(bg_img, (screen_width, screen_height)) 

# Loading the restart button 
restart_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\restart_button.png")
restart_img = pygame.transform.scale(restart_img,(148,68))

# Loading the start button 
start_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\start_button.png")
start_img = pygame.transform.scale(start_img,(148,68))

# Initialize a button class 
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.clicked = False
	
	def draw(self):
		# To keep track of what the mouse is doing. Starts as False, then if clicked will return True at the end of the function 
		action = False
		# Getting the mouse position 
		pos = pygame.mouse.get_pos()

		# Check if mouse is over the button, and that it has clicked 
		if self.rect.collidepoint(pos):
			# for debugging
			# print("mouse over")
			# Creates a list of mouse presses. 0 is left mouse click. 
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				# for debugging
				# print("clicked")
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
			self.clicked = False

		# Put in the button
		screen.blit(self.image,self.rect)

		return action 

# Initialize the player class 
class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def reset(self, x, y):
			self.images_right = []
			self.images_left = []
			self.index = 0
			self.counter = 0
			# Creating list of sprites for animation 
			for num in range(1, 12):
				img_right = pygame.image.load(f'C:/Users/User/Desktop/Y2S2/IntrotoPython/Platformer/platformer-art-complete-pack-0/Base pack/Player/p3_walk/PNG/p3_walk{num}.png')
				img_right = pygame.transform.scale(img_right, (30, 48.5))
				img_left = pygame.transform.flip(img_right, True, False)
				self.images_right.append(img_right)
				self.images_left.append(img_left)
			self.image = self.images_right[self.index]
			death_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_hurt.png")
			self.death_img = pygame.transform.scale(death_img, (30, 48.5))
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.width = self.image.get_width()
			self.height = self.image.get_height()
			self.vel_y = 0
			self.jumped = False
			# 1 = right, -1 = left
			self.direction = 1
			self.in_air = True

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 20

		if game_over == 0:

			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
				
			if key[pygame.K_UP] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1

			# if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
			# 	self.counter = 0
			# 	self.index = 0
			# 	if self.direction == 1:
			# 		self.image = self.images_right[self.index]
			# 	if self.direction == -1:
			# 		self.image = self.images_left[self.index]


			# Animating the player (left and right)
			if self.counter < walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			# Animating the jumping 
			if self.jumped == True:
				if self.direction == 1:
					img_jump = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_jump.png")
					img_jump = pygame.transform.scale(img_jump, (30, 48.5))
					self.image = img_jump
					
				if self.direction == -1:
					img_jump = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_jump.png")
					img_jump = pygame.transform.scale(img_jump, (30, 48.5))
					img_jump_left = pygame.transform.flip(img_jump, True, False)
					self.image = img_jump_left


			#a Adding gravity. Change velocity to make player jump higher/float more
			self.vel_y += 1
			if self.vel_y > 20:
				self.vel_y = 20
			dy += self.vel_y

			# Checking for collision with walls
			self.in_air = True
			for tile in world.tile_list:
				# x-axis
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				# y-axis
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					# Check if player is jumping upwards
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					# Check if player is falling downwards
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						if self.direction == 1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
							still_image = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_stand.png")
							still_image = pygame.transform.scale(still_image, (30, 48.5))
							self.image = still_image
						if self.direction == -1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
							still_image = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_stand.png")
							still_image = pygame.transform.scale(still_image, (30, 48.5))
							still_img_left = pygame.transform.flip(still_image,True,False)
							self.image = still_img_left
					self.in_air = False

			# Checking for collision with enemies
			if pygame.sprite.spritecollide(self, jelly_group, False):
				game_over = -1
			
			# Checking for collision with enemies
			if pygame.sprite.spritecollide(self, spikes_group, False):
				game_over = -1
				# for debugging
				# print(game_over)

			# Checking for collision with the door for exit
			if pygame.sprite.spritecollide(self, door_group, False):
				game_over = 1
		

			# Update player coordinates
			self.rect.x += dx
			self.rect.y += dy

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height
				dy = 0

		# Setting game over. Sprite changes and moves down 
		elif game_over == -1:
			if self.direction == 1:
				self.image = self.death_img
				self.rect.y += 5
			if self.direction == -1:
				self.image = pygame.transform.flip(self.death_img, True, False)
				self.rect.y += 5

		# Drawing the player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		return game_over



# Creating the groups for the different enemy classes
jelly_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

# Creating the enemy class 
class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		enemy_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Enemies\blockerMad.png")
		enemy_img = pygame.transform.scale(enemy_img, (tile_size,tile_size))
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 30:
			self.move_direction *= -1
			self.move_counter *= -1

# Creating a spikes class
class Spikes(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		spikes_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Ice expansion\Tiles\spikesBottomAlt2.png")
		spikes_img = pygame.transform.scale(spikes_img, (tile_size,tile_size))
		self.image = spikes_img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	
# Creating a doorway class
class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		door_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Buildings expansion\Tiles\windowOpen.png")
		door_img = pygame.transform.scale(door_img, (tile_size,tile_size))
		self.image = door_img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	
# Creating the world class 
class World():
	def __init__(self, data):
		self.tile_list = []

		# Loading textures
		ice_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Ice expansion\Tiles\iceBlock.png")
		tundra_img = pygame.image.load(r'C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Ice expansion\Tiles\tundraCenter.png')

		# Iterating through list of lists. Drawing textures
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(tundra_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(ice_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					jelly = Enemy(col_count * tile_size, row_count * tile_size)
					jelly_group.add(jelly)
				if tile == 4:
					door = Door(col_count * tile_size, row_count * tile_size)
					door_group.add(door)
				if tile == 6:
					spikes = Spikes(col_count * tile_size, row_count * tile_size)
					spikes_group.add(spikes)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# Creating instance of player. 
player = Player(30, screen_height - 130)

# Creating instance of world 
# if path.exists(f'level{level}.txt'):
# 	pickle_in = open(f'level{level}', 'rb')
# 	world_data = pickle.load(pickle_in)
def reset_level(level):
	player.reset(100, screen_height - 130)
	jelly_group.empty()
	spikes_group.empty()
	door_group.empty()

	#load in level data and create world
	if level == 1:
		world_data = world_data1
	elif level == 2: 
		world_data = world_data2
	elif level == 3: 
		world_data = world_data3
		

	world = World(world_data)

	return world

world = World(world_data1)

# Instances of the button class 
# Restart button 
restart_button = Button(screen_width // 2 - 75 , screen_height // 2 - 65, restart_img)

# Start button 
start_button = Button(screen_width // 2 - 75 , screen_height // 2 - 65, start_img)

# Writing a function that will restart a level



run = True
while run:

	clock.tick(fps)

	screen.blit(resized_background, (0, 0))

	if start_menu:
		if start_button.draw():
			start_menu = False

	else:

		world.draw()

		if game_over == 0:
			jelly_group.update()

		if game_over == -1:
			# This will return True if button is pressed, else will not return 
			if restart_button.draw():
				# for debugging
				# print('reset')
				# player.reset(30, screen_height - 130)
				world_data = []
				world = reset_level(level)
				game_over = 0
			

		if game_over == 1:
			level += 1
			if level <= max_levels:
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				if restart_button.draw():
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
		
		jelly_group.draw(screen)
		spikes_group.draw(screen)
		door_group.draw(screen)

		game_over = player.update(game_over)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()