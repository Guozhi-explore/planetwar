import pygame
from imagemanager import ImageManager
from constants import *

class Bullet:
	def __init__(self,screen,site,nature):
		self.site=site
		self.screen=screen
		self.nature=nature
		self.imagemanager=ImageManager()

	def move(self):
		if self.nature=='plane':
			self.site[1]=self.site[1]-0.5                                   #元组不支持修改删除
		elif self.nature=='enemy':
			self.site[1]+=0.5

	def show(self):
		if self.nature=='plane':
			self.screen.blit(self.imagemanager.get_plane_bullet(),(USIZE*self.site[0],USIZE*self.site[1]))
		elif self.nature=='enemy':
			self.screen.blit(self.imagemanager.get_enemy_bullet(),(USIZE*self.site[0],USIZE*self.site[1]))


class Plane:
	def __init__(self,screen):
		self.site=[CLOUMNS/2-1,ROWS-3]
		self.screen=screen
		self.imagemanager=ImageManager()

	def move(self,state):
		if state=='left' and self.site[0]>0:
			self.site[0]-=1
		elif state=='right' and self.site[0] <CLOUMNS-2:
			self.site[0]+=1
		else:
			pass

	def shoot(self):
		return Bullet(self.screen,[self.site[0]+1.5,self.site[1]],'plane')

	def show1(self):
		self.screen.blit(self.imagemanager.get_plane1(),(USIZE*self.site[0],USIZE*self.site[1]))

	def show2(self):
		self.screen.blit(self.imagemanager.get_plane2(),(USIZE*self.site[0],USIZE*self.site[1]))

class Enemy:
	def __init__(self,screen,site):
		self.screen=screen
		self.site=site
		self.imagemanager=ImageManager()

	def move(self):
		self.site[1]+=0.2

	def show(self):
		self.screen.blit(self.imagemanager.get_enemy(),(USIZE*self.site[0],USIZE*self.site[1]))

class EnemyKing:
	def __init__(self,screen,site):
		self.screen=screen
		self.site=site
		self.imagemanager=ImageManager()

	def move(self):
		self.site[1]+=0.08

	def show(self,times):
		self.screen.blit(self.imagemanager.get_enemy_king(times),(USIZE*self.site[0],USIZE*self.site[1]))

	def shoot(self):
		return Bullet(self.screen,[self.site[0]+2.5,self.site[1]+7],'enemy')

class Parachute:
	def __init__(self,screen,site):
		self.screen=screen
		self.site=site
		self.imagemanager=ImageManager()

	def move(self):
		self.site[1]+=0.4

	def show(self):
		self.screen.blit(self.imagemanager.get_parachute(),(USIZE*self.site[0],USIZE*self.site[1]))



