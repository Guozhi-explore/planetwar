import pygame
from constants import *
class ImageManager:
	def __init__(self):
		self.background=pygame.image.load('image/background.png')
		self.background=pygame.transform.smoothscale(self.background,(USIZE*CLOUMNS,USIZE*ROWS))
		self.gameover=pygame.image.load('image/gameover.png')
		self.gameover=pygame.transform.smoothscale(self.gameover,(USIZE*CLOUMNS,USIZE*ROWS))
		self.picture=pygame.image.load('image/shoot.jpg')
		
	def get_plane1(self):
		rect=pygame.Rect(0,99,102,126)
		plane1=self.picture.subsurface(rect)
		return plane1

	def get_plane2(self):
		rect=pygame.Rect(165,360,102,126)
		plane2=self.picture.subsurface(rect)
		return plane2

	def get_plane_bullet(self):
		rect=pygame.Rect(66,76,15,24)
		bullet=self.picture.subsurface(rect)
		return bullet

	def get_enemy_bullet(self):
		rect=pygame.Rect(826,692,32,56)
		bullet=self.picture.subsurface(rect)
		return bullet

	def get_enemy(self):
		rect=pygame.Rect(536,613,54,41)
		enemy=self.picture.subsurface(rect)
		return enemy

	def get_enemy_king(self,times):
		rect0=pygame.Rect(508,746,166,255)
		rect1=pygame.Rect(5,488,160,257)
		rect2=pygame.Rect(848,752,156,247)
		rect3=pygame.Rect(677,750,163,254)
		if times==0:
			enemyKing=self.picture.subsurface(rect0)
		elif times==1:
			enemyKing=self.picture.subsurface(rect1)
		elif times==2:
			enemyKing=self.picture.subsurface(rect2)
		elif times>=3:
			enemyKing=self.picture.subsurface(rect3)
		return enemyKing

	def get_parachute(self):
		rect=pygame.Rect(265,396,92,90)
		parachute=self.picture.subsurface(rect)
		return parachute

