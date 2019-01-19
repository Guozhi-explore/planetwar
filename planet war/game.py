import random
import pygame,sys
from pygame.locals import *
from constants import *
from soundmanager import SoundManager
from imagemanager import ImageManager
from constants import *
from role import *
class Game:
	def __init__(self):
		pygame.init()
		self.screen=pygame.display.set_mode(size)
		self.soundmanager=SoundManager()
		self.imagemanager=ImageManager()
		self.plane=Plane(self.screen)
		self.STATE='waiting'
		self.enemykingexist=False
		self.parachuteexist=False
		self.enemylist=[]
		self.bulletlist=[]
		self.enemybulletlist=[]
		self.score=0
		self.level=0
		self.chance=5
		self.chioce=0                          #select difficulty
		self.degree=DEGREE[self.chioce]
		self.speed=self.degree['initspeed']
		self.enemykingtimes=0
		self.clock=0

	def play(self):
		#self.draw()
		while True:
			for event in pygame.event.get():
				if event.type==KEYDOWN:
					if event.key== K_ESCAPE:
						sys.exit()
					if self.STATE=='waiting':
						self.drawmenu()
						if event.key in(K_DOWN,K_s):
							self.chioce=(self.chioce+1)%3
						if event.key in(K_UP,K_w):
							self.chioce=(self.chioce+2)%3
						if event.key ==K_RETURN:
							self.init_game()
					if self.STATE=='playing':
						if event.key in (K_LEFT,K_a):
							self.plane.move('left')
						elif event.key in (K_RIGHT,K_d):
							self.plane.move('right')
					if self.STATE=='gameover':
						self.soundmanager.play_fail_sound()
						if event.key==K_RETURN:
							self.init_game()
						if event.key==K_SPACE:
							self.STATE='waiting'
				if event.type==QUIT:
					sys.exit()
			if self.STATE=='playing':
				#shoot
				if self.clock%self.degree['shoot period']==0:
					self.bulletlist.append(self.plane.shoot())
				for bullet in self.bulletlist:
					bullet.move()
				if len(self.bulletlist)>0:
					if self.bulletlist[0].site[1]<=0:
						self.bulletlist.pop(0)

				#enemy assault
				if self.clock%self.degree['enemy period']==0:
					temp_x = random.randint(1,CLOUMNS-2)
					temp_enemy=Enemy(self.screen,[temp_x,0])
					self.enemylist.append(temp_enemy)
				for enemy in self.enemylist:
					enemy.move()
				if len(self.enemylist)>0 and self.enemylist[0].site[1]>ROWS-3:
					self.enemylist.pop(0)
					self.chance-=1
					if self.chance<=0:
						self.STATE='gameover'

				#enemyking assault
				if self.score%self.degree['enemyking period']==0 and self.enemykingexist==False:
					self.enemyking=EnemyKing(self.screen,[random.randint(1,CLOUMNS-4),0])
					self.enemykingtimes=0
					self.enemykingexist=True
				if self.enemykingexist==True:
					self.enemyking.move()
					if self.enemyking.site[1]>ROWS-3:
						self.STATE='gameover'
					if self.clock%(self.degree['enemyking period']-self.level)==0:                                          #enemy shooting frequency is related to the level
						self.enemybulletlist.append(self.enemyking.shoot())
				if len(self.enemybulletlist)>0:
					if abs(self.enemybulletlist[0].site[0]-self.plane.site[0]-0.8)<=1 and \
					abs(self.enemybulletlist[0].site[1]-0.8-self.plane.site[1])<=1:
						self.chance-=1
						self.enemybulletlist.pop(0)
						if self.chance<=0:
							self.STATE='gameover'
				if len(self.enemybulletlist)>0:
					if self.enemybulletlist[0].site[1]>ROWS-2:
						self.enemybulletlist.pop(0)
				for enemybullet in self.enemybulletlist:
					enemybullet.move()
					
				#shoot successfully
				for bullet in self.bulletlist:
					for enemy in self.enemylist:
						if abs(bullet.site[0]-enemy.site[0]-0.8)<=0.8 and \
						 abs(bullet.site[1]-enemy.site[1]-0.8)<=0.8:
							self.bulletlist.remove(bullet)
							self.enemylist.remove(enemy)
							self.score+=1
				for bullet in self.bulletlist:
					if abs(bullet.site[0]-self.enemyking.site[0]-3)<=2 and \
					abs(bullet.site[1]-self.enemyking.site[1]-3)<=2:
						self.enemykingtimes+=0.7
						self.bulletlist.remove(bullet)
						if self.enemykingtimes>3:
							self.soundmanager.play_shoot_sound()
							self.enemykingexist=False                            #if enemyking is shooted more than three times,it will disappear
				#parachute
				if random.randint(500,500+self.degree['parachute period'])==520 and self.parachuteexist==False:
					self.parachute=Parachute(self.screen,[random.randint(1,ROWS-3),0])
					self.parachuteexist=True
				if self.parachuteexist==True:
					self.parachute.move()
					if abs(self.plane.site[0]-self.parachute.site[0]+0.3)<1.5 and \
					 abs(self.plane.site[1]-self.parachute.site[1]-0.5)<1.5:
						self.chance+=1
						self.parachuteexist=False
				if self.parachuteexist==True:
					if self.parachute.site[1]>ROWS-2:
						self.parachuteexist=False

				#accelerate
				level_temp=self.level
				self.level=int((self.score+1)**0.5 /3)
				if self.level>level_temp:
					self.soundmanager.play_cheer_sound()
				self.speed=self.degree['initspeed']+self.speed

				self.draw()
				self.clock+=1

			if self.STATE=='gameover':
				self.drawfinal()
			if self.STATE=='waiting':
				self.drawmenu()

			pygame.display.update()
			pygame.time.Clock().tick(self.speed)
			
			

	def init_game(self):
		self.plane=Plane(self.screen)
		self.STATE='playing'
		self.enemykingexist=False
		self.parachuteexist=False
		self.enemylist=[]
		self.bulletlist=[]
		self.enemybulletlist=[]
		self.score=0
		self.level=0
		self.chance=5
		self.degree=DEGREE[self.chioce]
		self.speed=self.degree['initspeed']
		self.enemykingtimes=0
		self.clock=0

	def draw(self):
		self.screen.blit(self.imagemanager.background,(0,0))
		self.plane.show1()
		for bullet in self.bulletlist:
			bullet.show()
		for enemy in self.enemylist:
			enemy.show()
		if self.enemykingexist==True:
			self.enemyking.show(int(self.enemykingtimes))
		for enemybullet in self.enemybulletlist:
			enemybullet.show()
		if self.parachuteexist==True:
			self.parachute.show()

		scoreText=pygame.font.SysFont('楷体',30).render \
		('SCORE:'+str(self.score),True,(10,20,200))
		self.screen.blit(scoreText,(0,0))
		levelText=pygame.font.SysFont('楷体',30).render \
		('LEVEL:'+str(self.level),True,(10,20,200))
		self.screen.blit(levelText,(0,20))
		chanceText=pygame.font.SysFont('楷体',30).render \
		('CHANCE:'+str(self.chance),True,(10,20,200))
		self.screen.blit(chanceText,(0,40))
		degreeText=pygame.font.SysFont('楷体',30).render \
		('DEGREE:'+Degree[self.chioce],True,(10,20,200))
		self.screen.blit(degreeText,(0,60))

	def drawfinal(self):
		f=open('score.csv','r')
		score_hign=f.read().split(',')
		f.close()
		if int(score_hign[self.chioce])<self.score:
			score_hign[self.chioce]=str(self.score)
			f=open('score.csv','w')
			f.write(score_hign[0]+','+score_hign[1]+','+score_hign[2])
			f.close()
		self.screen.blit(self.imagemanager.background,(0,0))
		overText=pygame.font.SysFont('楷体',30).render(u'GAMEOVER!',True,(0,0,255))
		scoreText=pygame.font.SysFont('楷体',30).render(u'SCORE:'+str(self.score),True,(0,0,255))
		againText=pygame.font.SysFont('楷体',30).render(u'press enter to try again',True,(0,0,255))
		menuText=pygame.font.SysFont('楷体',30).render(u'press space and trun to the menu',True,(0,0,255))
		hignsocreText=pygame.font.SysFont('楷体',30).render(u'hignest score:'+score_hign[self.chioce],True,(0,0,255))
		self.screen.blit(overText,(150,200))
		self.screen.blit(scoreText,(150,230))
		self.screen.blit(hignsocreText,(150,260))
		self.screen.blit(againText,(150,290))
		self.screen.blit(menuText,(150,320))

	def drawmenu(self):
		self.screen.blit(self.imagemanager.background,(0,0))
		easyText=pygame.font.SysFont('楷体',40).render(u'EASY',True,(0,0,255))
		mediumText=pygame.font.SysFont('楷体',40).render(u'MEDIUM',True,(0,0,255))
		difficultText=pygame.font.SysFont('楷体',40).render(u'DIFFICULT',True,(0,0,255))
		if self.chioce==0:
			easyText=pygame.font.SysFont('楷体',40).render(u'EASY',True,(255,0,0))
		elif self.chioce==1:
			mediumText=pygame.font.SysFont('楷体',40).render(u'MEDIUM',True,(255,0,0))
		elif self.chioce==2:
			difficultText=pygame.font.SysFont('楷体',40).render(u'DIFFICULT',True,(255,0,0))
		self.screen.blit(easyText,(180,250))
		self.screen.blit(mediumText,(180,300))
		self.screen.blit(difficultText,(180,350))

if __name__=='__main__':
	game=Game()
	game.play()

