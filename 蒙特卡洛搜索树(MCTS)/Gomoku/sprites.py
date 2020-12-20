import pygame
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y, mov):
		self.groups = game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pygame.Surface((TILESIZE / 2, TILESIZE / 2))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.mov = mov

	def move(self, dx = 0, dy = 0):
		oldx = self.x 
		oldy = self.y
		self.x += dx
		self.y += dy
		if (self.x * TILESIZE) < X_MIN_BOUND or (self.x * TILESIZE - TILESIZE / 4) > X_MAX_BOUND or self.mov == 0:
			self.x = oldx
		if (self.y * TILESIZE) < Y_MIN_BOUND or (self.y * TILESIZE - TILESIZE / 4) > Y_MAX_BOUND or self.mov == 0:
			self.y = oldy

	def update(self):
		self.rect.x = self.x * TILESIZE - TILESIZE / 4
		self.rect.y = self.y * TILESIZE - TILESIZE / 4


class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pygame.Surface((TILESIZE / 2, TILESIZE / 2))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y

	def update(self):
		self.rect.x = self.x * TILESIZE - TILESIZE / 4
		self.rect.y = self.y * TILESIZE - TILESIZE / 4
	

