import pygame, random, math
 
pygame.init()
pygame.font.init()
pygame.mixer.init()

scrn_w = 1920
scrn_h = 1080

my_font = pygame.font.SysFont('Comic Sans MS', 30)

spawnRate = 60     #interval before enemies spawn
spawnDelay = 0    #Initial delay before spawning

explosions = []
explosionSprites = []
for x in range(12):
    explosionSprites.append(pygame.image.load("assets/explosion/"+str(x)+".png"))

class Stage():
    def __init__(self):
        self.background = pygame.image.load("assets/background.jpg")
        self.enemyCap = 10
        self.toSpawn = 10
        self.spawned = 0
        self.stageEnd = 0
        self.level = 0
        self.changeText = my_font.render("Stage "+str(self.level), False, (255, 255, 255))
        self.enemies = []
        self.shop = Shop()
    
    def advance(self):
        self.level += 1
        self.enemyCap = 5+math.ceil(self.level**.5)*5
        self.toSpawn = 9+self.level
        self.spawned = 0
        self.shop.active = True
        self.stageEnd = 300
        self.changeText = my_font.render("Stage "+str(self.level), False, (255, 255, 255))
        if self.level%5 == 0:
            Enemy.hpMulti += 0.2
            player.moneyMulti += 0.1
    
    def update(self):

        screen.blit(self.background, (0,0))

        if self.shop.active:
            self.shop.update()
        elif self.stageEnd > 0:
            self.stageEnd -= 1
            screen.blit(self.changeText, self.changeText.get_rect(center = screen.get_rect().center))
        elif len(self.enemies) == 0:
            self.advance()
        else:
            for enemy in range(len(self.enemies)):
                self.enemies[enemy].update()

class Shop():
    def __init__(self):
        self.active = False
        self.items = {# name = [level, max, price, price scaling[liner, exponential, ...], scaling start level[linear, exponential, ...]]
            "Buy Laser Beam": [0, 1, 5000, [], []],
            "Upgrade Laser Cannon Damage": [0, -1, 1000, [100, 1.1], [0, 10]],
            "Upgrade Laser Beam Damage": [0, -1, 5000, [1000, 1.2], [0, 10]],
            "Upgrade Laser Beam Duration": [0, 10, 100000, [0, 2], [0, 0]]
        }
        self.itemKeys = [
            "Buy Laser Beam",
            "Upgrade Laser Cannon Damage",
            "Upgrade Laser Beam Damage",
            "Upgrade Laser Beam Duration"
        ]
        self.clickToggle = False
    
    def buy(self, item):
        if item in self.items:
            upgrade = self.items[item]
            if upgrade[0] < upgrade[1] and player.money >= upgrade[2]:
                upgrade[0] += 1
                for scale in range(len(upgrade[4])):
                    if upgrade[0] > upgrade[4][scale]:
                        if scale == 0:
                            upgrade[2] += upgrade[3][0]
                        elif scale == 1:
                            upgrade[2] *= upgrade[3][1]
                        elif scale == 2:
                            upgrade[2] **= upgrade[3][2]
                if item == "Buy Laser Beam":
                    player.unlockedWeapons.insert(1, "Laser Beam")
                elif item == "Upgrade Laser Cannon Damage":
                    Bullet.damage += 0.5
                elif item == "Upgrade Laser Beam Damage":
                    Laser.damage += 0.25
                elif item == "Upgrade Laser Beam Duration":
                    player.laserDuration += 50

    def display(self):
        x_offset = 100
        y_offset = 150
        button_w = 500
        button_h = 50
        spacing_w = 50
        spacing_h = 50
        self.buttons = []
        button = 0
        for key in self.items:
            if player.money >= self.items[key][2] and self.items[key][0] < self.items[key][1]:
                color = (0, 255, 0)
            else:
                color = (220, 220, 220)
            self.buttons.append(pygame.Rect(x_offset, y_offset, button_w, button_h))
            pygame.draw.rect(screen, color, self.buttons[button])
            screen.blit(my_font.render(key, False, (0, 0, 0)), self.buttons[button])
            x_offset += button_w + spacing_w
            if x_offset + button_w + 100 > scrn_w:
                x_offset = 100
                y_offset += button_h + spacing_h
            button += 1

    def detectClick(self):
        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not self.clickToggle:
            self.clickToggle = True
            for button in range(len(self.buttons)):
                if self.buttons[button].collidepoint(pos):
                    self.buy(self.itemKeys[button])
        elif not mouse[0]:
            self.clickToggle = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.active = False
        self.detectClick()
        self.display()

