AW='assets/enemy_shoot.wav'
AV='BlueTurret'
AU='Strafer'
AT='assets/redBoss.png'
AS='assets/cargoShip.png'
AR='Laser Cannon'
AQ='assets/explosion.wav'
AP='Bomb'
AO='Laser Beam'
AN='Stage '
AM='.png'
AL='assets/explosion/'
AK='Comic Sans MS'
AJ=ValueError
A9='highscore'
A8='hs.json'
A7='Upgrade Shield Regen Speed'
A6='Upgrade Laser Cannon Speed'
A5='Upgrade Laser Cannon Cooldown'
A4='Upgrade Laser Cannon Damage'
A3=print
A2=open
x='Upgrade Bomb Cooldown'
w='Upgrade Bomb Damage'
v='Upgrade Laser Beam Duration'
u='Upgrade Laser Beam Damage'
m=range
a=int
X='Buy Bomb'
W='Buy Laser Beam'
T=len
N=str
K=isinstance
H=False
D=True
import pygame as B,random as J,math as U,json as q
B.init()
B.font.init()
B.mixer.init()
b=1920
Q=1080
I=B.font.SysFont(AK,30)
y=60
g=0
R=[]
r=[]
d=[]
e=[]
h=[]
n=[]
i=J.choice([1,-1])
j=J.choice([1,-1])
k=J.choice([1,-1])
l=J.choice([1,-1])
for AA in m(12):r.append(B.image.load(AL+N(AA)+AM))
class s:
	def __init__(A):A.background=B.image.load('assets/background.png');A.enemyCap=10;A.toSpawn=10;A.spawned=0;A.stageEnd=300;A.enemyProgression=1;A.level=1;A.bossDead=H;A.changeText=I.render(AN+N(A.level),D,(255,255,255));A.enemies=[];A.test=H;A.shop=AB();A.title=AC();B.mixer.music.load('assets/background.wav');B.mixer.music.set_volume(0.1);B.mixer.music.play(-1)
	def advance(B):
		B.level+=1;B.enemyCap=5+U.ceil(B.level**0.5)*5;B.toSpawn=9+B.level;B.spawned=0;B.shop.active=D;B.stageEnd=300;B.changeText=I.render(AN+N(B.level),D,(255,255,255))
		if B.level%5==0:G.hpMulti+=0.5;A.moneyMulti+=0.1
		if B.level>=6:B.enemyProgression=4
		elif B.level>=3:B.enemyProgression=3
		elif B.level>=2:B.enemyProgression=2
	def spawnBoss(A):B=[M()];A.enemies.append(J.choice(B.copy()))
	def paused(A):
		C.blit(A.background,(0,0))
		for B in m(T(A.enemies)):A.enemies[B].draw()
	def update(A):
		global AX;C.blit(A.background,(0,0))
		if A.title.active:A.title.update()
		elif A.shop.active:A.shop.update()
		elif A.stageEnd>0:A.stageEnd-=1;C.blit(A.changeText,A.changeText.get_rect(center=C.get_rect().center))
		elif T(A.enemies)==0 and A.spawned>=A.toSpawn:
			if A.level%5==0:
				if A.bossDead:A.advance()
				else:A.spawnBoss()
			else:A.bossDead=H;A.advance()
		else:
			for B in A.enemies:B.update()
