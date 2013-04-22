import pygame
from random import randint
from shapes import *

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)

FINESTRA = (800,640)

FORME = {0:T_SHAPE,1:Z_SHAPE,2:S_SHAPE,3:J_SHAPE,4:L_SHAPE,5:O_SHAPE,6:I_SHAPE}

quadratini = []
def draw_text(screen,msg,cord):
	font = pygame.font.SysFont('Comic Sans MS',30)
	label = font.render(msg,1,red)
	screen.blit(label,cord)
def gravity(quadrati):
	changed = False
	for q in quadrati:
		if (q[0],q[1]+1) not in quadrati and q[1]+1<20:
			quadrati.append((q[0],q[1]+1))
			quadrati.remove(q)
			changed = True
	if changed==False:
		return quadrati
	else:
		return gravity(quadrati)
def explodeLine(quadrati):
	if len(quadrati)<10:
		return quadrati
	for r in range(20):
		count = 0
		da_eliminare = []
		for c in range(10):
			if (c,r) in quadrati:
				count+=1
				da_eliminare.append((c,r))				
		if count==10:
			for el in da_eliminare:
				quadrati.remove(el)
	return quadrati
def addSquares(q,cord):
	for c in cord:
		q.append(c)
	return q
def draw_square(surf,x,y,color):
	surf.blit(IMAGES[color],(x,y))	
def draw_base(surf,s):
	x,y = 20,20
	for i in range(0,650,30):
		pygame.draw.line(surf,black,(x,y+i),(x+300,y+i),1)
	for i in range(0,320,30):
		pygame.draw.line(surf,black,(x+i,y),(x+i,y+600),1)
	pygame.draw.rect(surf,green,(340,120,440,400),2)
	draw_text(surf,'Comandi:',(350,130))
	draw_text(surf,'a,s,d --> Sinistra,giu,destra',(350,170))
	draw_text(surf,'p,k --> Pausa,ruota',(350,200))
	draw_text(surf,'Spazio --> Giu veloce',(350,235))
	draw_text(surf,'Score:'+str(s),(450,300))
	
class Block():
	def __init__(self,scelta_forma,x,y,color):
		self.status = 'Falling'
		self.x,self.y = (x,y)
		self.orient = 0
		self.forma = FORME[scelta_forma]
		self.color = color	
	def draw_me(self,screen):
		self.cord = []
		for r in range(5):
			for c in range(5):
				if self.forma[self.orient][r][c]==1:
					if self.x+c>9 or self.x+c<0 or self.y+r>19:
						raise
					if (self.x+c,self.y+r) in quadratini:
						raise 
					draw_square(screen,(20+self.x*30+c*30),(20+self.y*30+r*30),self.color)
					self.cord.append((self.x+c,self.y+r))
	def move(self,direction,screen):
		if direction=='dx':
			self.x+=1
			try:
				self.draw_me(screen)
			except:
				self.x-=1
		if direction=='sx':
			self.x-=1
			try:
				self.draw_me(screen)
			except:
				self.x+=1
		if direction=='giu':
			self.y+=1
			try:
				self.draw_me(screen)
			except:
				self.y-=1
				self.status = 'Stuck'		
	def ruota(self,screen):
		massimo = len(self.forma)
		self.orient+=1
		if self.orient==massimo:
			self.orient=0
		try:
			self.draw_me(screen)
			return
		except:
			self.orient-=1
			if self.orient==-1:
				self.orient=massimo
			self.draw_me(screen)		
	def isStuck(self):
		return self.status=='Stuck'
	def maxDown(self,screen):
		while(self.status=='Falling'):
			self.move('giu',screen)
pygame.init()

screen = pygame.display.set_mode(FINESTRA)

pygame.display.set_caption('Tetris by gyosko')

IMAGES = []
for i in range(4):
	IMAGES.append(pygame.image.load('img/block'+str(i)+'.png').convert())

done = False
blocco_in_gioco = False
count = 0
score = 0
lost = False
paused = False
clock = pygame.time.Clock()


while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a and paused==False:
				b.move('sx',screen)
			if event.key == pygame.K_d and paused==False:
				b.move('dx',screen)
			if event.key == pygame.K_s and paused==False:
				b.move('giu',screen)
			if event.key == pygame.K_k and paused==False:
				b.ruota(screen)
			if event.key == pygame.K_SPACE and paused==False:
				b.maxDown(screen)
			if event.key == pygame.K_p:
				paused = not paused
			if event.key == pygame.K_g and lost==True:
				quadratini = []
				try:
					del b
				except:
					pass
				lost = False
				blocco_in_gioco = False
				score = 0
	screen.fill(white)
	if lost:
		screen.fill(white)
		draw_text(screen,'Hai perso!',(250,200))
		draw_text(screen,'Premi g per giocare ancora',(250,250))
	if paused and lost==False:
		for q in quadratini:
			draw_square(screen,20+30*q[0],20+30*q[1],0)
		b.draw_me(screen)
		draw_base(screen,score)
	if paused==False and lost==False:
		count+=1 
		if blocco_in_gioco==False:
			b = Block(randint(0,6),3,-1,randint(1,3))
			blocco_in_gioco=True
		if blocco_in_gioco==True and count==60:
			b.move('giu',screen)
			count=0
		
		try:
			b.draw_me(screen)
			numQuadratini = len(quadratini)
			quadratini = explodeLine(quadratini)
			if numQuadratini!=len(quadratini):
				quadratini = gravity(quadratini)
				score+=10*(numQuadratini-len(quadratini))*(numQuadratini-len(quadratini))//10
			for q in quadratini:
				draw_square(screen,20+30*q[0],20+30*q[1],0)
			draw_base(screen,score)
			if b.isStuck():
				quadratini = addSquares(quadratini,b.cord)
				del b
				blocco_in_gioco=False
		except:
			lost = True
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()