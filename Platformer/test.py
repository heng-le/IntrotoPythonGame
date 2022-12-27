import pygame
from pygame.locals import *

#initialize pygame
pygame.init()


#initialize pygame
clock = pygame.time.Clock()
fps = 60

#initialize the screen size
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('YNC Platform Game')

#define game variables
# To make sure that it will fit the screen, make sure that tile_size * num tiles = screen_width/height
tile_size = 30


#load images
# sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load(r'C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Mushroom expansion\Backgrounds\bg_castle_square.png')

# Resize the background to screen size
resized_background = pygame.transform.scale(bg_img, (screen_width, screen_height)) 


# Initialize class for the player
# x and y are the coordinates of the player  
class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 12):
			img_right = pygame.image.load(f'C:/Users/User/Desktop/Y2S2/IntrotoPython/Platformer/platformer-art-complete-pack-0/Base pack/Player/p3_walk/PNG/p3_walk{num}.png')
			img_right = pygame.transform.scale(img_right, (30, 48.5))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 5

		#get keypresses
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.jumped == False:
			self.vel_y = -15
			self.jumped = True
			
		if key[pygame.K_UP] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			dx -= 5
			self.direction = -1
			self.image = self.images_left[self.index]
			
		if key[pygame.K_RIGHT]:
			dx += 5
			self.direction = 1
			self.image = self.images_right[self.index]
			
		if key[pygame.K_ESCAPE]:
			pygame.quit()
		if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
			if self.direction == -1:
				still_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_stand.png")
				still_img = pygame.transform.scale(still_img, (30, 48.5))
				still_img_left = pygame.transform.flip(still_img,True,False)
				self.image = still_img_left
			else:
				still_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_stand.png")
				still_img = pygame.transform.scale(still_img, (30, 48.5))
				self.image = still_img
				


		# Animating player
		self.index += 1
		if self.index >= len(self.images_right):
			self.index = 0
		# if self.direction == 1:
			self.image = self.images_right[self.index]
		# if self.direction == -1:
		# 	self.image = self.images_left[self.index]
	
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


		# Add gravity so that player can jump
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		# Check for collision
		for x in world.tile_list:
			# X-axis
			if x[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			# Y-axis
			if x[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# Check if jumping
				if self.vel_y < 0:
					dy = x[1].bottom - self.rect.top
					self.vel_y = 0
				# Check if falling
				elif self.vel_y >= 0:
					dy = x[1].top - self.rect.bottom
					self.vel_y = 0
					still_image = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Base pack\Player\p3_stand.png")
					still_image = pygame.transform.scale(still_image, (30, 48.5))
					self.image = still_image




		# Updating player coordinates
		self.rect.y += dy
		self.rect.x += dx

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0

		#draw player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)




class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		ice_img = pygame.image.load(r"C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Ice expansion\Tiles\iceBlock.png")
		tundra_img = pygame.image.load(r'C:\Users\User\Desktop\Y2S2\IntrotoPython\Platformer\platformer-art-complete-pack-0\Ice expansion\Tiles\tundraCenter.png')

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
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)



world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)
world = World(world_data)

running = True
while running:

	clock.tick(fps)

	screen.blit(resized_background, (0, 0))
	# screen.blit(sun_img, (100, 100))

	world.draw()

	player.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()

pygame.quit()