class Entity():
    def __init__(self):
        self.dead = False

class Player(Entity):
    playerSprite = pygame.image.load("assets/Ship.png")
    shieldSprite = pygame.image.load("assets/Shield.png")
    width = playerSprite.get_width()
    height = playerSprite.get_height()
    shieldWidth = shieldSprite.get_width()
    shieldHeight = shieldSprite.get_height()

    #sfx
    laserSound = pygame.mixer.Sound("assets/laser.wav")#
    laserSound.set_volume(0.2)
    bulletSound = pygame.mixer.Sound("assets/mixkit-short-laser-gun-shot-1670.wav")#
    shipHit = pygame.mixer.Sound("assets/ship_hit.wav")
    shipHit.set_volume(0.3)
    shieldHit = pygame.mixer.Sound("assets/shield_hit.wav")
    shieldHit.set_volume(0.2)
    reloadSound = pygame.mixer.Sound("assets/reloaded.wav")
    reloadSound.set_volume(0.1)
    shieldBreak = pygame.mixer.Sound("assets/break.wav")
    shieldBreak.set_volume(0.5)
    shipExplode = pygame.mixer.Sound("assets/explosion.wav")
    shipExplode.set_volume(0.5)

    def __init__(self):
        super().__init__()
        self.coords = [25, (scrn_h-Player.height)/2]
        self.hp = 3
        self.shield = 5
        self.shieldMax = 5
        self.shieldRegenSpeed = 500
        self.shieldTimer = 0
        self.speed = 3
        self.bulletCD = 0
        self.bullet_firerate = 200
        self.laserCD = 0
        self.laser_firerate = 1000
        self.laserTime = 0
        self.laserDuration = 300
        self.bullets = []
        self.bulletSpeed = 20
        self.weapon = 0
        self.unlockedWeapons = ["Laser Cannon"]
        self.invTime = 0
        self.money=0
        self.moneyMulti = 1

    def getWeapon(self):
        return self.weapon

    def switchWeapon(self, slot):
        self.weapon = slot
        if self.weapon < 0:
            self.weapon = len(self.unlockedWeapons)-1
        elif self.weapon >= len(self.unlockedWeapons):
            self.weapon = 0

    def shoot(self):
        if self.unlockedWeapons[self.weapon] == "Laser Cannon":
            if self.bulletCD <= 0:
                self.bullets.append(Bullet(self.coords.copy(), self.bulletSpeed, 0))
                self.bulletCD = self.bullet_firerate
                #Player.bulletSound.play()
        elif self.unlockedWeapons[self.weapon] == "Laser Beam":
            if self.laserCD <= 0 and self.laserTime < self.laserDuration:
                self.bullets.append(Laser(self.coords.copy(), 0))
                self.laserTime += 1
                #Player.laserSound.play()
            elif self.laserTime >= self.laserDuration:
                self.laserCD = self.laser_firerate
                self.laserTime = 0
                #Player.laserSound.fadeout(300)

    def collide(self, other):
        if isinstance(other, Enemy) and not self.invTime:
            self.invTime = 50
            if self.shield:
                self.shield -= 1
                x_offset = random.randrange(-25, 25)
                y_offset = 0
                explosions.append([0, other.coords[0] + x_offset, other.coords[1] + y_offset])
                if self.shield == 0:
                    Player.shieldBreak.play()
                else:
                    Player.shieldHit.play()

            else:
                self.hp -= 1
                x_offset = random.randrange(-25, 25)
                y_offset = 0
                explosions.append([0, other.coords[0] + x_offset, other.coords[1] + y_offset])
                if self.hp == 0:
                    Player.shipExplode.play()
                else:
                    Player.shipHit.play()

            if self.shield <= 0:
                self.shieldTimer = self.shieldRegenSpeed * -1
    
    def regenShield(self):
        if self.shield < self.shieldMax:
            self.shieldTimer += 1
        if self.shieldTimer >= self.shieldRegenSpeed:
            self.shield += 1
            self.shieldTimer = 0

    def earn(self, amt):
        self.money += amt*self.moneyMulti

    def update(self):
        screen.blit(Player.playerSprite, self.coords)
        self.regenShield()
        if self.shield > 0:
            screen.blit(Player.shieldSprite, [self.coords[0]-(Player.shieldWidth-Player.width)/2, self.coords[1]-(Player.shieldHeight-Player.height)/2])
        if self.bulletCD > 0 :
            self.bulletCD -= 1
            if (self.bulletCD == 0):
                Player.reloadSound.play()
        if self.laserCD > 0:
            self.laserCD -= 1
            if (self.laserCD == 0):
                Player.reloadSound.play()
        if self.invTime > 0:
            self.invTime -= 1
        for bullet in self.bullets:
            bullet.update()