class AB:
	def __init__(A):A.active=H;A.items={A4:[1,-1,1500,[500,1.2,1.01],[0,0,3]],A5:[1,9,3000,[0,1.5],[0,0]],A6:[1,11,500,[100],[0]],W:[0,1,10000,[],[]],u:[0,-1,10000,[5000,1.2,1.07],[0,0,3]],v:[0,11,100000,[0,2],[0,0]],X:[0,1,30000,[],[]],w:[0,-1,10000,[5000,1.2,1.07],[0,0,3]],x:[0,11,50000,[0,1.5,1.1],[0,0,5]],A7:[1,10,10000,[0,1.5,1.1],[0,0,3]]};A.itemKeys=[A4,A5,A6,W,u,v,X,w,x,A7];A.clickToggle=H
	def buy(D,item):
		C=item
		if C in D.items:
			B=D.items[C]
			if C==X and D.items[W]==0:return
			if(B[0]<B[1]or B[1]==-1)and A.money>=B[2]and(B[0]!=0 or C in[W,X])and not(C==X and D.items[W][0]==0):
				B[0]+=1;A.money-=a(B[2])
				for E in m(T(B[4])):
					if B[0]>B[4][E]:
						if E==0:B[2]+=B[3][0]
						elif E==1:B[2]=B[2]*B[3][1]
						elif E==2:B[2]=B[2]**B[3][2]
					else:break
				if C==A4:o.damage+=0.25
				elif C==A5:A.bullet_firerate-=10
				elif C==A6:A.bulletSpeed+=3
				elif C==W:A.unlockedWeapons.append(AO);D.items[u][0]=1;D.items[v][0]=1
				elif C==u:P.damage+=0.01
				elif C==v:A.laserDuration+=50
				elif C==X:D.items[w][0]=1;D.items[x][0]=1;A.unlockedWeapons.append(AP)
				elif C==w:z.damage+=0.5
				elif C==x:A.bomb_firerate-=100
				elif C==A7:A.shieldRegenSpeed=U.ceil(500*0.95**B[0])
	def display(E):
		S='Lv. ';J=150;L=200;K=500;M=100;Q=50;R=50;E.buttons=[];G=0
		for F in E.items:
			if A.money>=E.items[F][2]and(E.items[F][0]<E.items[F][1]or E.items[F][1]==-1)and(E.items[F][0]!=0 or F in[W,X])and not(F==X and E.items[W][0]==0):O=0,255,0
			else:O=220,220,220
			E.buttons.append(B.Rect(J,L,K,M));B.draw.rect(C,O,E.buttons[G]);C.blit(I.render(F,D,(0,0,0)),E.buttons[G]);C.blit(I.render('$'+N(a(E.items[F][2]))[:-2]+'.'+N(a(E.items[F][2]))[-2:],D,(0,0,0)),E.buttons[G].copy().move(0,50))
			if E.items[F][0]==0 and F not in[W,X]or F==X and E.items[W][0]==0:C.blit(I.render('Locked',D,(0,0,0)),E.buttons[G].copy().move(350,50))
			elif E.items[F][1]==-1:C.blit(I.render(S+N(E.items[F][0]),D,(0,0,0)),E.buttons[G].copy().move(350,50))
			elif E.items[F][0]<E.items[F][1]:C.blit(I.render(S+N(E.items[F][0])+'/'+N(E.items[F][1]),D,(0,0,0)),E.buttons[G].copy().move(350,50))
			elif E.items[F][0]>=E.items[F][1]:C.blit(I.render('Lv. MAX',D,(0,0,0)),E.buttons[G].copy().move(350,50))
			J+=K+Q
			if J+K+100>b:J=150;L+=M+R
			G+=1
		P=I.render('Press ENTER to Continue',H,(255,255,255));C.blit(P,(C.get_width()/2-P.get_width()/2,3*C.get_height()/4))
	def detectClick(A):
		F=B.mouse.get_pos();C=B.mouse.get_pressed()
		if C[0]and not A.clickToggle:
			A.clickToggle=D
			for E in m(T(A.buttons)):
				if A.buttons[E].collidepoint(F):A.buy(A.itemKeys[E])
		elif not C[0]:A.clickToggle=H
	def update(A):
		C=B.key.get_pressed()
		if C[B.K_RETURN]:A.active=H
		A.detectClick();A.display()