class PlayerProjectile(Entity):
    def __init__(self, coords, speed, angle):
        super().__init__()
        self.coords = coords
        self.speed = speed
        self.angle = angle

    def move(self):
        self.coords[0] += math.cos(self.angle)*self.speed
        self.coords[1] += math.sin(self.angle)*self.speed
        if self.coords[0] > scrn_w:
            self.dead = True

class Bullet(PlayerProjectile):
    sprite = pygame.image.load("assets/playerBullet.png")
    width = sprite.get_width()
    height = sprite.get_height()
    damage = 1

    def __init__(self, coords, speed, angle):
        super().__init__(coords, speed, angle)
    
    def collide(self, other):
        if isinstance(other, Enemy) and not isinstance(other, EnemyProjectile):
            self.dead = True

    def update(self):
        self.move()
        screen.blit(Bullet.sprite, self.coords)

class Laser(PlayerProjectile):
    baseSprite = pygame.image.load("assets/laser_base.png")
    sprite = pygame.image.load("assets/laser.png")
    width = sprite.get_width()
    height = sprite.get_height()
    baseOffsetY = (baseSprite.get_height()-height)/2
    damage = 0.5

    def __init__(self, coords, angle, speed=sprite.get_width()):
        super().__init__([coords[0]+player.width*5/7, coords[1]+(player.height-Laser.height)/2], speed, angle)
    
    def collide(self, other):
        if isinstance(other, Enemy) and not isinstance(other, EnemyProjectile):
            self.dead = True

    def update(self):
        self.move()
        if self.coords != [player.coords[0]+player.width*5/7+Laser.width, player.coords[1]+(player.height-Laser.height)/2]:
            screen.blit(Laser.sprite, self.coords)
        else:
            screen.blit(Laser.baseSprite, [self.coords[0], self.coords[1]-Laser.baseOffsetY])

class Enemy(Entity):
    hpMulti = 1
    shipExplode = pygame.mixer.Sound("assets/explosion.wav")
    shipExplode.set_volume(0.5)

    def __init__(self):
        super().__init__()

class Strafer(Enemy):
    sprite = pygame.image.load("assets/Ship.png")                                                   #change this
    bounty = 100
    speed = 1
    hp = 1*Enemy.hpMulti
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self):
        super().__init__()
        self.coords = [random.randint(scrn_w/2, scrn_w-100), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-Strafer.height:
            self.direction = -1
        self.coords[1] += self.direction*Strafer.speed
    
    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
            Enemy.shipExplode.play()
      
    def update(self):
        self.move()
        screen.blit(Strafer.sprite, self.coords)

class BlueTurret(Enemy):
    sprite = pygame.image.load("assets/Shield.png")                                                 #change this
    bounty = 150
    speed = 0.5
    firerate = 300
    hp = 3*Enemy.hpMulti
    width = sprite.get_width()
    height = sprite.get_height()
    bulletSound = pygame.mixer.Sound("assets/enemy_shoot.wav")
    bulletSound.set_volume(0.08)#idk too loud

    def __init__(self):
        super().__init__()
        self.coords = [random.choice([scrn_w/2, scrn_w*2/3, scrn_w*5/6]), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])
        self.cooldown = BlueTurret.firerate

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-BlueTurret.height:
            self.direction = -1
        self.coords[1] += self.direction*BlueTurret.speed

    def shoot(self):
        if self.cooldown <= 0:
            BlueTurret.bulletSound.play()
            stage.enemies.append(EnemyBullet([self.coords[0], self.coords[1]+(BlueTurret.height-EnemyBullet.height)/2]))
            self.cooldown = BlueTurret.firerate
    
    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
                Enemy.shipExplode.play()
    
    def update(self):
        self.cooldown -= 1
        self.move()
        self.shoot()
        screen.blit(BlueTurret.sprite, self.coords)

class EnemyProjectile(Enemy):
    def __init__(self, coords):
        super().__init__()
        self.coords = coords
    
    def collide(self, other):
        if isinstance(other, Player):
            self.dead = True

class EnemyBullet(EnemyProjectile):
    sprite = pygame.image.load("assets/EnemyBullet.png")
    speed = 10
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, coords):
        super().__init__(coords)
    
    def move(self):
        self.coords[0] -= EnemyBullet.speed
        if self.coords[0] <= 0-EnemyBullet.width:
            self.dead = True
    
    def update(self):
        self.move()
        screen.blit(EnemyBullet.sprite, self.coords)

class SuicideEnemy(Enemy):
    sprite = pygame.transform.scale(pygame.image.load("assets/EnemySuicide.png"), (50, 50))
    bounty = 250
    speed = 10
    hp = 0.5*Enemy.hpMulti
    width = sprite.get_width()
    height = sprite.get_height()
    prepTime = 500

    def __init__(self):
        super().__init__()
        self.coords = [random.randint(scrn_w/2, scrn_w*3/4), random.randint(100, scrn_h-100)]
        self.time = SuicideEnemy.prepTime
    
    def move(self):
        if(self.time > 0):
            self.angle = math.atan((self.coords[1]-player.coords[1])/(self.coords[0]-player.coords[0]))
            self.coords[0] += SuicideEnemy.speed/100
        else:
            self.coords[0] -= math.cos(self.angle)*SuicideEnemy.speed
            self.coords[1] -= math.sin(self.angle)*SuicideEnemy.speed
            if self.coords[0] <= 0-SuicideEnemy.width:
                self.dead = True

    def collide(self, other):
        if isinstance(other, Player):
            self.hp = 0
            self.dead = True
            Enemy.shipExplode.play()
        elif isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True

    def update(self):
        if self.time:
            self.time -= 1
        self.move()
        screen.blit(SuicideEnemy.sprite, self.coords)


class Bar():
    def __init__(self, xpos, ypos, width, height, title, maxval=10, notch=False, color=(0,255,0)):
        super().__init__()
        self.value = 0
        self.maxvalue = maxval
        self.w = width
        self.h = height
        self.x = xpos
        self.y = ypos
        self.title = title
        self.notch = notch
        self.color = color

    def display(self):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, (self.value/self.maxvalue)*self.w,self.h))
        barText = my_font.render(self.title, False, (255, 255, 255))
        screen.blit(barText, (self.x+self.w+15, self.y))

        if (self.notch):
            for x in range(self.maxvalue):
                pygame.draw.line(screen, (0, 0, 0), (self.x+(x*(self.w/self.maxvalue)), self.y), (self.x+(x*(self.w/self.maxvalue)), self.y+self.h))
   
    def update(self, val):
        self.value = val

enemyTypes = [Strafer(), BlueTurret(), SuicideEnemy()]