class AC:
	def __init__(A):C='assets/fonts/IshimuraRegular.otf';A.active=D;A.titleFont=B.font.Font(C,108);A.contFont=B.font.Font(C,44)
	def display(E):
		F=E.titleFont.render('Space Force',D,(249,4,5));A=E.contFont.render('Press ENTER to Play!',D,(255,255,255));G=I.render('Press Q to Exit',H,(255,255,255))
		with A2(A8,'r')as J:K=q.loads(J.read())[A9]
		B=I.render(f"Highscore: {K}",H,(255,255,255));L=F.get_rect().width;M=A.get_rect().width;N=A.get_rect().height;C.blit(F,(960-L//2,25));C.blit(A,(960-M//2,540-N//2));C.blit(G,(960-G.get_width()//2,C.get_height()-50));C.blit(B,(C.get_width()-B.get_width()-30,C.get_height()-B.get_height()-20))
	def update(A):
		C=B.key.get_pressed()
		if C[B.K_RETURN]:A.active=H
		A.display()
class t:
	def __init__(A):A.dead=H
class E(t):
	playerSprite=B.image.load('assets/Ship.png');shieldSprite=B.image.load('assets/Shield.png');width=playerSprite.get_width();height=playerSprite.get_height();shieldWidth=shieldSprite.get_width();shieldHeight=shieldSprite.get_height();laserSound=B.mixer.Sound('assets/laser.wav');laserSound.set_volume(0.2);bulletSound=B.mixer.Sound('assets/bullet.wav');shipHit=B.mixer.Sound('assets/ship_hit.wav');shipHit.set_volume(0.3);shieldHit=B.mixer.Sound('assets/shield_hit.wav');shieldHit.set_volume(0.2);reloadSound=B.mixer.Sound('assets/reloaded.wav');reloadSound.set_volume(0.1);shieldBreak=B.mixer.Sound('assets/shield_break.wav');shieldBreak.set_volume(0.5);shipExplode=B.mixer.Sound(AQ);shipExplode.set_volume(0.5);regenSound=B.mixer.Sound('assets/shield_regen.wav');regenSound.set_volume(0.3);gameLose=B.mixer.Sound('assets/lose.wav');gameLose.set_volume(0.5)
	def __init__(A):super().__init__();A.coords=[25,(Q-E.height)/2];A.hp=3;A.shield=5;A.shieldMax=5;A.shieldRegenSpeed=500;A.shieldTimer=0;A.speed=3;A.bulletCD=0;A.bullet_firerate=200;A.laserCD=0;A.laser_firerate=1000;A.laserTime=0;A.laserDuration=300;A.bombCD=0;A.bomb_firerate=1500;A.bullets=[];A.bombs=[];A.bulletSpeed=20;A.bulletDistance=b*3/4;A.bombDistance=1450;A.bombRadius=200;A.weapon=0;A.unlockedWeapons=[AR];A.invTime=0;A.money=0;A.moneyMulti=1;A.score=0
	def getWeapon(A):return A.weapon
	def switchWeapon(A,slot):
		A.weapon=slot
		if A.weapon<0:A.weapon=T(A.unlockedWeapons)-1
		elif A.weapon>=T(A.unlockedWeapons):A.weapon=0
	def shoot(A):
		if A.unlockedWeapons[A.weapon]==AR:
			if A.bulletCD<=0:A.bullets.append(o(A.coords.copy(),A.bulletSpeed,0));A.bulletCD=A.bullet_firerate;E.bulletSound.play()
		elif A.unlockedWeapons[A.weapon]==AO:
			if A.laserCD<=0 and A.laserTime<A.laserDuration:A.bullets.append(P(A.coords.copy(),0));A.laserTime+=1;E.laserSound.play()
			elif A.laserTime>=A.laserDuration:A.laserCD=A.laser_firerate;A.laserTime=0;E.laserSound.fadeout(300)
		elif A.unlockedWeapons[A.weapon]==AP:
			if A.bombCD<=0:A.bombs.append(z(A.coords.copy(),A.bombDistance,A.bombRadius,0));A.bombCD=A.bomb_firerate;E.bulletSound.play()
	def collide(C,other):
		D=other
		if K(D,G)and not C.invTime:
			C.invTime=50
			if C.shield:
				C.shield-=1;F=J.randrange(-25,25);H=0;R.append([50,[0,D.coords[0]+F,D.coords[1]+H]])
				if C.shield==0:E.shieldBreak.play()
				else:E.shieldHit.play()
			else:
				C.hp-=1;F=J.randrange(-25,25);H=0;R.append([50,[0,D.coords[0]+F,D.coords[1]+H]])
				if C.hp==0:
					E.shipExplode.play();B.mixer.stop();B.mixer.music.stop();E.gameLose.play()
					with A2(A8,'r')as I:L=q.loads(I.read())
					if L[A9]<A.score:
						with A2(A8,'w')as I:I.write(q.dumps({A9:A.score}))
				else:E.shipHit.play()
			if C.shield<=0:C.shieldTimer=C.shieldRegenSpeed*-1
	def regenShield(A):
		if A.shield<A.shieldMax:A.shieldTimer+=1
		if A.shieldTimer>=A.shieldRegenSpeed:A.shield+=1;E.regenSound.play();A.shieldTimer=0
	def earn(A,amt):A.money+=amt*A.moneyMulti;A.score+=amt*A.moneyMulti
	def update(A,shopactive):
		C.blit(E.playerSprite,A.coords)
		if not shopactive:
			A.regenShield()
			if A.bulletCD>0:
				A.bulletCD-=1
				if A.bulletCD==0:E.reloadSound.play()
			if A.laserCD>0:
				A.laserCD-=1
				if A.laserCD==0:E.reloadSound.play()
			if A.bombCD>0:
				A.bombCD-=1
				if A.bombCD==0:E.reloadSound.play()
			if A.invTime>0:A.invTime-=1
		if A.shield>0:C.blit(E.shieldSprite,[A.coords[0]-(E.shieldWidth-E.width)/2,A.coords[1]-(E.shieldHeight-E.height)/2])
		for D in A.bullets:D.update()
		for B in A.bombs:
			B.update()
			if B.dead:A.bombs.remove(B)
	def paused(A):
		C.blit(E.playerSprite,A.coords)
		if A.shield>0:C.blit(E.shieldSprite,[A.coords[0]-(E.shieldWidth-E.width)/2,A.coords[1]-(E.shieldHeight-E.height)/2])
		for B in A.bullets:B.draw()
class Y(t):
	def __init__(A,coords,speed,angle):super().__init__();A.coords=coords;A.speed=speed;A.angle=angle
	def move(A):
		A.coords[0]+=U.cos(A.angle)*A.speed;A.coords[1]+=U.sin(A.angle)*A.speed
		if A.coords[0]>b:A.dead=D
class o(Y):
	sprite=B.image.load('assets/playerBullet.png');width=sprite.get_width();height=sprite.get_height();damage=1
	def __init__(A,coords,speed,angle):super().__init__(coords,speed,angle)
	def collide(B,other):
		A=other
		if K(A,G)and not K(A,f):B.dead=D
	def update(A):A.move();C.blit(o.sprite,A.coords)
	def draw(A):C.blit(o.sprite,A.coords)
class P(Y):
	baseSprite=B.image.load('assets/laser_base.png');sprite=B.image.load('assets/laser.png');width=sprite.get_width();height=sprite.get_height();baseOffsetY=(baseSprite.get_height()-height)/2;damage=0.05
	def __init__(C,coords,angle,speed=sprite.get_width()):B=coords;super().__init__([B[0]+A.width*5/7,B[1]+(A.height-P.height)/2],speed,angle)
	def collide(B,other):
		A=other
		if K(A,G)and not K(A,f):B.dead=D
	def update(B):
		B.move()
		if B.coords!=[A.coords[0]+A.width*5/7+P.width,A.coords[1]+(A.height-P.height)/2]:C.blit(P.sprite,B.coords)
		else:C.blit(P.baseSprite,[B.coords[0],B.coords[1]-P.baseOffsetY])
	def draw(B):
		if B.coords!=[A.coords[0]+A.width*5/7+P.width,A.coords[1]+(A.height-P.height)/2]:C.blit(P.sprite,B.coords)
		else:C.blit(P.baseSprite,[B.coords[0],B.coords[1]-P.baseOffsetY])
class z(Y):
	sprite=B.image.load(AS);redSprite=B.image.load(AT);width=sprite.get_width();height=sprite.get_height();bombExplosionSprites=r.copy();damage=5
	def __init__(A,coords,bombDistance,radius,angle):
		C=radius;super().__init__(coords,None,angle);A.fuse=400;A.timer=0;A.speed=bombDistance/200;A.radius=C;A.explosionSprites=[]
		for D in m(12):A.explosionSprites.append(B.transform.scale(B.image.load(AL+N(D)+AM),(C*2,C*2)))
	def move(A):
		A.coords[0]+=A.speed
		if A.speed>0:A.coords[0]+=U.cos(A.angle)*A.speed;A.coords[1]+=U.sin(A.angle)*A.speed;A.speed-=0.04
		elif A.speed!=0:A.speed=0
	def explode(A):C.blit(A.explosionSprites[a(A.explosions[0])],(A.explosions[1],A.explosions[2]));A.explosions[0]+=0.25
	def update(B):
		B.timer+=1
		if B.timer<=B.fuse:
			B.move();C.blit(B.sprite,B.coords)
			if B.timer==B.fuse:
				B.explosions=[0,B.coords[0]+B.width/2-B.radius,B.coords[1]+B.height/2-B.radius]
				for E in F.enemies:
					if K(E,Z):
						for G in E.fleetMembers:
							if A1(B.coords,B.radius,G.sprite.get_rect()):
								G.hp-=B.damage
								if G.hp<=0:G.dead=D;E.memberCount-=1;A.earn(G.bounty);E.fleetMembers.remove(G)
						if E.memberCount==0:E.dead=D;A.earn(E.bounty);F.enemies.remove(E)
					elif not K(E,f):
						if A1(B.coords,B.radius,E.sprite.get_rect()):
							E.hp-=B.damage
							if E.hp<=0:E.dead=D;A.earn(E.bounty);F.enemies.remove(E)
		elif B.timer>B.fuse+36:B.dead=D
		else:B.explode()
class G(t):
	hpMulti=1;shipExplode=B.mixer.Sound(AQ);shipExplode.set_volume(0.5);spawnMargin=25
	def __init__(A):super().__init__()
	def positionChooser(C,type):
		global d,e,h,n,i,j,k,l
		if type==AU:C.w=O.width;C.h=O.height
		elif type==AV:C.w=S.width;C.h=S.height
		F=0
		while D:
			E=H;A=[J.choice([950,1200,1200,1450,1450,1700,1700]),J.randint(Q/2-O.height*5,Q/2+O.height*4)]
			if F>100:A3('ERROR: Overcrowding');break
			if A[0]==950 and T(d)>0:
				for B in d:
					if not(A[1]+C.h+G.spawnMargin<B.coords[1]or A[1]>B.coords[1]+B.h+G.spawnMargin):E=D
			elif A[0]==1200 and T(e)>0:
				for B in e:
					if not(A[1]+C.h+G.spawnMargin<B.coords[1]or A[1]>B.coords[1]+B.h+G.spawnMargin):E=D
			elif A[0]==1450:
				for B in h:
					if not(A[1]+C.h+G.spawnMargin<B.coords[1]or A[1]>B.coords[1]+B.h+G.spawnMargin):E=D
			elif A[0]==1700:
				for B in n:
					if not(A[1]+C.h+G.spawnMargin<B.coords[1]or A[1]>B.coords[1]+B.h+G.spawnMargin):E=D
			if E==H:break
			F+=1
		if A[0]==950:d.append(C)
		elif A[0]==1200:e.append(C)
		elif A[0]==1450:h.append(C)
		else:n.append(C)
		I=J.choice([-1,1]);return A,I
	def move(A):
		global d,e,h,n,i,j,k,l
		if A in d:
			if A.coords[1]<=0:i=1
			elif A.coords[1]>Q-100:i=-1
			A.coords[1]+=i*O.speed
		elif A in e:
			if A.coords[1]<=0:j=1
			elif A.coords[1]>Q-100:j=-1
			A.coords[1]+=j*O.speed
		elif A in h:
			if A.coords[1]<=0:k=1
			elif A.coords[1]>Q-100:k=-1
			A.coords[1]+=k*O.speed
		else:
			if A.coords[1]<=0:l=1
			elif A.coords[1]>Q-100:l=-1
			A.coords[1]+=l*O.speed
class O(G):
	sprite=B.image.load(AS);bounty=100;speed=1;width=sprite.get_width();height=sprite.get_height()
	def __init__(A):super().__init__();A.coords,A.direction=A.positionChooser(AU);A.hp=1*G.hpMulti
	def collide(A,other):
		B=other
		if K(B,Y):
			A.hp-=B.damage
			if A.hp<=0:A.dead=D
			G.shipExplode.play()
	def update(A):A.move();C.blit(O.sprite,A.coords)
	def draw(A):C.blit(O.sprite,A.coords)
class S(G):
	sprite=B.image.load('assets/blueTurret.png');bounty=200;speed=0.5;firerate=300;width=sprite.get_width();height=sprite.get_height();bulletSound=B.mixer.Sound(AW);bulletSound.set_volume(0.08)
	def __init__(A):super().__init__();A.coords,A.direction=A.positionChooser(AV);A.cooldown=S.firerate;A.hp=3*G.hpMulti
	def shoot(A):
		if A.cooldown<=0:S.bulletSound.play();F.enemies.append(c([A.coords[0],A.coords[1]+(S.height-c.height)/2]));A.cooldown=S.firerate
	def collide(A,other):
		B=other
		if K(B,Y):
			A.hp-=B.damage
			if A.hp<=0:A.dead=D;G.shipExplode.play()
	def update(A):A.cooldown-=1;A.move();A.shoot();C.blit(S.sprite,A.coords)
	def draw(A):C.blit(S.sprite,A.coords)
class f(G):
	def __init__(A,coords):super().__init__();A.coords=coords
	def collide(A,other):
		if K(other,E):A.dead=D
class c(f):
	sprite=B.image.load('assets/EnemyBullet.png');speed=10;width=sprite.get_width();height=sprite.get_height()
	def __init__(A,coords):super().__init__(coords)
	def move(A):
		A.coords[0]-=c.speed
		if A.coords[0]<=0-c.width:A.dead=D
	def update(A):A.move();C.blit(c.sprite,A.coords)
	def draw(A):C.blit(c.sprite,A.coords)
class V(G):
	sprite=B.transform.scale(B.image.load('assets/EnemySuicide.png'),(50,50));bounty=250;speed=10;width=sprite.get_width();height=sprite.get_height();prepTime=500
	def __init__(A):super().__init__();A.coords=[J.randint(b/2,b*3/4),J.randint(100,Q-100)];A.time=V.prepTime;A.hp=0.5*G.hpMulti
	def move(B):
		if B.time>0:B.angle=U.atan((B.coords[1]-A.coords[1])/(B.coords[0]-A.coords[0]));B.coords[0]+=V.speed/100
		else:
			B.coords[0]-=U.cos(B.angle)*V.speed;B.coords[1]-=U.sin(B.angle)*V.speed
			if B.coords[0]<=0-V.width:B.dead=D
	def collide(A,other):
		B=other
		if K(B,E):A.hp=0;A.dead=D;G.shipExplode.play()
		elif K(B,Y):
			A.hp-=B.damage
			if A.hp<=0:A.dead=D
	def update(A):
		if A.time:A.time-=1
		A.move();C.blit(V.sprite,A.coords)
	def draw(A):C.blit(V.sprite,A.coords)
class Z(G):
	bounty=250;speed=1
	def __init__(A):
		super().__init__();A.coords=[b,J.randint(0,L.height*5)];A.fleetMembers=[L([A.coords[0]+L.width*2,A.coords[1]]),L([A.coords[0]+L.width,A.coords[1]+L.height]),L([A.coords[0],A.coords[1]+L.height*2]),L([A.coords[0]+L.width,A.coords[1]+L.height*3]),L([A.coords[0]+L.width*2,A.coords[1]+L.height*4])]
		for B in A.fleetMembers:B.speed=A.speed
		A.memberCount=T(A.fleetMembers);A.bountyMsg=I.render('Wipe out the insurgent convoy to claim a large bounty!',D,(255,255,255))
	def move(A):
		A.coords[0]-=A.speed
		if A.coords[0]+L.width*3<0:
			for B in A.fleetMembers:A.fleetMembers.remove(B)
			A.dead=D
	def update(B):
		if T(B.fleetMembers)<=0:
			B.dead=D
			if B.memberCount<=0:A.earn(Z.bounty)
			return
		C.blit(B.bountyMsg,(C.get_rect().centerx-B.bountyMsg.get_width()/2,B.bountyMsg.get_height()*2));B.move()
		for E in B.fleetMembers:
			if E.dead:B.fleetMembers.remove(E);continue
			E.update()
	def draw(B):
		if T(B.fleetMembers)<=0:
			B.dead=D
			if B.memberCount<=0:A.earn(Z.bounty)
			return
		for C in B.fleetMembers:
			if C.dead:B.fleetMembers.remove(C);continue
			C.draw()
class L(G):
	sprite=B.image.load('assets/convoyShip.png');bounty=20;speed=1;width=sprite.get_width();height=sprite.get_height()
	def __init__(A,coords):super().__init__();A.hp=1*G.hpMulti;A.coords=coords
	def move(A):A.coords[0]-=A.speed
	def collide(A,other):
		B=other
		if K(B,Y):
			A.hp-=B.damage
			if A.hp<=0:A.dead=D
		elif K(B,E):A.hp=0;A.dead=D;G.shipExplode.play()
	def update(A):A.move();C.blit(L.sprite,A.coords)
	def draw(A):C.blit(L.sprite,A.coords)
class AD(G):
	bounty=10000
	def __init__(A):super().__init__();A.bounty*=F.level/5
	def collide(A,other):
		B=other
		if K(B,Y):
			A.hp-=B.damage
			if A.hp<=0:A.dead=D;F.bossDead=D
class M(AD):
	sprite=B.image.load(AT);firerate=100;suicide_firerate=500;speed=0.5;width=sprite.get_width();height=sprite.get_height();bulletSound=B.mixer.Sound(AW);bulletSound.set_volume(0.08)
	def __init__(A):super().__init__();A.coords=[(b-M.width)*4/5,(Q-M.height)/2];A.hp=20*G.hpMulti;A.cooldown=M.firerate;A.suicideCooldown=M.suicide_firerate;A.direction=J.choice([-1,1]);A.bossBar=p(A.coords[0],A.coords[1],M.sprite.get_width(),13,'',maxval=A.hp,color=(255,0,0))
	def move(A):
		if A.coords[1]<=0:A.direction=1
		elif A.coords[1]>=Q-M.height:A.direction=-1
		A.coords[1]+=A.direction*M.speed
	def shoot(A):
		if A.cooldown<=0:M.bulletSound.play();F.enemies.append(c([A.coords[0],A.coords[1]+(M.height-M.height)/2]));A.cooldown=M.firerate
		if A.suicideCooldown<=0:F.enemies.append(V());A.suicideCooldown=M.suicide_firerate
	def update(A):A.cooldown-=1;A.suicideCooldown-=1;A.move();A.shoot();C.blit(M.sprite,A.coords);A.bossBar.update(A.hp);A.bossBar.x=A.coords[0];A.bossBar.y=A.coords[1]+M.sprite.get_height()+25;A.bossBar.display()
	def draw(A):C.blit(M.sprite,A.coords);A.bossBar.display()
class p:
	def __init__(A,xpos,ypos,width,height,title,maxval=10,notch=H,color=(0,255,0)):super().__init__();A.value=0;A.maxvalue=maxval;A.w=width;A.h=height;A.x=xpos;A.y=ypos;A.title=title;A.notch=notch;A.color=color
	def display(A):
		if F.title.active:return
		B.draw.rect(C,(255,255,255),B.Rect(A.x,A.y,A.w,A.h));B.draw.rect(C,A.color,B.Rect(A.x,A.y,A.value/A.maxvalue*A.w,A.h));G=I.render(A.title,D,(255,255,255));C.blit(G,(A.x+A.w+15,A.y-5))
		if A.notch:
			for E in m(A.maxvalue):B.draw.line(C,(0,0,0),(A.x+E*(A.w/A.maxvalue),A.y),(A.x+E*(A.w/A.maxvalue),A.y+A.h))
	def update(A,val):A.value=val
def AE():
	h='Score: ';global C,F,A;Y=0;Z=0;L=H;P=D;S=B.time.Clock();B.display.set_caption('Space Invaders');C=B.display.set_mode((1920,1080),B.FULLSCREEN|B.SCALED);F=s();A=E();a=p(15,10,100,35,'Health',maxval=A.hp,notch=D,color=(255,0,0));b=p(15,55,100,35,'Shield',maxval=A.shieldMax,notch=D,color=(30,50,255));J=p(250,10,100,35,'Cooldown');c=B.font.SysFont(AK,300);O=c.render('Game Over!',H,(200,0,0));K=I.render(h+N(A.score),H,(255,255,255));K.set_alpha(0);T=-c.get_height();V=1;g=0.1;d=0
	while P:
		if F.test:
			A.money+=100
			if F.level<8:F.level=8
		C.fill((0,0,0))
		if L:F.paused();A.paused()
		else:F.update();A.update(F.shop.active)
		a.update(A.hp);b.update(A.shield)
		if A.getWeapon()==0:J.update(J.maxvalue-A.bulletCD/A.bullet_firerate*J.maxvalue)
		elif A.getWeapon()==1:
			if A.laserTime>0:J.update(J.maxvalue-A.laserTime/A.laserDuration*J.maxvalue)
			else:J.update(J.maxvalue-A.laserCD/A.laser_firerate*J.maxvalue)
		elif A.getWeapon()==2:J.update(J.maxvalue-A.bombCD/A.bomb_firerate*J.maxvalue)
		a.display();b.display();J.display();A0(Y,Z,S.get_fps())
		for W in B.event.get():
			if W.type==B.QUIT:P=H
			if W.type==B.MOUSEWHEEL:A.switchWeapon(A.getWeapon()+W.y*-1)
		G=B.key.get_pressed();A0(Y,Z,S.get_fps())
		if A.hp<=0:
			L=D;M=B.Surface((C.get_width(),C.get_height()));M.set_alpha(120);M.fill((0,0,0));C.blit(M,(0,0));C.blit(O,(C.get_width()/2-O.get_width()/2,T))
			if d>5:
				C.blit(K,(C.get_width()/2-K.get_width()/2,C.get_height()/2+O.get_height()/2));K.set_alpha(min(254,K.get_alpha()+1));e=I.render('Press E to Return to Main Menu',H,(255,255,255));C.blit(e,(C.get_width()/2-e.get_width()/2,C.get_height()/2+O.get_height()/2+K.get_height()+30))
				if G[B.K_e]:F=s();A=E();L=H
			else:
				K=I.render(h+N(A.score),H,(255,255,255));K.set_alpha(0);T+=V
				if T<C.get_height()/2-O.get_height()*3/5:V+=g
				else:V*=-0.5;d+=1
				if G[B.K_RETURN]:return
		elif not L:
			if(G[B.K_UP]or G[B.K_w])and A.coords[1]-(E.shieldHeight-E.height)/2>0:A.coords[1]-=A.speed
			if(G[B.K_DOWN]or G[B.K_s])and A.coords[1]+(E.shieldHeight-E.height/2)<Q:A.coords[1]+=A.speed
			if G[B.K_1]:A.switchWeapon(0)
			if G[B.K_2]:A.switchWeapon(1)
			if G[B.K_SPACE]:A.shoot()
			elif A.getWeapon()==1 and A.laserTime!=A.laserDuration and A.laserTime!=0:A.laserCD=U.floor(A.laser_firerate*max(0.5,A.laserTime/A.laserDuration));A.laserTime=0;E.laserSound.fadeout(300)
			if G[B.K_ESCAPE]:L=D
			if G[B.K_UP]and G[B.K_DOWN]and G[B.K_RIGHT]and G[B.K_LEFT]and G[B.K_b]and G[B.K_a]and not F.test:F.test=D;A3('=========TESTING=========')
			if G[B.K_q]and F.title.active:P=H
			AH(F.enemies);AG();AF(R)
		else:
			M=B.Surface((C.get_width(),C.get_height()));M.set_alpha(120);M.fill((0,0,0));C.blit(M,(0,0));X=I.render('Press ENTER to Resume',H,(255,255,255));f=I.render('Press E to Exit to Main Menu',H,(255,255,255));C.blit(X,(C.get_width()/2-X.get_width()/2,C.get_height()/2));C.blit(f,(C.get_width()/2-f.get_width()/2,C.get_height()/2+X.get_height()+15))
			if G[B.K_RETURN]:L=H
			if G[B.K_e]:F=s();A=E();L=H
		B.display.flip();S.tick(120)
def AF(explosions):
	E=explosions
	if T(E)!=0:
		for D in E:
			F=[]
			for G in r:F.append(B.transform.scale(G,(D[0]*1.5,D[0]*1.5)))
			A=D[1]
			if A[0]%2==0:H=F[A[0]//2].get_height();C.blit(F[A[0]//2],(A[1]+50,A[2]-H/2))
			A[0]+=1
			if A[0]>22:E.remove(D)
def AG():
	for B in A.bullets:
		B.update()
		if B.dead:A.bullets.remove(B);continue
		for C in F.enemies:
			if not K(C,f)and not K(C,Z):
				if C.coords[0]<=B.coords[0]+B.width and C.coords[0]+C.width>=B.coords[0]and C.coords[1]<=B.coords[1]+B.height and C.coords[1]+C.height>=B.coords[1]:
					C.collide(B);B.collide(C);E=J.randrange(-25,25);G=0
					if C.dead:
						A.earn(C.bounty);F.enemies.remove(C)
						try:
							if C.width>C.height:R.append([C.width,[0,B.coords[0]+E,B.coords[1]+G]])
							else:R.append([C.height,[0,B.coords[0]+E,B.coords[1]+G]])
						except:R.append([100,[0,B.coords[0]+E,B.coords[1]+G]])
					else:R.append([50,[0,B.coords[0]+E,B.coords[1]+G]])
					if B.dead:
						try:A.bullets.remove(B)
						except AJ:pass
					break
			elif K(C,Z):
				for D in C.fleetMembers:
					if D.coords[0]<=B.coords[0]+B.width and D.coords[0]+D.width>=B.coords[0]and D.coords[1]<=B.coords[1]+B.height and D.coords[1]+D.height>=B.coords[1]:
						D.collide(B);B.collide(D);E=J.randrange(-25,25);G=0
						if D.dead:
							A.earn(D.bounty);C.memberCount-=1
							try:
								if C.width>C.height:R.append([C.width,[0,B.coords[0]+E,B.coords[1]+G]])
								else:R.append([C.height,[0,B.coords[0]+E,B.coords[1]+G]])
							except:R.append([100,[0,B.coords[0]+E,B.coords[1]+G]])
						else:R.append([50,[0,B.coords[0]+E,B.coords[1]+G]])
						if B.dead:
							try:A.bullets.remove(B)
							except AJ:pass
						break
def AH(enemies):
	D=enemies;global y;global g
	if F.shop.active or F.title.active:return
	E=0
	if g==0:
		for B in D:
			if not K(B,f):E+=1
		if E<F.enemyCap and F.spawned<F.toSpawn:AI(D);F.spawned+=1;g=y
	if g!=0:g-=1
	for B in D:
		if K(B,Z):
			for C in B.fleetMembers:
				if C.coords[0]<=A.coords[0]+A.width and C.coords[0]+C.width>=A.coords[0]and C.coords[1]<=A.coords[1]+A.height and C.coords[1]+C.height>=A.coords[1]:A.collide(B);C.collide(A)
			if B.dead:D.remove(B)
			else:B.update()
		else:
			if B.coords[0]<=A.coords[0]+A.width and B.coords[0]+B.width>=A.coords[0]and B.coords[1]<=A.coords[1]+A.height and B.coords[1]+B.height>=A.coords[1]:A.collide(B);B.collide(A)
			if B.dead:D.remove(B)
			else:B.update()
def AI(enemies):
	A=enemies
	if F.enemyProgression==1:A.append(O())
	elif F.enemyProgression==2:
		B=J.randint(0,1)
		if B==0:A.append(O())
		else:A.append(S())
	elif F.enemyProgression==3:
		B=J.randint(0,2)
		if B==0:A.append(O())
		elif B==1:A.append(S())
		else:A.append(Z())
	elif F.enemyProgression==4:
		B=J.randint(0,3)
		if B==0:A.append(O())
		elif B==1:A.append(S())
		elif B==2:A.append(Z())
		else:A.append(V())
	else:A3('ERROR: Stage above 4')
def A0(coolDown,activeWeapon,fps):
	if F.title.active:return
	E=I.render(A.unlockedWeapons[A.getWeapon()]+' Active',D,(255,255,255))
	if A.money<10:B=I.render('$0.0'+N(a(A.money)),D,(255,255,255))
	elif A.money<100:B=I.render('$0.'+N(a(A.money)),D,(255,255,255))
	else:B=I.render('$'+N(a(A.money))[:-2]+'.'+N(a(A.money))[-2:],D,(255,255,255))
	G=I.render(N(a(fps)),H,(0,255,0));C.blit(E,(15,100));C.blit(G,(1865,0));C.blit(B,(600,0))
def A1(circleCoords,radius,rect):
	B=circleCoords;A=rect;E=[[A.left,A.top],[A.left+A.width,A.top],[A.left,A.top+A.height],[A.left+A.width,A.top+A.height]]
	for C in E:
		if radius<((B[0]-C[0])**2+(B[1]-C[1])**2)**0.5:return D
	return H
if __name__=='__main__':AE()