# define a main function
def main():
    global screen, stage, player

    coolDown = 0
    activeWeapon = 0
    keyPressCD = 0

    running = True
    
    frametime = pygame.time.Clock()
  
    #music
    #pygame.mixer.music.load("assets/background.mp3")#
    #pygame.mixer.music.set_volume(0.1)#
    #pygame.mixer.music.play()# 

    #pygame.display.set_icon(pygame.image.load("assets/logo.png"))                              reenable this
    pygame.display.set_caption("Space Invaders")
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN|pygame.SCALED)

    stage = Stage()
     
    player = Player()

    ##########
    health_bar = Bar(15, 0, 100, 35, "Health", maxval=player.hp, notch=True, color=(255, 0, 0))
    shield_bar = Bar(15, 40, 100, 35, "Shield", maxval=player.shield, notch=True, color=(30, 50, 255))   
    cooldown_bar = Bar(250, 0, 120, 50, "Cooldown")
    ##########

    # main loop
    while running:
        screen.fill((0,0,0)) #Clears the screen
  
        stage.update()

        player.update()

        health_bar.update(player.hp)
        shield_bar.update(player.shield)

        if player.getWeapon() == 0:
            cooldown_bar.update(cooldown_bar.maxvalue-(player.bulletCD/player.bullet_firerate)*cooldown_bar.maxvalue)

        elif player.getWeapon() == 1:
            if player.laserTime > 0:
                cooldown_bar.update(cooldown_bar.maxvalue-((player.laserTime)/player.laserDuration)*cooldown_bar.maxvalue)
            else:
                cooldown_bar.update(cooldown_bar.maxvalue-(player.laserCD/player.laser_firerate)*cooldown_bar.maxvalue)


        health_bar.display()
        shield_bar.display()
        cooldown_bar.display()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                player.switchWeapon(player.getWeapon()+event.y*-1)
     
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.coords[1] - (Player.shieldHeight-Player.height)/2 > 0:
            player.coords[1] -= player.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.coords[1] + (Player.shieldHeight-Player.height/2) < scrn_h:
            player.coords[1] += player.speed

        if keys[pygame.K_1]:
            player.switchWeapon(0)
        if keys[pygame.K_2]:
            player.switchWeapon(1)

        if keys[pygame.K_SPACE]:
            player.shoot()
        elif player.getWeapon() == 1 and player.laserTime != player.laserDuration and player.laserTime != 0:
                player.laserCD = math.floor(player.laser_firerate * max(0.5, player.laserTime / player.laserDuration))
                player.laserTime = 0
                Player.laserSound.fadeout(300)
        
        if keyPressCD != 0:
            keyPressCD -= 1

        enemyCore(stage.enemies)
        playerBulletCore()
        explosionCore(explosions)

        renderHUD(coolDown, activeWeapon, frametime.get_fps())
        pygame.display.flip()
        frametime.tick(120)

def explosionCore(explosions):
    for x in explosions:
        if x[0] % 2 == 0:
            screen.blit(explosionSprites[x[0]//2], (x[1], x[2]))
        x[0] += 1
        if x[0] > 22:
            explosions.remove(x)

def playerBulletCore():
    for x in player.bullets:
        x.update()

        if x.dead:
            player.bullets.remove(x)
            continue

        for ship in stage.enemies:
            if not isinstance(ship, EnemyProjectile):
                if ship.coords[0] <= x.coords[0] + x.width and ship.coords[0] + ship.width >= x.coords[0] and ship.coords[1] <= x.coords[1] + x.height and ship.coords[1] + ship.height >= x.coords[1]:          #detects bullet collision
                    ship.collide(x)
                    x.collide(ship)

                    if ship.dead:
                        player.earn(ship.bounty)
                        stage.enemies.remove(ship)

                    x_offset = random.randrange(-25, 25)
                    y_offset = 0


                    explosions.append([0, x.coords[0] + x_offset, x.coords[1] + y_offset])
                    
                    if x.dead:
                        try:
                            player.bullets.remove(x)
                        except ValueError:
                            pass

def enemyCore(enemies):
    global spawnRate
    global spawnDelay
    if stage.shop.active:
        return
    numEnemies = 0
    if spawnDelay == 0:
        for x in enemies:
            if not isinstance(x, EnemyProjectile):
                numEnemies += 1
        if numEnemies < stage.enemyCap and stage.spawned < stage.toSpawn:
            enemies.append(random.choice([Strafer(), BlueTurret(), SuicideEnemy()]))
            stage.spawned += 1
            spawnDelay = spawnRate

    if spawnDelay != 0:
        spawnDelay -= 1

    for x in enemies:
        if x.coords[0] <= player.coords[0] + player.width and x.coords[0] + x.width >= player.coords[0] and x.coords[1] <= player.coords[1] + player.height and x.coords[1] + x.height >= player.coords[1]:
            player.collide(x)
            x.collide(player)
        if x.dead:
            enemies.remove(x)
        else:
            x.update()

    #enemyMove(enemies)                                                                                     needs fixing

def enemyMove(enemies):
        g1 = []
        g2 = []
        g3 = []

        for index in range(len(enemies)):
            if enemies[index].coords[0] == 1250:
                g1.append(index)
            elif enemies[index].coords[0] == 1450:
                g2.append(index)
            else:
                g3.append(index)
        
        if len(g1) > 0:                 #makes newly spawned enemies move in the same direction as others
            for x in g1:
                if not isinstance(enemies[x], EnemyProjectile):
                    if enemies[x].direction != enemies[g1[0]].direction:
                        enemies[x].direction = enemies[g1[0]].direction
        if len(g2) > 0:
            for x in g2:
                if not isinstance(enemies[x], EnemyProjectile):
                    if enemies[x].direction != enemies[g2[0]].direction:
                        enemies[x].direction = enemies[g2[0]].direction
        if len(g3) > 0:
            for x in g3:
                if not isinstance(enemies[x], EnemyProjectile):
                    if enemies[x].direction != enemies[g3[0]].direction:
                        enemies[x].direction = enemies[g3[0]].direction

        large_g1 = 0                                        #inverts direction of column if out of bounds
        small_g1 = 1080
        for index in g1:
            if enemies[index].coords[1] > large_g1:
                large_g1 = enemies[index].coords[1]
            if enemies[index].coords[1] < small_g1:
                small_g1 = enemies[index].coords[1]
        if small_g1 < 10 or large_g1 > 1000:
            for x in g1:
                if not isinstance(enemies[x], EnemyProjectile):
                    enemies[x].direction = -enemies[x].direction

        large_g2 = 0                                        #inverts direction of column if out of bounds
        small_g2 = 1080
        for index in g2:
            if enemies[index].coords[1] > large_g2:
                large_g2 = enemies[index].coords[1]
            if enemies[index].coords[1] < small_g2:
                small_g2 = enemies[index].coords[1]
        if small_g2 < 10 or large_g2 > 1000:
            for x in g2:
                if not isinstance(enemies[x], EnemyProjectile):
                    enemies[x].direction = -enemies[x].direction

        large_g3 = 0                                        #inverts direction of column if out of bounds
        small_g3 = 1080
        for index in g3:
            if enemies[index].coords[1] > large_g3:
                large_g3 = enemies[index].coords[1]
            if enemies[index].coords[1] < small_g3:
                small_g3 = enemies[index].coords[1]
        if small_g3 < 10 or large_g3 > 1000:
            for x in g3:
                if not isinstance(enemies[x], EnemyProjectile):
                    enemies[x].direction = -enemies[x].direction

        for x in enemies:
            x.update()

def renderHUD(coolDown, activeWeapon, fps):
        
        if player.getWeapon() == 0:
            #CDtext = my_font.render(str(player.bulletCD), False, (255, 255, 255))
            activeWeaponText = my_font.render("Laser Cannon Active", False, (255, 255, 255))
        elif player.getWeapon() == 1:
            #CDtext = my_font.render(str(player.laserCD), False, (255, 255, 255))
            activeWeaponText = my_font.render("Laser Beam Active", False, (255, 255, 255))
        if player.money < 10:
            money = my_font.render("$0.0"+str(player.money), False, (255, 255, 255))
        elif player.money < 100:
            money = my_font.render("$0."+str(player.money), False, (255, 255, 255))
        else:
            money = my_font.render('$'+str(player.money)[:-2]+'.'+str(player.money)[-2:], False, (255, 255, 255))

        frameRate = my_font.render(str(int(fps)), False, (0, 255, 0))

        #screen.blit(CDtext, (10,0))
        screen.blit(activeWeaponText, (10, 90))
        screen.blit(frameRate, (1865, 0))
        screen.blit(money, (600,0))

     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main() 
